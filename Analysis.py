# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 17:05:08 2017

@author: shampa
"""


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from calendar import weekday, day_name
from datetime import datetime
import math

dataFolder = 'D:/ANZ/Results'
#printTopFIVe
def topFive(data):
    colNames=list(data)
    output="Rank::"+"\t"
    for j in range(len(colNames)):
        output=output+colNames[j]+"\t"
    output=output+"\n"
    print(output)
    for i in range(0,min(5,len(data))):
        output= str(i)+"::\t"
        for j in range(len(colNames)):
            output=output+str(data[colNames[j]][i])+"\t"
        output=output+"\n"
        print(output)
def printTopFive(data):
    #colNames=list(data)
    output="Rank::"+"\tValue"+ "\tFrequency"
    output=output+"\n"
    print(output)
    for i in range(0,min(5,len(data))):
        output= str(i)+"::\t"
        output=output+str(data.index[i])+"\t"+str(data.values[i])
        output=output+"\n"
        print(output)
def convertToNumeric(data,colNames,dataTypes):
    for i in range(len(data)):
        for j in range(len(colNames)):
            value=0
            colName=colNames[j]
            dataType=dataTypes[j]
            if dataType=='float':
                value=float(data[colName][i].replace(",",""))
            elif dataType=='int':
                value=int(data[colName][i].replace(",",""))
            data[colName][i]=value
            
    return data

def calculateDuration(startT,endT):
    startDate=startT.split()
    endDate=endT.split()

    FMT = '%H:%M:%S'
    if startDate[0]==endDate[0]:
        tDelta = datetime.strptime(endDate[1], FMT) - datetime.strptime(startDate[1], FMT)
    else:
        tDelta=-1000
        return tDelta
        
#    if tDelta.seconds/60 >60:
#        return tDelta.seconds/3600
#    else:    
    return tDelta.seconds/60

def addDurationAndDayName(data):
    colName='trip_duration'
    colName1='trip_day'
    colName2='trip_hour_start'
    colName3='trip_hour_end'
    value=[]
    valueName=[]
    valueStartHour=[]
    valueEndHour=[]
    for i in range(len(data)):
        startT=dataset['tpep_pickup_datetime'][i]
        endT=dataset['tpep_dropoff_datetime'][i]
        duration=calculateDuration(startT,endT)
        date=startT.split()
        hour=date[1].split(":")
        hour=int(hour[0])
        dateE=endT.split()
        hourE=dateE[1].split(":")
        hourE=int(hourE[0])
        date=date[0].split("-")
        dayNumber = weekday(int(date[0]), int(date[1]), int(date[2]))
        dayName = day_name[dayNumber]
        value.append(duration)
        valueName.append(dayName)
        valueStartHour.append(hour)
        valueEndHour.append(hourE)
       
    data[colName] = pd.Series(value, index=data.index) 
    data[colName1] = pd.Series(valueName, index=data.index)
    data[colName2] = pd.Series(valueStartHour, index=data.index)
    data[colName3] = pd.Series(valueEndHour, index=data.index)       

def writeData(base_filename,dataFrame,lookupsFolder):
    with open(os.path.join(lookupsFolder, base_filename),'w') as outfile:
        dataFrame.to_string(outfile,index=False)

def appendData(base_filename,dataFrame,lookupsFolder):
    with open(os.path.join(lookupsFolder, base_filename),'a') as outfile:
        dataFrame.to_string(outfile,index=False,header=False)
#************************************************************************_____________________________________________________________________________

              
dataset = pd.read_csv('yellow_tripdata_2016-01\yellow_tripdata_2016-01.csv')
addDurationAndDayName(dataset)
datasetNew=dataset[dataset['fare_amount'] >0] 
datasetNew=datasetNew[datasetNew['passenger_count'] >0] 
datasetNew=datasetNew[datasetNew['trip_duration'] >0]
datasetNew=datasetNew[datasetNew['trip_distance'] >0]
datasetNew=datasetNew[ datasetNew['pickup_longitude'] !=0]
datasetNew=datasetNew[ datasetNew['pickup_latitude'] !=0]
datasetNew=datasetNew[ datasetNew['dropoff_longitude'] !=0]
datasetNew=datasetNew[ datasetNew['dropoff_latitude'] !=0]
datasetNew=datasetNew[datasetNew['pickup_longitude'] != datasetNew['dropoff_longitude'] ]
datasetNew=datasetNew[datasetNew['pickup_latitude'] != datasetNew['dropoff_latitude'] ]

datasetold=dataset
dataset=datasetNew
dataset=dataset.reset_index(drop=True)
writeData('CleanedTaxiData.txt',datasetNew,dataFolder)

#histogram of number of passengers per trip
#------------------------------------------------------------------

passengerCount =dataset.groupby(['passenger_count']).size()
passengerCount = {'passenger_count': passengerCount.index, 'Frequency': passengerCount.values}
passengerCount = pd.DataFrame(data=passengerCount)
topFive(passengerCount)

plt.bar(passengerCount['passenger_count'],passengerCount['Frequency'])
plt.xticks(passengerCount['passenger_count'])
plt.legend()
plt.title("Distribution of number of passenger per taxi trip")
plt.xlabel("Number of passenger")
plt.ylabel("Frequency")
#------------------------------------------------------------------
#histogram of payment type

paymentType=dataset.groupby(['payment_type']).size()
paymentType= {'payment_type': paymentType.index, 'Frequency': paymentType.values}
paymentType= pd.DataFrame(data=paymentType)
topFive(paymentType)

plt.cla()

paymentTypeCat = {1:('Credit Card','r'), 
              2:('Cash','g'), 
              3:('No Charge','b'), 
              4:('Dispute','yellow'), 
              5:('Unknown','k'), 
              6:('Voided Trip', 'magenta')}
ax1 = plt.subplot(111)

for j in range(len(paymentType)):
    ax1.bar(paymentType['payment_type'][j], paymentType['Frequency'][j], width=0.8, bottom=0.0, align='center', color=paymentTypeCat[paymentType['payment_type'][j]][1], alpha=0.6, label=paymentTypeCat[paymentType['payment_type'][j]][0])
  

ax1.set_xticks(paymentType['payment_type'])
ax1.set_xticklabels([paymentTypeCat[i][0] for i in paymentType['payment_type']])
ax1.legend()
ax1.set_title("Distribution of payment type on taxi trip")
ax1.set_xlabel("Payment Type")
ax1.set_ylabel("Frequency")
plt.show()

ax1.cla()



#------------------------------------------------------------------
#histogram of fare amount

fareAmount=dataset.groupby(['fare_amount']).size()
fareAmount= {'fare_amount': fareAmount.index, 'Frequency': fareAmount.values}
fareAmount= pd.DataFrame(data=fareAmount)
fareAmount=fareAmount.sort_values(by=['Frequency'],ascending=[False])
fareAmount=fareAmount.reset_index(drop=True)
topFive(fareAmount)

plt.cla()
plt.bar(fareAmount['fare_amount'][0:20], fareAmount['Frequency'][0:20],width=0.1, color = 'red')  
#plt.xticks(fareAmount['fare_amount'][0:20])
plt.title("Distribution of fare amount per trip")
plt.xlabel("Fare amount per trip")
plt.ylabel("Frequency")
plt.show()



#------------------------------------------------------------------
#histogram of total fare amount

totalAmount=dataset.groupby(['total_amount']).size()
totalAmount= {'total_amount': totalAmount.index, 'Frequency': totalAmount.values}
totalAmount= pd.DataFrame(data=totalAmount)
totalAmount=totalAmount.sort_values(by=['Frequency'],ascending=[False])
totalAmount=totalAmount.reset_index(drop=True)
topFive(totalAmount)

plt.cla()
plt.bar(totalAmount['total_amount'][0:20], totalAmount['Frequency'][0:20],width=0.1, color = 'black')  
#plt.xticks(fareAmount['fare_amount'])
plt.title("Distribution of Total amount per trip")
plt.xlabel("Total amount per trip")
plt.ylabel("Frequency")
plt.show()


#histogram of tips amount
tipsAmount=dataset.groupby(['tip_amount']).size()
tipsAmount= {'tip_amount': tipsAmount.index, 'Frequency': tipsAmount.values}
tipsAmount= pd.DataFrame(data=tipsAmount)
tipsAmount=tipsAmount.sort_values(by=['Frequency'],ascending=[False])
tipsAmount=tipsAmount.reset_index(drop=True)
topFive(tipsAmount)


plt.cla()
plt.bar(tipsAmount['tip_amount'][0:10], tipsAmount['Frequency'][0:10],width=0.3,color = 'green')  
plt.title("Distribution of Tips amount per trip")
plt.xlabel("Tips amount per trip")
plt.ylabel("Frequency")
plt.show()

#busiest hour weekdays
weekends=['Saturday','Sunday']
weekdays=['Friday','Monday','Tuesday','Wednesday', 'Thursday']
datasetWeek=dataset[dataset['trip_day'] != 'Saturday'] 
datasetWeek=datasetWeek[datasetWeek['trip_day'] != 'Sunday']
datasetWeekend=dataset[dataset['trip_day'] != weekdays[0] ] 
for i in range(1,len(weekdays)):
    datasetWeekend=datasetWeekend[datasetWeekend['trip_day'] != weekdays[i]]

busyHour=datasetWeek.groupby(['trip_hour_start']).size()
busyHour= {'trip_hour_start': busyHour.index, 'Frequency': busyHour.values}
busyHour= pd.DataFrame(data=busyHour)
busyHour=busyHour.sort_values(by=['Frequency'],ascending=[False])
busyHour=busyHour.reset_index(drop=True)
topFive(busyHour)

plt.cla()
plt.bar(busyHour['trip_hour_start'],(busyHour['Frequency']*100)/len(datasetWeek),width=0.8,color = 'green')  
plt.xticks(busyHour['trip_hour_start'])
plt.title("Distribution of busy hours in weekdays")
plt.xlabel("Hours")
plt.ylabel("Percentage (%)")
plt.show()


#weekends
busyHourWeekend=datasetWeekend.groupby(['trip_hour_start']).size()
busyHourWeekend= {'trip_hour_start': busyHourWeekend.index, 'Frequency': busyHourWeekend.values}
busyHourWeekend= pd.DataFrame(data=busyHourWeekend)
busyHourWeekend=busyHourWeekend.sort_values(by=['Frequency'],ascending=[False])
busyHourWeekend=busyHourWeekend.reset_index(drop=True)
topFive(busyHourWeekend)

plt.cla()
plt.bar(busyHourWeekend['trip_hour_start'],(busyHourWeekend['Frequency']*100)/len(datasetWeekend),width=0.8,color = 'green')  
plt.xticks(busyHourWeekend['trip_hour_start'])
plt.title("Distribution of busy hours in weekends")
plt.xlabel("Hours")
plt.ylabel("Percentage (%)")
plt.show()

#discrepency in dataset
#1 number of passenger per trip =0
#fare amount is negative
#total amount is negative
#tips amount is negative
#trip distance is 0
#when passenger count is 0, check trip distance is 0,check pick and drop time and location
#check fare amount and total amount

#for 11 entries pickup>drop down

#dataset.to_csv('Taxidata.txt', sep='\t', index=False)

#plt.hist(dataset['passenger_count'])
#plt.title("Distribution of number of passengers per trip")
#plt.xlabel("Number of passengers per trip")
#plt.ylabel("Frequency")
#fig = plt.gcf()
#plt.cla()


#frequency of trip each day
dayTypeCat = {1:('Friday','r',0), 
              2:('Saturday','g',1), 
              3:('Sunday','b',2), 
              4:('Monday','yellow',3), 
              5:('Tuesday','violet',4), 
              6:('Wednesday', 'magenta',5),
              7:('Thursday','black',6)}
day=[0,1,2,3,4,5,6]
ax1 = plt.subplot(111)

plt.cla()
tripDayFrequency=dataset['trip_day'].value_counts()
for j in range(1,len(dayTypeCat)+1):
    ax1.bar(dayTypeCat[j][2], (tripDayFrequency[dayTypeCat[j][0]]*100)/len(dataset), width=0.8, bottom=0.0, align='center', color=dayTypeCat[j][1], alpha=0.6, label=dayTypeCat[j][0])
  
ax1.set_xticks(day)
ax1.set_xticklabels([dayTypeCat[i+1][0][0:3] for i in day])
ax1.legend()
ax1.set_title("Distribution of trips on each day")
ax1.set_xlabel("Day")
ax1.set_ylabel("Percentage (%)")
plt.show()



#What is the hourly taxi activity for each day of the week
allDays=['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']
activityHour=dataset.groupby(['trip_hour_start','trip_day']).size()

hours=[]
days=[]
for i in range(0,24):
    for j in range(0,7):
        hours.append(i)
        days.append(allDays[j])

values=activityHour.values/29
activityHour= {'trip_hour_start': hours, 'trip_day': days,'Frequency': values }
activityHour= pd.DataFrame(data=activityHour)
activityHour=activityHour.sort_values(by=['Frequency'],ascending=[False])
activityHour=activityHour.reset_index(drop=True)
topFive(activityHour)

writeData('plotActivty.csv',activityHour,dataFolder)

#Which trip has the most consistent fares:

consistantTrip=dataset.groupby(['trip_duration', 'trip_distance','fare_amount']).size()

distance=[]
time=[]
money=[]
for i in range(len(consistantTrip)):
    distance.append((consistantTrip.index.values[i][1]))
    time.append((consistantTrip.index.values[i][0]))
    money.append((consistantTrip.index.values[i][2]))
values=consistantTrip.values
consistantTrip= {'trip_duration': time, 'trip_distance': distance,'fare_amount':money,'Frequency': values }
consistantTrip= pd.DataFrame(data=consistantTrip)

consistantTrip=consistantTrip.sort_values(by=['Frequency'],ascending=[False])
consistantTrip=consistantTrip.reset_index(drop=True)
topFive(consistantTrip)
 
writeData('consistantTrip.csv',consistantTrip,dataFolder)





