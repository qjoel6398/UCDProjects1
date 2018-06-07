# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:13:40 2017

@author: Qadmin
"""


"""
For more information on the CU Denver Varroa Mite Project, visit: http://cuurbanbee.businesscatalyst.com/cu-beekeeping-survey.html
For our Urban Beekeeping survey, users were asked to submit the major intersection that is closest to their beehives. This script attempts to find the lat/long coordinates corresponding to those intersections and merges them into the beekeeper survey results table. Also returns a column called cert -for "Certainty"- which is the number of results google retured for a given intersection.

A typical google places request with intersections looks like this:
https://maps.googleapis.com/maps/api/place/textsearch/json?query=Lakewood:Florida+and+Kipling&key=XXX

-status_codes is used to identify why a the API had a problem geocoding a specific result.

-Must Replace 'KEY' with your own Google API Key.

-Change file paths to your directories.
"""

import pandas as pd
import requests

def googleGeocoder(df, KEY):
    

    GOOGLE_PLACES_URL ='https://maps.googleapis.com/maps/api/place/textsearch/json?'
#Empty lists to populate dataframe columns
    lats = []
    lons = []
    certs = []
    status_codes = {}

    
    for i in range(len(df['Intersection'])):
        try:
            response = requests.get(GOOGLE_PLACES_URL + 'query=' + df['Intersection'][i]+'&' + 'key=' + KEY)
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
            print "Error thrown for " + "[" + str(df['Intersection'][i]) + "]" + "!"
    status_codes
    df['Latitude'] = lats
    df['Longitude'] = lons
    df['Uncertainty'] = certs    
    return df, status_codes

#INPUT DATA
df = pd.read_csv(r'C:\Users\Default\Desktop\MultipleSites_Invalid1.csv')
KEY = 'XXX'

#OUTPUT DATA
geo_df = googleGeocoder(df, KEY)
geo_df[0].to_csv(r'C:\Users\Default\Desktop\Beekeeping_Survey_Spatial_V02_MultiInv1.csv')




