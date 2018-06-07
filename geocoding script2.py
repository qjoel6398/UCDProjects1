# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:13:40 2017

@author: Qadmin
"""
import pandas as pd
import requests


#https://maps.googleapis.com/maps/api/place/textsearch/json?query=Lakewood:  Florida and Kipling&key=AIzaSyBu_iOY2Ty5mKhC3K5DslUSX7R6i7rZOPI


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

#BEEKEEPING SURVEY DATA
df = pd.read_csv(r'C:\Users\Default\Desktop\MultipleSites_Invalid1.csv')
df.head
KEY = 'AIzaSyBu_iOY2Ty5mKhC3K5DslUSX7R6i7rZOPI'
#New Columns
geo_df = googleGeocoder(df, KEY)
geo_df[0].to_csv(r'C:\Users\Default\Desktop\Beekeeping_Survey_Spatial_V02_MultiInv1.csv')









df.Intersection





df['Intersection','cubee_id']


s = df.Intersection.str.len().sort_values().index
df_1 = df.reindex(s)



subset = df_1.cubee_id,df_1.Intersection
subset

"""subset
The following function joins all the survey counties into one column (EXCEL)
    =CONCATENATE(N3,O3,P3,Q3,R3,S3,T3,U3,V3,W3,X3,Y3)

Resulting column for county is:
    [ConcatCounty]

Column for intersection:
    ['Please specify the street intersection (with the city or town) nearest to your bee hive(s).\xc2\xa0 If you are maintaining hives at multiple locations, please specify the nearest street intersection to each. This information will never be available to the public.']

Need to find the column you want?:
    Specificstring_cols = [col for col in df.columns if 'specific string' in col]
    print(list(df.columns))
    print(intersection_cols)
"""


