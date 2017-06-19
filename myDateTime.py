#encoding=utf-8
import datetime
import time
import pytz


t = datetime.datetime.utcnow()
t1 = datetime.datetime.now()
print(t)
print(t1)


def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%MZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    time_str = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%Y-%m-%d %H:%M")
    return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M")))


t3 = utc_to_local(utc_time_str='2012-06-11T15:00Z')
print(t3)

t4 = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
print(t4)

t5 = datetime.datetime.utcfromtimestamp(t3)
print(t5)

t6 = '2012-06-11T15:00Z'.replace('T', ' ').replace('Z', '')
print(t6)

t7 = int(time.time())
print(t7)

t8 = datetime.datetime.utcfromtimestamp(t7)
print(t8)

t9 = datetime.datetime.fromtimestamp(t7)
print(t9)

t10 = datetime.datetime.strptime('2012-06-11T15:00Z', '%Y-%m-%dT%H:%MZ')
print(t10)

t11 = time.strptime('2012-06-11T15:00Z', '%Y-%m-%dT%H:%MZ')
print(t11)

t12 = datetime.datetime.now().strftime('%Y-%m-%dT%H:%MZ')
print(t12)

t13 = datetime.datetime.now() - datetime.timedelta(hours=8)
print(t13)

t14 = int(time.mktime(t11))
print(t14)

t15 = datetime.datetime.fromtimestamp(t14)
print(t15)

