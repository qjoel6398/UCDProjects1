# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:31:47 2017

@author: minifast026
"""

"""The purpose of this project was to classify a point dataset of Denver street intersections by the combination of road volume classes that made them up. After classifying the intersections, one could analyze different occurrences (such as bicycle crashes) based on volume-class intersection makeup.
"""

import arcpy
from arcpy import env
from time import clock
import numpy as np
import math
import pdb

t0 = clock()
env.workspace = r'\\ifast\iUniversity\joelq\Desktop\PROJECT INTERSECTION\PROJECT INTERSECTION\PROJECT INTERSECTION.gdb'
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")
env.qualifiedFieldNames = "UNQUALIFIED"

def uniqueCategories(inputDict):
    """Takes a dictionary of categorized intersections and returns only the unique categories.
    """
    sums = []
    valuesgroup = np.array(inputDict.values())
    for j in valuesgroup:
        sums.append(sum(j))
    uniqueCategories = np.unique(np.array(sums))
    return uniqueCategories

def GetSummedCategories(inputDict):
    """Takes a dictionary of road classes making up each intersection and aggregates them into a summed value for categorization.
    """
    sums5way = {}
    for k,v in inputDict.items():
        sums5way[k]=sum(v)
    return sums5way


def categorizeVolClass(intersectionPoints, streetLines):
    """
    This function takes intersection point data, buffers them, then checks all line data to see if they cross each buffer.
    If a line crosses the buffer, its VOLCLASS attribute is coded as a number('LOCAL' = 1, 'COLLECTOR' = 10, 'ARTERIAL' = 100) and is placed in a "category bin",
        which is a list of the VOLCLASS' of streets making up the intersection.
    The sum of this category_bin is a code representing the combination of VOLCLASS' making up the intersection.
    The length of this bin tells us how many streets make up the intersection (4-way, 5-way, etc.)
    This function inserts the sum and length of category_bin into the attribute table of the input point dataset.
    This function also returns a pandas DataFrame of the unique identifiers of the intersections, along with their corresponding category bins.

        param intersectionPoints:: a point dataset containing intersections.

        param streetLines:: a line dataset containing street centerlines.

    """
    arcpy.Buffer_analysis(intersectionPoints, 'intersections_buf', '2 feet')
    arcpy.AddField_management(r'intersections_buf', 'INT_TYPE', 'SHORT')
    Intersections7way = {}
    Intersections6way = {}
    Intersections5way = {}
    Intersections4way = {}
    Intersections3way = {}
    Intersections2way = {}
    Intersections1way = {}
    fieldsPolygons = ['SHAPE@', 'MASTERID', 'INT_TYPE']
    fieldsLines = ['SHAPE@', 'VOLCLASS']
    with arcpy.da.UpdateCursor('intersections_buf',fieldsPolygons) as polygons_Ucur:
        for polygon_row in polygons_Ucur:
            category_bin = []
            with arcpy.da.SearchCursor(streetLines,fieldsLines) as lines_Scur:
                for linerow in lines_Scur:
                    if polygon_row[0].crosses(linerow[0]) is True:
                        if linerow[1] == 'LOCAL':
                            category_bin.append(1)
                        elif linerow[1] == 'COLLECTOR':
                            category_bin.append(10)
                        elif linerow[1] == 'ARTERIAL':
                            category_bin.append(100)
                        else:
                            pass

            #pdb.set_trace()
            polygon_row[2] = sum(category_bin)
            polygons_Ucur.updateRow(polygon_row)
            if len(category_bin) == 7:
                Intersections7way[polygon_row[1]] = category_bin
            elif len(category_bin) == 6:
                Intersections6way[polygon_row[1]] = category_bin
            elif len(category_bin) == 5:
                Intersections5way[polygon_row[1]] = category_bin
            elif len(category_bin) == 4:
                Intersections4way[polygon_row[1]] = category_bin
            elif len(category_bin) == 3:
                Intersections3way[polygon_row[1]] = category_bin
            elif len(category_bin) == 2:
                Intersections2way[polygon_row[1]] = category_bin
            elif len(category_bin) == 1:
                Intersections1way[polygon_row[1]] = category_bin
            else:
                pass
    del polygons_Ucur
    del lines_Scur
    arcpy.JoinField_management(intersectionPoints, "MASTERID", "intersections_buf", "MASTERID", ["INT_TYPE"])
    print 'Loop - elapsed time: ', round(clock()-t0,4), ' seconds'
    print 'Intersections Categorized!'
    dictionaries = [\
    Intersections7way,\
    Intersections6way,\
    Intersections5way,\
    Intersections4way,\
    Intersections3way,\
    Intersections2way,\
    Intersections1way]
    return dictionaries


StreetCenterlineslist = []
Intersectionslist = []
dictionarieslist = []

#One problem I had with this project was the sheer amount of calculation that this was doing. As I clocked the progress, I saw that processsing time was increasing exponentially. To solve this, I split the study area up into tiles, ran the process on each individual tile, and then merged the results at the end. This was significantly faster.

testbounds = ['testbound01','testbound02','testbound03','testbound04','testbound05','testbound06','testbound07','testbound08','testbound09','testbound10']
intersectionclips = ['intersection_tb01', 'intersection_tb02','intersection_tb03','intersection_tb04','intersection_tb05', 'intersection_tb06', 'intersection_tb07','intersection_tb08','intersection_tb09','intersection_tb10']
streetclips = ['street_tb01', 'street_tb02','street_tb03','street_tb04','street_tb05', 'street_tb06', 'street_tb07','street_tb08','street_tb09','street_tb10']



#Running the process
for i in range(len(testbounds)):
    arcpy.FeatureClassToFeatureClass_conversion ('Test_Boundary', env.workspace, testbounds[i], "OBJECTID = " + str(i+1))
    Intersectionslist.append(arcpy.Clip_analysis ('Intersections', testbounds[i], intersectionclips[i]))
    StreetCenterlineslist.append(arcpy.Clip_analysis ('street_centerlines', testbounds[i], streetclips[i]))
    dictionarieslist.append(categorizeVolClass(Intersectionslist[i], StreetCenterlineslist[i]))


arcpy.Merge_management(StreetCenterlineslist, 'StreetCenterlinesFinal')
arcpy.Merge_management(Intersectionslist, 'IntersectionsFinal')
