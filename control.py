import time
import datetime
from datetime import date
import  pymysql
import  pymysql.cursors
import pandas as pd
import re

def getLast24HoursData():
  inputList = list()
  t=date.today()
  today = t.strftime("%Y%m%d")
  oneday=datetime.timedelta(days=1) 
  yesterday=t-oneday
  yesterday = yesterday.strftime("%Y%m%d")
  yesterdayTable = 'table_'+yesterday
  todayTable = 'table_'+today
  print(todayTable)
  dbConn = pymysql.connect(host='middlewaredbinstance.cie0rnnmypb0.us-east-1.rds.amazonaws.com', 
        port=3306, user='hyxjames', password='Hyx123987', db='vaData')
  cursor = dbConn.cursor()
  try:
    sql="SELECT * from "+yesterdayTable
    cursor.execute(sql)
    result=cursor.fetchall()
    for data in result:
      inputList.append(yesterday)
      inputList.append(data[0])
      inputList.append(data[1])
      inputList.append(data[2])
      inputList.append(30) #pressure
      inputList.append(0) #wind
    sql = "SELECT * from "+todayTable
    cursor.execute(sql)
    result = cursor.fetchall()
    for data in result:
      inputList.append(today)
      inputList.append(data[0])
      inputList.append(data[1])
      inputList.append(data[2])
      inputList.append(30) #pressure
      inputList.append(0) #wind
      inputList = inputList[len(inputList)-6*24:len(inputList)]
  except:
    print("read data fails")
  dbConn.close()
  return inputList

date = time.strftime("%d", time.localtime())
hour = time.strftime("%H", time.localtime())
minute = time.strftime("%m", time.localtime())
second = time.strftime("%s", time.localtime())
print("minute")
print("second")
curMinute = minute
curSecond = second
maps = {'Unknown': 0, 'Clear': 1, 'Scattered Clouds': 2, 'Mist': 3, 'Haze': 4, 'Shallow Fog': 5,
                              'Patches of Fog': 6, 'Fog': 7, 'Partly Cloudy': 8, 'Mostly Cloudy': 9, 'Overcast': 10,
                              'Funnel Cloud': 11, 'Light Drizzle': 12, 'Drizzle': 13, 'Light Rain': 14, 'Rain': 15,
                              'Heavy Rain': 16, 'Light Thunderstorms and Rain': 17, 'Thunderstorms and Rain': 18,
                              'Thunderstorm': 19, 'Smoke': 20}

while True:
    minute = time.strftime("%m", time.localtime())
    second = time.strftime("%s", time.localtime())
    if minute != curMinute:
        print(minute)
        engine = train.Train('data.csv', maps)
        model = engine.model()
        curMinute = minute
    if int(second) > int(curSecond) + 10:
        print(second)
        curSecond = second
        input = [0]*24*6
        pre = predict.Predict(model, input)
        output = pre.predict()
    time.sleep(1)
