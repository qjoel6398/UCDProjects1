# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 21:42:13 2017

@author: minifast026
"""

import pandas as pd
import requests

"""
# * http://docs.python-requests.org/en/latest/
# * https://developers.google.com/maps/

This Geocoding script is designed to geocode many addresses using google APIs. Attempts address geocoder first, and then attempts google places.  Also returns a column called 'cert' -for "Certainty"- which is the number of results google retured for a given intersection.

A typical google places request with intersections looks like this:
https://maps.googleapis.com/maps/api/place/textsearch/json?query=Lakewood:Florida+and+Kipling&key=XXX

-status_codes is used to identify why the API had a problem geocoding a specific result.

-Must replace 'KEY' with your own Google API Key.

-Change file paths to your own directories.
"""


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
                print "Error thrown at address number" + str(i) + ","
    status_codes
        
    df['Latitude'] = lats
    df['Longitude'] = lons
    df['Uncertainty'] = certs    
    df.head
    return df, status_codes

#OUTPUT DATAFRAME
df = pd.read_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 pandas.csv')
KEY = 'XXX'
geo_df = googleGeocoder(df, KEY)
geo_df[0].to_csv(r'C:\Users\minifast026\Desktop\GEOCODING PROJECT\User dump for quin 20170920 pandas geo.csv')


