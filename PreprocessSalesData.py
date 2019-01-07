#Purpose of my role in project was to prepare the mattress sales data for further analysis

import pandas as pd
import numpy as np
from datetime import timedelta

def create_date_range(start_date, end_date): #This function outputs an array of dates between start_date and end_date
    A = [];
    for n in range(int((end_date - start_date).days) + 1):
        A.append(start_date + timedelta(n))
    return A

df = pd.read_csv('sales data.txt', sep='\t') #Retrieve data from txt file

Division = df['Division']   #Set variables to different columns of the txt file
Region = df['Region']       #allows for easier and more organized accessibility
Brand = df['Brand']
WrittenDate =(df['WrittenDate'])
UnitsSold = df['UnitsSold']

#First step in task was to find the dates that were not used in the matress sales.
#Through this we use a range of dates from the start date of the sales to the end date.
#Then we use the data listed from the sales data.txt and we subtract them to find the missing dates.

WrittenDate = np.array(pd.to_datetime(WrittenDate).dt.date) #Retrieving "Written Date" coumln and converting the library to numpy from pandas

start_date = np.min(WrittenDate)
end_date = np.max(WrittenDate)

daterange = create_date_range(start_date, end_date); #set new variable to function daterange

daterange = (pd.to_datetime(daterange).date) #convert back to pandas from numpy

diff = np.setdiff1d(daterange, WrittenDate) #Both variables are in the same data type and are now able to be subtracted to find missing dates

units = 0
tf = pd.DataFrame({'WrittenDate': diff, 'UnitsSold': units})

#new data frame is created with dates that are not used in the matress sales

frames = [df, tf]
result = pd.concat(frames, sort='True')

result['WrittenDate'] = pd.to_datetime(result['WrittenDate'])
result = result.sort_values(by='WrittenDate',ascending=True) #sort the sales by writtendate

result.reset_index(drop=True, inplace=True) #reset index according to new sorted result

result['WrittenDate'] = pd.to_datetime(result['WrittenDate']) # converts to pandas datetime
newUnits = result['UnitsSold']

year = pd.DatetimeIndex(result['WrittenDate']).year.astype(str) #get value of year converted in string
week = pd.DatetimeIndex(result['WrittenDate']).week.astype(str) #get value of weeknumber converted in string

final = year+ '_' +['0'+w if len(w)==1 else w for w in week] #need this to converte the date like 2014_1 to 2014_01
zf = pd.DataFrame({'year_week':final, 'UnitsSold':newUnits})
grouped = zf.groupby('year_week').sum()  #group the sale count by year_week
grouped.to_csv('weekly_sales_count.txt',sep='\t') # output weekly sale count to file for forecasting

print grouped