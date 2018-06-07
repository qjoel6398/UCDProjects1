# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 19:36:27 2017

@author: joelq
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 21:06:51 2017

@author: joelq
"""

import arcpy
from arcpy import env
import numpy as np
import math

def uniqueCategories(inputDict):
    """
    """
    sums = []
    valuesgroup = np.array(inputDict.values())
    for j in valuesgroup:
        sums.append(sum(j))
    uniqueCategories = np.unique(np.array(sums))
    return uniqueCategories

def GetSummedCategories(inputDict):
    """
    """
    sums5way = {}
    for k,v in Intersections5way.items():
        sums5way[k]=sum(v)
    return sums5way

def GetAzimuthPolyline(shape):
    """
    """
    radian = math.atan((shape.lastPoint.Y - shape.firstPoint.Y)/(shape.lastPoint.X - shape.firstPoint.X))
    degrees = radian * 180 / math.pi
    return degrees


env.workspace = r'H:\Fall17_Geog4092_McLaurin\PROJECT INTERSECTIONS\5092_Project.gdb'
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

env.qualifiedFieldNames = "UNQUALIFIED"



#EXTRACTING DATA:
arcpy.ListFeatureClasses()

#BUFFER POINT FEATURES BEFORE RUNNING SPATIAL JOIN
#Buffer_analysis(in_features, out_feature_class, buffer_distance_or_field)

#ADD NEW FIELD FOR NEW INTERSECTION CATEGORY
arcpy.AddField_management(r'IntersectionVolClass_test', 'INT_TYPE', 'SHORT')

##Maybe don't need to do this
#sr = arcpy.SpatialReference(26754)#epsg projection 26754 - nad27 / colorado central
#arcpy.DefineProjection_management (r'IntersectionVolClass_test', sr)
#arcpy.DefineProjection_management (r'street_centerline_test', sr)


#polygons_U = arcpy.da.UpdateCursor('IntersectionVolClass_test',fieldsPolygons)
#polygons_S = arcpy.da.SearchCursor('IntersectionVolClass_test',fieldsPolygons)
#lines_I = arcpy.da.InsertCursor('street_centerline_test',fieldsLines)
#lines_S = arcpy.da.SearchCursor('street_centerline_test',fieldsLines)

#EMPTY DICTIONARIES TO CATEGORIZE THE DIFFERENT LENGTHS OF INTERSECTIONS
Intersections7way = {}
Intersections6way = {}
Intersections5way = {}
Intersections4way = {}
Intersections3way = {}
Intersections2way = {}
Intersections1way = {}

"""
This part is meant to open up cursors, find out if a line intersects a polygon, then, 
if so, it will categorize the polygon with a tag for the VOLCLASS of each line that intersects it.
after the polygon is tagged with a multipart categorization, a sum of that categorization is calculated, 
resulting in one number to be placed in the newly created field. 

The bin created for each polygon will also be thrown into one of several dictionaries depending on their length; 
these dictionaries will categorize intersection by number of streets it consists of.

*Should I use update cursor, or calculatefield_management?
**Figure our SQL Error
***Look at more example code to help use update cursor correctly, etc.
"""

fieldsLines = ['SHAPE@', 'VOLCLASS', 'MASTERID']
with arcpy.da.SearchCursor(r'street_centerline_test',fieldsLines) as lines_Scur:
    for linerow in lines_Scur:
        print (linerow[2], GetAzimuthPolyline(linerow[0]))
        
        
#OPENING UP CURSORS
fieldsPolygons = ['SHAPE@', 'MASTERID', 'INT_TYPE']
fieldsLines = ['SHAPE@', 'VOLCLASS']
with arcpy.da.UpdateCursor('IntersectionVolClass_test',fieldsPolygons) as polygons_Ucur:
#CREATING THE POLYGON CATEGORY BIN (runs 206x):
    for polygon_row in polygons_Ucur: #Getting an error somewhere around here:""" RuntimeError: An invalid SQL statement was used. [SELECT @SHAPE, MASTERID, INT_TYPE, OBJECTID_1, Shape_Area, Shape_Length FROM IntersectionVolClass_test]"""
        category_bin = []
        #print "for this polygon:"
#TESTING IF THE LINE CROSSES THE POLYGON (runs__x):
        with arcpy.da.SearchCursor(r'street_centerline_test',fieldsLines) as lines_Scur:
            for linerow in lines_Scur:
                #print "for this line:"
#Polyline.crosses not working for some reason. I think it has to do with the data not crossing in Arcmap.
                if polygon_row[0].crosses(linerow[0]) is True:
                    #print "Line cross found!"
                    #print linerow[1]
                    
    #FILLING THE POLYGON CATEGORY BIN USING NUMBERS FOR EACH ROAD TYPE:
                    if linerow[1] == 'LOCAL':
                        category_bin.append(1)  
                       # print "LOCAL found!"
                    elif linerow[1] == 'COLLECTOR':
                        category_bin.append(10)
                        #print "COLLECTOR found!"
                    elif linerow[1] == 'ARTERIAL':
                        category_bin.append(100)
                        #print "ARTERIAL found!"
                    else:
                        pass  
                
#PLACING THE SUM OF THAT POLYGON CATEGORY BIN INTO THE NEW FIELD "INT_TYPE" (POSSIBLY USING UPDATE CURSOR INCORRECTLY):
#        polygons_Ucur.updateRow([polygon_row[0], polygon_row[1], sum(category_bin)])
        polygon_row[2] = sum(category_bin)
        polygons_Ucur.updateRow(polygon_row)
        
#CATEGORIZING EACH POLYGON BIN BY LENGTH, SIGNIFYING NUMBER OF ROADS COMPRISING THE ROAD INTERSECTION:
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

#DELETE CURSORS:
del polygons_Ucur
del lines_Scur

#NOW, WE HAVE DICTIONARIES THAT CONTAIN THE CATEGORYBINS OF EACH "WAY" OF INTERSECTION
category_bin
dictionaries = [\
Intersections7way,\
Intersections6way,\
Intersections5way,\
Intersections4way,\
Intersections3way,\
Intersections2way,\
Intersections1way]

#USED A FUNCTION HERE TO CALCULATE THE UNIQUE SUMS OF THESE VALUE GROUPINGS:
    #THE NEXT STEP IS TO IDENTIFY IF THESE UNIQUE SUMS ACTUALLY REPRESENT UNIQUE CATEGORIES OF INTERSECTION
unique_5way = uniqueCategories(Intersections5way)
unique_4way = uniqueCategories(Intersections4way)
unique_3way = uniqueCategories(Intersections3way)
unique_2way = uniqueCategories(Intersections2way)
unique_1way = uniqueCategories(Intersections1way)

unique_5way
unique_4way
unique_3way
unique_2way
unique_1way

Intersections7way
GetSummedCategories(Intersections7way)
Intersections6way
GetSummedCategories(Intersections6way)
Intersections5way
GetSummedCategories(Intersections5way)
Intersections4way
GetSummedCategories(Intersections4way)
Intersections3way
GetSummedCategories(Intersections3way)
Intersections2way
GetSummedCategories(Intersections2way)
Intersections1way





