import time
import train
import predict

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
