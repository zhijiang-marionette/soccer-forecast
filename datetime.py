import datetime

str = '2017-10-26 23:00:07'
date = datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
print(date)