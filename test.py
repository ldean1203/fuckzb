import datetime

today = datetime.date.today()
content = '驻场'
start_time = '9:00'
end_time = '18:00'
for i in range(10, 15):
    sunday = today + datetime.timedelta(6 - today.weekday() + 1) - datetime.timedelta(i)
    date = sunday.strftime("%Y-%m-%d")
    print(date)



