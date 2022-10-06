# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 16:00:35 2022

@author: soxst
"""

import pandas as pd
df = pd.read_csv("eplusout.csv")
asd = {}
asb = {}
date = pd.DataFrame({'date':list(df['Date/Time'])})
#estrarre colonne del dataframe che ci interessano: la selezione viene effettuata tramite
#ispezione delle stringhe per parole chiave
for col in df.columns:
    asd[col] = 0
    col_split = col.split()
    split_0 = col_split[0].split(':')
    flag_1 = ('MAINXFIRST'in split_0) or ('MAINGROUND'in split_0) or ('ROOF' in split_0)
    flag_2 = ('Temperature'in col_split) and ('Air' in col_split) and ('[C](Hourly)' in col_split)
    if flag_1  and flag_2:
        asb[col] = list(df[col])
        
keys = list(asb.keys())
mean_temp = []
mean_power = []
#calcolare la media per singola ora annuale tra tutte le zone d'interesse
for i in range(len(asb[keys[0]])):
    mean = 0
    for key in keys:
        mean += asb[key][i]
    mean = mean/len(keys)
    mean_temp.append(mean)
    mean_power.append((df['Electricity:Facility [J](Hourly)'][i]+df['DistrictCooling:Facility [J](Hourly)'][i]+df['DistrictHeating:Facility [J](Hourly)'][i])/3)
    
date.insert(1, "Temperature_in", mean_temp)
date.insert(2, "Power", mean_power)
df_average_out_temp = pd.read_csv("averagedOverHourAndYearsTemperatures.csv")

for i in range(1416,1440):
    df_average_out_temp=df_average_out_temp.drop(i)
date.insert(2, "Temperature_out", df_average_out_temp['Temperature_C'])
date = date.set_index(df_average_out_temp['Date_Time'])
date = date.drop(columns = ['date'])
#date = date.set_index('date')
path = "C:\\Users\\soxst\\Desktop\\hourly_mean.csv"
date.to_csv(path)
    