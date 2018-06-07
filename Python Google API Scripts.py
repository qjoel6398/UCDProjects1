# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 21:42:13 2017

@author: minifast026
"""

import pandas as pd
import requests

#
# * http://docs.python-requests.org/en/latest/
# * https://developers.google.com/maps/


def googleGeocoder(df, KEY):
    GOOGLE_GEOCODER_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
    GOOGLE_PLACES_URL ='https://maps.googleapis.com/maps/api/place/textsearch/json?'
    lats = []
    lons = []
    certs = []
    status_codes = {}

    for i in range(len(df['Address1'])):

        try:
            response = requests.get(GOOGLE_GEOCODER_URL + 'address=' + df['Address1'][i] + '&' + 'key=' + KEY)
            json = response.json()
            results = json['results'][0]

            lat = results['geometry']['location']['lat']
            lon = results['geometry']['location']['lng']
            lats.append(lat)
            lons.append(lon)
            certs.append(len(json['results']))

        except:
            try:
                response = requests.get(GOOGLE_PLACES_URL + 'query=' + df['Address1'][i] + '&' + 'key=' + KEY)
                json = response.json()
                results = json['results'][0]
    
                lat = results['geometry']['location']['lat']
                lon = results['geometry']['location']['lng']
                lats.append(lat)
                lons.append(lon)
                certs.append(len(json['results']))

            except:
                lats.append(None)
                lons.append(None)
                certs.append(None)
                status_codes[i] = response.status_code
                print "Error thrown at address number" + str(i) + ", Muthafucka!!!"
    status_codes
        
    df['Latitude'] = lats
    df['Longitude'] = lons
    df['Uncertainty'] = certs    
    df.head
    return df, status_codes

#The Data Frame
df = pd.read_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 pandas.csv')
KEY = 'AIzaSyAoaDu72f9e0ze-8hFYoZ37pVM8Ia_BGgA'
geo_df = googleGeocoder(df, KEY)
geo_df[0].to_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 pandas geo.csv')







#Process:
import arcpy
from arcpy import env 
#import os
env.workspace = r'\\ifast\iUniversity\joelq\Desktop\GEOCODING PROJECT\GEOCODING PROJECT.gdb'
env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")
env.qualifiedFieldNames = "UNQUALIFIED"

l = arcpy.ListFeatureClasses() 
print l

def mc_dd_creation(featureclass):
    """
    creates mean center and directional distribution feature class for each selection in a feature class
    """
    arcpy.FeatureClassToFeatureClass_conversion (featureclass, env.workspace, featureclass+"_TT", "TT_Graduate = 1")
    arcpy.FeatureClassToFeatureClass_conversion (featureclass, env.workspace, featureclass+"_DT", "DT_Graduate = 1")
    arcpy.FeatureClassToFeatureClass_conversion (featureclass, env.workspace, featureclass+"_CT", "CT_Graduate = 1")
    arcpy.MeanCenter_stats(featureclass+"_TT",featureclass+"_TT"+"_MC")
    arcpy.DirectionalDistribution_stats (featureclass+"_TT", featureclass+"_TT"+"_DD", "1_STANDARD_DEVIATION")    
    arcpy.MeanCenter_stats(featureclass+"_DT",featureclass+"_DT"+"_MC")
    arcpy.DirectionalDistribution_stats (featureclass+"_DT", featureclass+"_DT"+"_DD", "1_STANDARD_DEVIATION")
    arcpy.MeanCenter_stats(featureclass+"_CT",featureclass+"_CT"+"_MC")
    arcpy.DirectionalDistribution_stats (featureclass+"_CT", featureclass+"_CT"+"_DD", "1_STANDARD_DEVIATION")
    return

mc_dd_creation(l[3])
mc_dd_creation(l[4])
mc_dd_creation(l[5])










#
#
#
#
#
#
#
#countries = {}
#df1 = pd.read_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 Countries.csv', names= ['Country','Address1'])
#df1.head
#KEY = 'AIzaSyAoaDu72f9e0ze-8hFYoZ37pVM8Ia_BGgA'
#
#shortnames = []
#formats = []
#for i,el in enumerate(df1['Address1']):
#    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
#    try: 
#        response = requests.get(GOOGLE_MAPS_API_URL + 'address=' + str(el) + '&key=' + KEY)
#        json = response.json()
#        results = json['results'][0]
#        shortnames.append(results["address_components"]["short_name"])
#        formats.append(results["formatted_address"])
#        print "OK"
#    except:
#        #print "Error thrown at address number " + str(i) + ", Muthafucka!!!"
#        shortnames.append(df1['Address1'][0][-2:])
#        formats.append(None)
#        print "NO"
#
#countries['shortnames']=shortnames
#countries['formats']=formats
#
#df1 = pd.DataFrame(countries)
#df1
#
##THIS CODE ATTEMPTS TO TROUBLESHOOT USING ONE REQUEST AT A TIME. THIS ONE WORKS, BUT THE LOOP ABOVE DOESN'T
#import pandas as pd
#import requests
#
#countries = {}
#df1 = pd.read_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 Countries.csv', names= ['Country','Address1'])
#df1.head
#GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
#KEY = 'AIzaSyAoaDu72f9e0ze-8hFYoZ37pVM8Ia_BGgA'
#for i,el in enumerate(df1['Address1']):
#    response = requests.get(GOOGLE_MAPS_API_URL + 'address=' + el  + '&key=' + KEY)
#    json = response.json()
#    json
##    results = json['results'][0]
##    print results["formatted_address"]
##    print results["address_components"][5]["short_name"]
##    countries[tuple(df1['Address1'][0][-2:])] = None