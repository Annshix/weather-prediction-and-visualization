
import pandas as pd
import datetime
from datetime import date
from datetime import timedelta
import pymysql
import pymysql.cursors
import re

dbConn = pymysql.connect(host='middlewaredbinstance.****.us-east-1.rds.amazonaws.com', 
	port=0000, user='****', password='******', db='trData')
cursor = dbConn.cursor()


url = "https://www.wunderground.com/history/airport/KSNA/"
req_city = "req_city=irvine"
req_state = "req_state=CA"
req_statename = "req_statename=California"
reqdb_zip = "reqdb.zip=92612"
req = '&'.join([req_city,req_state,req_statename,reqdb_zip])
start_date = date.today()

num = 3000
res = []
for i in xrange(140, num+1):
	create_table = "CREATE TABLE IF NOT EXISTS "+ 'table_'+str(i) + "(hour int NOT NULL AUTO_INCREMENT, temperature decimal(5,1) NOT NULL, humidity int NOT NULL,pressure decimal(5,2) NOT NULL, PRIMARY KEY (hour))ENGINE=Innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"
	cursor.execute(create_table)
	dbConn.commit()

	delta = timedelta(days=i)
	time = start_date - delta
	time = time.strftime("20%y/%m/%d")
	tmp = '/'.join([url, time, 'DailyHistory.html?'+req])
	tables = pd.read_html(tmp)
	res.append(tables[-1])

	data = []
	t = tables[-1].values
	orders = []
	for k in xrange(len(t)):
		clock = [int(c) for c in re.findall("\d+", t[k][0])]
		am_pm = t[k][0][-2:]
		if am_pm == "AM" and clock[0] == 12:
			clock[0] -= 12
		if am_pm == "PM" and clock[0] < 12:
			clock[0] += 12
		orders.append(clock[0]*60+clock[1])

	for l in xrange(1,25):
		delta = [abs(x-60*l) for x in orders]
		min_delta = min(delta)
		idx = delta.index(min_delta)
		data.append(t[idx])

	if not data:
		continue

	for j in xrange(24):   #24 hours
		hour = j+1
		try:
			temp = float(re.findall("\d+\.\d+", data[j][2])[0])
			humidity = int(re.findall("\d+", data[j][3])[0])
			pressure = float(re.findall("\d+\.\d+", data[j][4])[0])
			sql = "INSERT into " +'table_'+str(i)+ "(hour, temperature, humidity, pressure) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql,(hour, temp, humidity, pressure))
			dbConn.commit()
		except:
			cursor.execute("DROP TABLE table_"+str(i))
			print i, "table dropped"
			break

	print  i, " day stored in database!"

dbConn.close()

print res
