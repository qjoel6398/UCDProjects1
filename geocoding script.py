# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:13:40 2017

@author: Qadmin
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
            response = requests.get(GOOGLE_PLACES_URL + 'query=' + df['Intersection'][i] + "Colorado" + '&' + 'key=' + KEY)
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
#    status_codes
        
    df['Latitude'] = lats
    df['Longitude'] = lons
    df['Uncertainty'] = certs    
    return df, status_codes

#BEEKEEPING SURVEY DATA
df = pd.read_csv(r'C:\Users\Qadmin\Downloads\Beekeeping_Survey_V02.csv')
df.head
KEY = 'AIzaSyAoaDu72f9e0ze-8hFYoZ37pVM8Ia_BGgA'
#New Columns
df['StudyID'] = pd.Series(range(25))
geo_df = googleGeocoder(df, KEY)
geo_df[0].to_csv(r'C:\Users\Default\Desktop\Beekeeping_Survey_Spatial_V02.csv')



"""
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


