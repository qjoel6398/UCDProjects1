# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 20:45:05 2018

@author: Qadmin
"""

import pandas as pd
import requests
import time

names = []
emails = []
states = []
counties = []
conditions = []
purposes = []

Total_records = 51795-20618
for i in range(20618,51795):
    try:
        response = requests.get('https://co.beecheck.org/api/specialty_sites/'+str(i))
        json = response.json()
        names.append(json['contact']['name'])
        emails.append(json['contact']['email'])
        states.append(json['statename'])
        counties.append(json['county'])
        conditions.append(json['growing_condition_name'])
        purposes.append(json['purpose_of_bees'])
    except:
        pass

d = {"Name": names,"Email": emails,"State": states,"County": counties,"Growing Condition": conditions, "Purpose of bees": purposes}
df = pd.DataFrame(d)
df.to_csv(r'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Survey Analysis (R)\BeeCheckEmailList.csv')


subset = df['State'] == 'Colorado'
ColoradoDf = df[subset]
ColoradoDf = ColoradoDf.drop_duplicates()
ColoradoDf.to_csv(r'C:\Users\Qadmin\Desktop\Varroa Mite Project Research\Survey Analysis (R)\BeeCheckEmailList.csv')



##DELAY:
##If you want to be polite and not overwhelm the target site you’re scraping, 
##you can introduce an intentional delay or lag in your scraper to slow it down
#
#for term in ["web scraping", "web crawling", "scrape this site"]:
#    r = requests.get("http://example.com/search", params=dict(
#        query=term
#    ))
#    time.sleep(5)  # wait 5 seconds before we make the next request
#   



##BACKOFF
##Some also recommend adding a backoff that’s proportional to how long the site took to respond to your request. 
##That way if the site gets overwhelmed and starts to slow down, your code will automatically back off.
#
#for term in ["web scraping", "web crawling", "scrape this site"]:
#    t0 = time.time()
#    r = requests.get("http://example.com/search", params=dict(
#        query=term
#    ))
#    response_delay = time.time() - t0
#    time.sleep(10*response_delay)  # wait 10x longer than it took them to respond
