from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
d=datetime.now()
week_day=d.isoweekday()
week_day_cn=week_list[week_day-1]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),\
         weather['date'],weather['humidity'],weather['wind'],\
         weather['low'],weather['high'],weather['airQuality']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,today_date, humidity,wind,low,high,Air = get_weather()
data = {"date":{"value":today_date},"weekday":{"value":week_day_cn},"weather":{"value":wea},
        "high":{"value":high},"low":{"value":low},
        "city":{"value":city},"wind":{"value":wind},"air":{"value":Air},
        "love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
