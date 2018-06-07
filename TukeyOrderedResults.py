# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
This script was made to process the results of a pairwaise ANOVA comparison (Tukey Test). This data was output from RStudio into CSV form. Out of over 2200 parwise comparisons, I wanted only the ones who's means were adjacent in order. In effect, I wanted an ordered list of pairwise p-values.
"""

import pandas as pd
import numpy as np

#dataframe of 2244 pairwise comparisons:
tk = pd.read_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\TukeyResults.csv')

#dataframe of 67 means corresponding with groups (Tapestry segments):
seg = pd.read_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\orderedmeans.csv')

#Sort groups by mean
seg = seg.sort_values(by="mean", axis=0, ascending=False, inplace=False)

#Create reference list of adjacent group names in the format "group 1 - group 2". This is the same format that the pairwise comparisons are in.
segList = []
lseg = list(seg["TSEGNAME"])
for i in range((len(lseg))-1):
    segList.append(str(lseg[i]+'-'+lseg[i+1]))
    
    

#Entire list of pairwise comparisons are now compared to the previous reference list - extracting only those that are identical. This will extract the P-values associated as well.
segbool = []           
for i in range(len(tk["Unnamed: 0"])):      
    x = tk["Unnamed: 0"][i].split("-")
    x = str(x[1]+'-'+x[0])
    if tk["Unnamed: 0"][i] in segList:
        segbool.append(True)
    elif x in segList:   
        segbool.append(True)
        tk["Unnamed: 0"][i]=x
    else:
        segbool.append(False)        
tk2 = tk[np.array(segbool)]

#Write data to output.
tk2.to_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\tk2.csv')
