from datetime import datetime, timedelta
from datetime import date
import requests
import time
import users
import user
import re
import sqlite3
import schedule
import pyowm
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


## Тут Рассылка

## Утро
def mor():
    for u in users.Users().subbed():
        gname,gid = u.UserGroup
        print(f"Сообщение для: {gname} {gid}")
        if(u.getSchedule(u.today()) != None):
            try:
                u.send(f"Ваше расписание на сегодня({gname}):\n{u.getSchedule(u.today())}")
            except:
                pass

## Вечер
def eve():
    for u in users.Users().subbed():
        gname,gid = u.UserGroup
        print(f"Сообщение для: {gname} {gid}")
        if(u.getSchedule(u.tomorrow()) != None):
            try:
                u.send(f"Ваше расписание на завтра({gname}):\n{u.getSchedule(u.tomorrow())}")
            except:
                pass
        
def test():
    u = user.User("297621144")
    gname,gid = u.UserGroup
    print(f"Сообщение для: {gname} {gid}")
    if(u.getSchedule(u.tomorrow()) != None):
        try:
            u.send(f"Ваше расписание на завтра({gname}):\n{u.getSchedule(u.tomorrow())}")
        except:
            pass
#test()

schedule.every().day.at("07:10").do(mor)
schedule.every().day.at("18:32").do(eve)


while True:
    schedule.run_pending()
    time.sleep(5)
