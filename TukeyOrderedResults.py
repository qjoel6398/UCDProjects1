# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

tk = pd.read_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\TukeyResults.csv')
seg = pd.read_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\orderedmeans.csv')
seg = seg.sort_values(by="mean", axis=0, ascending=False, inplace=False)


#ltk = list(tk["Unnamed: 0"])
#
#tkList = []
#for i in tk["Unnamed: 0"]:
#    tkList.append(i.split("-"))


segList = []
lseg = list(seg["TSEGNAME"])
for i in range((len(lseg))-1):
    segList.append(str(lseg[i]+'-'+lseg[i+1]))
    


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

        
tk2
#k=[0,1,2,3]        
#for i in range(len(k)):
#    k[i]=9
#k  
#    

#list(segList[1].split("-").reverse())    
#
#elif i.split("-").reverse() in segList:
#    segbool.append(True)
#        
#x = i.split("-")
#x.reverse()
#x = str(x[0]+'-'+x[1])
#x    
#        
#segList[1]       
#list(segList[1].split("-").reverse())    
#segList[1]    
    

#subset tukey dataframe by single,ordered matches. But now they are not in order 
tk2.to_csv(r'C:\Users\qjoel\OneDrive\Desktop\GEOM\R\tk2.csv')

for i in range(len(list(tk2["Unnamed: 0"]))):
    tk2["Unnamed: 0"][i]=list(tk2["Unnamed: 0"]).split("-")[0]
    