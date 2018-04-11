# -*- coding: utf-8 -*-
"""
The script calculates temperature difference between Sodankyla and Helsinki stations.
Calculates mean value and standard deviation for summer temperatures for both stations.

@author: Pavel
"""
# Import pandas
import pandas as pd

# Import monthly data of Helsinki station
from temperature_anomalies import monthlyData as monthlyDataHel, monthes_dictionary as monthes_dictionary

# Read datafile
data = pd.read_csv("1308661.txt", sep="\s+", names=['STATION','STATION_NAME','STATION_NAME_1','STATION_NAME_2','ELEVATION','LATITUDE','LONGITUDE','DATE','PRCP','TMAX','TMIN'], skiprows=2, na_values=['-9999'])

# Merge station name to single column
data['STATION_NAME'] = data['STATION_NAME'] + ' ' + data['STATION_NAME_1'] + ' ' + data['STATION_NAME_2'] 

# Drop unnecessary columns
data = data.drop(['STATION_NAME_1','STATION_NAME_2'],axis=1)

# Calculate average temperature
data['TAVG'] = data[['TMAX','TMIN']].mean(axis=1,skipna=False)

# The function converts temperature from Fahrenheit to Celsius
def fahrenheitToCelsius(fahr_temp):
    converted_temp = (fahr_temp - 32) / 1.8
    return converted_temp
    
# Create year-month, month columns
data['YM'] = (data['DATE'].astype(str)).str.slice(start=0,stop=6)
data['monthNumber'] = (data['DATE'].astype(str)).str.slice(start=4,stop=6)

# Convert temperatures to Celsius
data['TAVG_Celsius'] = fahrenheitToCelsius(data['TAVG'])

# Create empty Dataframe
monthlyData = pd.DataFrame()

# Group Dataframe
grouped_month = data.groupby('YM')

# Aggregate data
for key, group in grouped_month:
    mean_value = group[['TAVG_Celsius']].mean()
    mean_value['YM'] = key
    mean_value['monthNumber'] = key[4:6]
    monthlyData = monthlyData.append(mean_value, ignore_index=True)
    
# Reorder columns
monthlyData = monthlyData[['YM','monthNumber','TAVG_Celsius']]

# Create empty Dataframe
referenceTemps = pd.DataFrame()

# Group by month
grouped_data = data.groupby('monthNumber')

# Iterate groups
for key, group in grouped_data:
    row = group[['TAVG_Celsius']].mean()
    row['monthNumber'] = key
    referenceTemps = referenceTemps.append(row,ignore_index=True)
    
# Rename columns
referenceTemps = referenceTemps.rename(columns={'TAVG_Celsius':'avgTempsC'})
    
# Merge with dictionary
referenceTemps = referenceTemps.merge(monthes_dictionary,on='monthNumber')

# Join monthlyData and referenceTemps
monthlyData = monthlyData.merge(referenceTemps,how='left', on='monthNumber',sort=False)

# Compare temperatures
monthlyData['Diff'] = monthlyData['TAVG_Celsius'] - monthlyData['avgTempsC']

# Merge monthly temperatures in Sodankyla Lokka and Helsinki
monthlyData = monthlyData.merge(monthlyDataHel,how='inner', on='YM',sort=False)

# Colculate difference 
monthlyData['Diff_SodHel'] = monthlyData['TAVG_Celsius_x'] - monthlyData['TAVG_Celsius_y']

# Choose summer temperatures
summer = monthlyData.ix[(monthlyData['monthNumber_x'] == '06') | (monthlyData['monthNumber_x'] == '07') | (monthlyData['monthNumber_x'] == '08')]

# Output summer temperatures to csv
summer.to_csv("Summer_SodHel.csv", sep=',', index=False, float_format='%.3f')

# Calculate mean summer temperatures for Sodankyla Lokka station
meanSummerSod = summer['TAVG_Celsius_x'].mean()

# Calculate mean summer temperatures for Helsinki station
meanSummerHel = summer['TAVG_Celsius_y'].mean()

# Calculate std summer temperatures for Sodankyla Lokka station
stdSummerSod = summer['TAVG_Celsius_x'].std()

# Calculate std summer temperatures for Helsinki station
stdSummerHel = summer['TAVG_Celsius_y'].std()


