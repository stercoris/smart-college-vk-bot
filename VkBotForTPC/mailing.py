import tpc
import base
from datetime import datetime, timedelta
import requests
import time
import re
import sqlite3
import schedule
import pyowm
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

owm = pyowm.OWM('7a3311af086e869f40c669f258aa04f7') 
tl = owm.weather_at_place("Tolyatti, RU")
nmwea = owm.three_hours_forecast("Tolyatti, RU")

def MailingMorning():
    try:
        temp = ((tl.get_weather()).get_temperature('celsius')['temp'])
    except:
        temp = "хз, погода не загрузилась"
    try:
        XKPS = vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение 
    except:
        print(("=== Соединение восстановленно ===").upper())
    print("Рассылка началась")
    for client in base.GetAllUsersForMailing():
        try:
            print("Проверка клиента id : " + client[0])
            if base.GetSubToSchedule(client[0]) == 1:
                try:
                    GroupId = base.GetGroupId(client[0]);
                    if GroupId == 1 or GroupId == 0 :
                        continue
                    Lessions = tpc.GetLession(GroupId,datetime.today().weekday() + 1,tpc.GetWeekColor())
                    if Lessions == "Расписания на этот день нет":
                        continue
                    GroupName = base.GetGroupName(client[0])
                    tpc.send(client[0],f"Погода : {int(float(temp))}℃\nВаше расписание, для группы {GroupName} : \n" + Lessions)
                except:
                    print("Что - то пошло не так")
            else:
                print("Клиент не подписан")
        except:
            print("Error")


def MailingEvening():
    nextmorning = datetime.now() + timedelta(days=0,hours = 13)
    try:
        temp = ((nmwea.get_weather_at(nextmorning)).get_temperature('celsius')['temp'])
    except:
        temp = "хз, погода не загрузилась"
    try:
        XKPS = vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение
    except:
        print(("=== Соединение восстановленно ===").upper())
    print("Рассылка началась")
    for client in base.GetAllUsersForMailing():
        try:
            print("Проверка клиента id : " + client[0])
            if base.GetSubToSchedule(client[0]) == 1:
                try:
                    GroupId = base.GetGroupId(client[0]);
                    if GroupId == 1 or GroupId == 0 :
                        continue
                    Lessions = tpc.GetLession(GroupId,datetime.today().weekday() + 2,tpc.GetWeekColor())
                    if Lessions == "Расписания на этот день нет":
                        continue
                    GroupName = base.GetGroupName(client[0])
                    tpc.send(client[0],f"Погода на завтра : {int(float(temp))}℃\nВаше расписание на завтра, для группы {GroupName} : \n" + Lessions)
                except:
                    print("Что - то пошло не так")
            else: 
                print("Клиент не подписан")
        except:
            print("Error")

schedule.every().day.at("07:00").do(MailingMorning)
schedule.every().day.at("18:05").do(MailingEvening)

tpc.send(297621144,"Клиент запущен")

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except:
        time.sleep(5)
        schedule.run_pending()
