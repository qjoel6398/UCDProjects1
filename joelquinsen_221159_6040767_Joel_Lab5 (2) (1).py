# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:29:59 2017

@author: minifast026
"""



#import every tool i can find:
import os
import gdal, gdalconst, gdalnumeric
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import time
#gjm: you need to import the lab5functions module:
from lab5functions import *

path = r'/Users/gmaclaur/GEOG4092/lab5/data'
subfolder = r'/Users/gmaclaur/GEOG4092/lab5/data/L5_big_elk'
os.chdir(path) #set working directory in python
demName = 'bigElk_dem.tif'
firePerimeter = 'fire_perimeter.tif'
landsats = [subfolder+r'/L5034032_2002_B3.tif', subfolder+r'/L5034032_2002_B4.tif',\
            subfolder+r'/L5034032_2003_B3.tif', subfolder+r'/L5034032_2003_B4.tif',\
            subfolder+r'/L5034032_2004_B3.tif', subfolder+r'/L5034032_2004_B4.tif',\
            subfolder+r'/L5034032_2005_B3.tif', subfolder+r'/L5034032_2005_B4.tif',\
            subfolder+r'/L5034032_2006_B3.tif', subfolder+r'/L5034032_2006_B4.tif',\
            subfolder+r'/L5034032_2007_B3.tif', subfolder+r'/L5034032_2007_B4.tif',\
            subfolder+r'/L5034032_2008_B3.tif', subfolder+r'/L5034032_2008_B4.tif',\
            subfolder+r'/L5034032_2009_B3.tif', subfolder+r'/L5034032_2009_B4.tif',\
            subfolder+r'/L5034032_2010_B3.tif', subfolder+r'/L5034032_2010_B4.tif',\
            subfolder+r'/L5034032_2011_B3.tif', subfolder+r'/L5034032_2011_B4.tif']

#Functions
def ZonalStatsTable(zoneArray, valueArray, outName):
    '''
    Create a Pandas DataFrame of zonal statistics for a given zone. 
    Exports DataFrame to a csv file.
    
    :param zoneArray: 
    :param valueArray: numpy array 
    :param outName: pathname that the output csv will go under.
    :return: pandas DataFrame
    ''' 
    zoneIndex = np.unique(zoneArray[~np.isnan(zoneArray)])
    mins = []
    maxs = []
    means =[]
    stddevs = []
    counts = []   
    
    for i in zoneIndex:
         mins.append(np.min(valueArray[zoneArray==i]))
         maxs.append(np.max(valueArray[zoneArray==i]))
         means.append(np.mean(valueArray[zoneArray==i]))
         stddevs.append(np.std(valueArray[zoneArray==i]))
         counts.append(np.size(valueArray[zoneArray==i]))
        
    d = {
         'zone': zoneIndex,
         'min': mins,
         'max': maxs,
         'mean': means,
         'stddev': stddevs,
         'count': counts
         } 
    
    df = pd.DataFrame(d)
    df.head()
    df.to_csv(outName)
    return df
    #gjm: You should return None based on how you call this function below. You don't actually want to get anything out of the function in memory.

#gjm: very well done!

def mask_ndarray(inputArray, maskArray):
    '''
    Masks an array based on a boolean array of the same shape.
    :param input3D: 3D array representing values you would like masked.
    :param mask_3D: a boolean 3D array representing desired mask. Must have same shape as input and correspond geographically.
    :return masked_3D: 3D array of np.nan where mask array is False and input values where mask array is true.
    '''
    subset = inputArray[maskArray]
    emptyArray = np.zeros_like(inputArray, dtype=np.float32)
    emptyArray[emptyArray == 0] = np.nan
    emptyArray[maskArray] = subset
    outputArray = emptyArray
    return outputArray
#gjm: good.

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   PART I   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#getting slope and aspect arrays
demGdal = gdal.Open(demName,gdalconst.GA_ReadOnly)
demArray = demGdal.GetRasterBand(1).ReadAsArray()
slope, aspect = slopeAspect(demArray, 30)
reSlope = reclassByHisto(slope, 10)
reAspect = reclassAspect(aspect)
#gjm: good.

#Band 3 stacking
b3Arrays = []
for i in range(0,len(landsats),2):
    b3Array = gdalnumeric.LoadFile(landsats[i])
    b3Arrays.append(b3Array)
band3_3D = np.dstack(b3Arrays)

#Band 4 stacking
b4Arrays = []
for i in range(1,len(landsats),2):
    b4Array = gdalnumeric.LoadFile(landsats[i])
    b4Arrays.append(b4Array)
band4_3D = np.dstack(b4Arrays)

#fire perimeter stacking
mask = gdalnumeric.LoadFile('fire_perimeter.tif')
masks = []
for i in range(10):
    masks.append(mask)
len(masks)
mask_3D = np.dstack(masks)

#Mask boolean arrays
burned_areas_bool = mask_3D == 1
healthy_areas_bool = mask_3D == 2

#Calculations
NDVI_3D = (band4_3D - band3_3D)/(band4_3D + band3_3D)
NDVI_3D_burned = mask_ndarray(NDVI_3D, burned_areas_bool)
NDVI_3D_healthy = mask_ndarray(NDVI_3D, healthy_areas_bool)

RR_3D = np.zeros_like(NDVI_3D_healthy,dtype=np.float32)
for i in range(mask_3D.shape[2]):
    RR_3D[:,:,i] = NDVI_3D_burned[:,:,i]/(np.nanmean(NDVI_3D_healthy[:,:,i]))
    print "In " + str(range(2002,2012)[i]) + ", the mean recovery ratio was: " + str(np.nanmean(RR_3D[:,:,i]))
    
CR = np.zeros_like(RR_3D[:,:,i],dtype=np.float32)
for row in range(RR_3D.shape[0]):
    for col in range(RR_3D.shape[1]):
        if np.all(np.isfinite(RR_3D[row,col,:])):
            CR[row, col] = np.polyfit(range(2002,2012), RR_3D[row,col,:], 1)[0]
        else:
            #CR[row, col] = np.nan
            pass
print "The average coefficient of recovery for burned areas across all the years was: " + str(np.nanmean(CR))
#gjm: Very well done! good work with the 3D arrays.

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   PART II   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#mask slope and aspect
reSlopeMask = mask_ndarray(reSlope, mask==1)
reAspectMask = mask_ndarray(reAspect, mask==1)

#Perform Zonal Stats
ZonalStatsTable(reSlopeMask, CR, path + r'/Zonal_Statistics_Slope.csv')
ZonalStatsTable(reAspectMask, CR, path + r'/Zonal_Statistics_Aspect.csv')

#Writing out Final Geotif
demGdal = gdal.Open(demName,gdalconst.GA_ReadOnly)
driver = demGdal.GetDriver()
driver.Register()

outFile = driver.Create('CR_BurnedArea.tif',CR.shape[1],CR.shape[0],1,gdal.GDT_Float32)
outFile.GetRasterBand(1).WriteArray(CR)
outFile.GetRasterBand(1).ComputeStatistics(False)
outFile.SetGeoTransform(demGdal.GetGeoTransform())
outFile.SetProjection(demGdal.GetProjection())

#delete datasources
del demGdal, outFile

print '''
Conclusions:

There seems to be a higher mean coefficient of recovery for Northwestern, Northern and Northeastern aspects with ~.03. Compare this to ~.01 for southern aspects.

Additionally, There seems to be a slightly higher mean coefficent of recovery for more level slopes (lower with ~.02. Compare this to ~.01 for steeper slopes (higher degree slopes).
'''
#gjm: Excellent solution, very well done!






























#1st Try:
##~~~~~~~~~~~~~~~~~~GETTING NDVI CALCULATIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#t0 = time.clock()
#
##Band 3 stacking
#b3Arrays = []
#for i in range(0,len(landsats),2):
#    b3Array = gdalnumeric.LoadFile(landsats[i])
#    b3Arrays.append(b3Array)
#b3stack = np.dstack(b3Arrays)
#b3stackTran = b3stack.transpose((2,0,1))
#
##Band 4 stacking
#b4Arrays = []
#for i in range(1,len(landsats),2):
#    b4Array = gdalnumeric.LoadFile(landsats[i])
#    b4Arrays.append(b4Array)
#b4stack = np.dstack(b4Arrays)
#b4stackTran = b4stack.transpose((2,0,1))
#
##Empty 3D Arrays for use in loop.
#NDVI_3D = np.zeros_like(b3stackTran) 
#RR = np.zeros_like(b3stackTran) 
#CR = np.zeros_like(b3stackTran[0])
#
##Create Mask for use in analysis
#mask = gdalnumeric.LoadFile('fire_perimeter.tif')
#masks = []
#for i in range(10):
#    masks.append(mask)
#len(masks)
#maskStack = np.dstack(masks)
#maskStackTran = maskStack.transpose((2,0,1))
#years = [2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012]
#
##Calculate NDVI, and RR
#for i in range(len(b3stackTran)):
#    NDVI_3D[i] = (b4stackTran[i] - b3stackTran[i])/(b4stackTran[i] + b3stackTran[i])
#    #QUESTION: I seem to have gotten the right answers but, is the numerator below supposed to be NDVI of only burned area??
#    RR[i] = NDVI_3D[i]/(np.mean(NDVI_3D[i][maskStackTran[i]==2]))
#    print "In " + str(years[i]) + ", the mean recovery ratio was: " + str(np.mean(RR[i][maskStackTran[0]==1]))
#
##Calculate CR
#for row in range(RR[0].shape[0]):
#    for col in range(RR[0].shape[1]):
#        #pdb.set_trace()
#        #QUESTION: I still might be having the problem of pdb.set_trace showing me a "RR[:,row,col]" slice that has one value in the front, and the rest zeros. How to test if answers are correct??
#        CR[row, col] = np.polyfit(range(2002,2012), RR[:,row,col], 1)[0]
#  
##Print statements      
#print "The average coefficient of recovery across all the years was: " + str(np.mean(CR[maskStackTran[0]==1]))   
#
#print time.clock(), "seconds process time"
#
#
#plt.imshow(CR)
#
#
#RR.shape
#RR = RR.transpose((2,0,1))
#RR.shape


















































#
#NDVI_3D.shape
#RR.shape
#RR = RR.transpose((2,0,1))
#RR.shape
#
#RR.shape
#NDVI_3D.shape
#maskStackTran.shape
#b3stackTran.shape
#b4stackTran.shape
#
##visualization:
#plt.imshow(maskStackTran[0])
#plt.imshow(maskStackTran[1])
#plt.imshow(maskStackTran[2])
#plt.imshow(RR[0])
#plt.imshow(RR[1])
#plt.imshow(RR[2])
#plt.imshow(RR[3])
#plt.imshow(RR[4])
#plt.imshow(RR[5])
#plt.imshow(RR[6])
#plt.imshow(RR[7])
#plt.imshow(RR[8])
#plt.imshow(RR[9])
#plt.imshow(NDVI_3D[0])
#plt.imshow(NDVI_3D[1])
#plt.imshow(NDVI_3D[2])
#plt.imshow(NDVI_3D[3])
#plt.imshow(NDVI_3D[4])
#plt.imshow(NDVI_3D[5])
#plt.imshow(NDVI_3D[6])
#plt.imshow(NDVI_3D[7])
#plt.imshow(NDVI_3D[8])
#plt.imshow(NDVI_3D[9])
#
#test = CR == RR[0]
#test

##Different attempt at it 3d vectorization:
#for i in range(len(b3stackTran)):
#    NDVI_3D[i] = (b4stackTran[i] - b3stackTran[i])/(b4stackTran[i] + b3stackTran[i])
#NDVI_3D.shape
#
#for i in range(len(b3stackTran)):
#    RR[i] = NDVI_3D[i]/(np.mean(NDVI_3D[i][maskStackTran[i]==2]))
#RR.shape

##Test NDVI CALC FOR 1 YEAR:
#b3 = gdalnumeric.LoadFile(landsats[0])
#b4 = gdalnumeric.LoadFile(landsats[1])
#
#NDVI = (b4-b3)/(b4+b3)
#NDVI.shape
#plt.imshow(NDVI)

#Test NDVI CALC 3D VECTORIZATION?: This failed somehow. I think it has to do with the order that CR is being iterated through in thelast nested loop.
#b3stack.shape
#b3stackTran = b3stack.transpose((2,0,1))
#b3stackTran.shape
#b4stack.shape
#b4stackTran = b4stack.transpose((2,0,1))
#b4stackTran.shape
#NDVI_3D = np.zeros_like(b3stackTran) 
#NDVI_3D.shape
#RR = np.zeros_like(b3stackTran) 
#RR.shape
#CR = np.zeros_like(b3stackTran[0]) 
#CR.shape
#mask = gdalnumeric.LoadFile('fire_perimeter.tif')
#masks = []
#for i in range(10):
#    masks.append(mask)
#len(masks)
#maskStack = np.dstack(masks)
#maskStack.shape
#maskStackTran = maskStack.transpose((2,0,1))
#maskStackTran.shape
##why does this iterate over the z-dimension??
#for i in range(len(b3stackTran)):
#    NDVI_3D[i] = (b4stackTran[i] - b3stackTran[i])/(b4stackTran[i] + b3stackTran[i])
#    RR[i] = NDVI_3D[i]/(np.mean(NDVI_3D[i][maskStackTran[i]==2]))
#    #CR = np.polyfit(range(2002,20012), RR[:,,], 1)
#
##output of this will be single array
##I don't fully understand the 3D vectorization yet; why did transposing it make the loop run off the Z axis? because it iterates on the 1st dimension in the list! 
##stepping back down from 3D to 2D! Fucking hard@@!!!
#    for row in range(len(b3stackTran[1])):
#        for col in range(len(b3stackTran[2])):
#            #pdb.set_trace()
#            CR = np.polyfit(range(2002,20012), RR[:,row,col,], 1)
#    print np.mean(RR[i])
#print np.mean(CR)   