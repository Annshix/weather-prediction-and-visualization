import pymysql
import pymysql.cursors
import pandas as pd
import re

conn = pymysql.connect(host='middlewaredbinstance.cie0rnnmypb0.us-east-1.rds.amazonaws.com', port=3306, user='hyxjames',
                       password='Hyx123987', db='trData', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

dateList = list()
temperatureList = list()
pressureList = list()
humidityList = list()
hourList = list()
condList = list()
try:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            sql = "select * from " + table['Tables_in_trData']
            cursor.execute(sql)
            result = cursor.fetchall()
            for data in result:
                date = re.findall(r't_(.*)', table['Tables_in_trData'])[0]
                dateList.append(date)
                temperatureList.append(data['temperature'])
                pressureList.append(data['pressure'])
                humidityList.append(data['humidity'])
                hourList.append(data['hour'])
                condList.append(data['cond'])
finally:
    conn.close()
    dataframe = pd.DataFrame({'date': dateList, 'hour': hourList, 'temperature': temperatureList,
                              'pressure': pressureList, 'humidity': humidityList, 'condition': condList})
    dataframe.to_csv("data.csv", index=False, sep=',')
