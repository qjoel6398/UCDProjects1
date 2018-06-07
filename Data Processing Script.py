# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 14:17:57 2018

@author: Qadmin
"""

#1. Get headings and imports from Galen's scripts
import arcpy
import os
from arcpy import env
from arcpy.sa import *
#os.listdir(env.workspace)
arcpy.CheckOutExtension('Spatial')
env.workspace = r'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\Quin Data\Raw Data\RawRasters'
env.overwriteOutput = 1

sr = arcpy.SpatialReference  (102254)


l=arcpy.ListDatasets()
print l
Rasters = []

treRast = arcpy.Raster(l[0])
impRast = arcpy.Raster(l[1])
lcrRast = arcpy.Raster(l[2])

arcpy.ProjectRaster_management (treRast, "treRast_proj", sr)
arcpy.ProjectRaster_management (impRast, "impRast_proj", sr)
arcpy.ProjectRaster_management (lcrRast, "lcrRast_proj", sr)

canopy_pc = arcpy.sa.ExtractByMask ("treRast_proj", "C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb\State_v01")
imperv_pc = arcpy.sa.ExtractByMask ("impRast_proj", "C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb\State_v01")
landcov_pc = arcpy.sa.ExtractByMask ("lcrRast_proj", "C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb\State_v01")
print "extractions done!"
#2. Vector Processing Workflow

def Projectandclipvector(invectorfile):
#    Project_management (vectorfile, vectorfile+"_proj", 'NAD_1983_HARN_StatePlane_Colorado_Central_FIPS_0502', {transform_method}, {in_coor_system})
    projectedvector = arcpy.Project_management(invectorfile, "tempclip", sr)
    PC_vector = arcpy.Clip_analysis ("tempclip", "C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb\State_v01", invectorfile+"_pc")
    return PC_vector

CensusBlock = 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\Quin Data\Raw Data\Census\ACS_2015_5YR_BG_08_COLORADO.gdb\ACS_2015_5YR_BG_08_COLORADO'
CensusCountysub = 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\Quin Data\Raw Data\Census\ACS_2015_5YR_COUSUB_08_COLORADO.gdb\ACS_2015_5YR_COUSUB_08_COLORADO'
CensusTract = 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\Quin Data\Raw Data\Census\ACS_2015_5YR_TRACT_08_COLORADO.gdb\ACS_2015_5YR_TRACT_08_COLORADO'

CensusBlock_pc = Projectandclipvector(CensusBlock)
CensusCountysub_pc = Projectandclipvector(CensusCounty)
CensusTract_pc = Projectandclipvector(CensusTract)

print "Projectandclipvector done!"


arcpy.RasterToGeodatabase_conversion (canopy_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')
arcpy.RasterToGeodatabase_conversion (imperv_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')
arcpy.RasterToGeodatabase_conversion (landcov_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')

print "RasterToGeodatabase done!"

arcpy.FeatureClassToGeodatabase_conversion (CensusBlock_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')
arcpy.FeatureClassToGeodatabase_conversion (CensusCounty_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')
arcpy.FeatureClassToGeodatabase_conversion (CensusTract_pc, 'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Bee GIS\BGIS01.gdb')

print "FeatureClassToGeodatabase done!"


#pc means projected and clipped



#4. File delivery and use of above functions
IMAGERY (RASTER) 

IMPERMEABLE SURFACE (RASTER)
TREES (RASTER)
LANDCOVER (RASTER)

CENSUS (VECTOR)

Step 2 - Project
Step 3 - Clip

#5. Finish documenting all data and creating map/geodatabase  
#6. Is all your Data appropriate?
#    Best Land use set? Ask Peter
#    Best Imagery set? Ask Peter
    