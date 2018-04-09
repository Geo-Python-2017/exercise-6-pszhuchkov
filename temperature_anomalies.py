# -*- coding: utf-8 -*-
"""
The script uses climate data from the Helsinki-Vantaa airport station.
The data contains daily observations obtained from the NOAA Global Historical Climatology Network. 
The scripts outputs the number of non-NaN values for average and minimum temperature, 
the total number of observation days, the first and last observations, average temperature
for whole file and maximum temperatures for summer of 1969. 

@author: Pavel
"""
# Import pandas
import pandas as pd

# Reading file
data = pd.read_csv("1091402.txt", sep='\s+', skiprows=[1], na_values=['-9999'])

# How many non-NaN values are there for TAVG?
numb_tavg = data.ix[data['TAVG']==data['TAVG']]
print('The number of non-NaN values for TAVG is', len(numb_tavg))

# What about for TMIN?
numb_tmin = data.ix[data['TMIN']==data['TMIN']]
print('The number of non-NaN values for TMIN is', len(numb_tmin))

# How many days total are covered by this data file?
unique_date = data['DATE'].unique()
print('The total number of days is', len(unique_date))

# When is the first observation?
first_obser = data['DATE'].min()
print('The first observation is', first_obser)

# When is the last?
last_obser = data['DATE'].max()
print('The last observation is', last_obser)

# What was the average temperature of the whole data file (all years)?
avg_t = data['TAVG'].mean()
print('The average temperature for all years is', avg_t)

# What was the TMAX temperature of the Summer 69 (i.e. including months May, June, July, August of the year 1969)?
selection_summer = data.ix[(data['DATE']>=19690501) & (data['DATE']<19690901)]
selection_summer_tmax = selection_summer['TMAX']
print(selection_summer_tmax)






 