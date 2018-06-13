import time

date = time.strftime("%d", time.localtime())
hour = time.strftime("%H", time.localtime())
minute = time.strftime("%m", time.localtime())
second = time.strftime("%s", time.localtime())
print("minute")
print("second")
curMinute = minute;
curSecond = second;
while(True):
	minute = time.strftime("%m", time.localtime())
	second = time.strftime("%s", time.localtime())
	if(minute != curMinute):
		print(minute);
		curMinute = minute
	if(int(second) > int(curSecond)+10):
		print(second);
		curSecond = second;
	time.sleep(1)