import tpc
import base
from datetime import datetime, timedelta
from datetime import date
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
w_pari = []
def MailingMorning():
    try:
        temp = ((tl.get_weather()).get_temperature('celsius')['temp'])
        today = datetime.today()
        w_pari = [((nmwea.get_weather_at(today.replace(hour=10,minute=00,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(today.replace(hour=11,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(today.replace(hour=13,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(today.replace(hour=15,minute=30,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(today.replace(hour=17,minute=10,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(today.replace(hour=18,minute=50,second=00))).get_temperature('celsius')['temp'])]
        for i in range(len(w_pari)):
            print(w_pari[i])
    except:
        temp = "хз, погода не загрузилась :("
    try:
        vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение 
    except:
        print(("=== Соединение восстановленно ===").upper())
    print("Рассылка началась")
    for client in base.GetAllUsersForMailing():
        try:
            print("Проверка клиента id : " + client[0])
            if base.GetSubToSchedule(client[0]) == 1:
                try:
                    GroupId = base.GetGroupId(client[0])
                    if GroupId == 1 or GroupId == 0 :
                        continue
                    Lessions = tpc.GetLession(GroupId,datetime.today().weekday() + 1,tpc.GetWeekColor(),w_pari)
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

def rodi_mailing():
    try:
        nextmorning = datetime.now() + timedelta(days=0,hours = 13)
        temp = ((nmwea.get_weather_at(nextmorning)).get_temperature('celsius')['temp'])
        tomorrow = datetime.today() + timedelta(days=1)
        w_pari = [((nmwea.get_weather_at(tomorrow.replace(hour=10,minute=00,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=11,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=13,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=15,minute=30,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=17,minute=10,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=18,minute=50,second=00))).get_temperature('celsius')['temp'])]
        for i in range(len(w_pari)):
            print(w_pari[i])
    except:
        temp = "хз, погода не загрузилась"
    try:
        vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение
    except:
        print(("=== Соединение восстановленно ===").upper())
    print("Рассылка началась")
    try:
        try:
            GroupId = base.GetGroupId(297621144)
            if GroupId == 1 or GroupId == 0 :
                return
            Lessions = tpc.GetLession(GroupId,datetime.today().weekday() + 2,tpc.GetWeekColor(),w_pari)
            if Lessions == "Расписания на этот день нет":
                return
            GroupName = base.GetGroupName(297621144)
            tpc.send(297621144,f"Погода на завтра : {int(float(temp))}℃\nВаше расписание на завтра, для группы {GroupName} : \n" + Lessions)
        except:
            print("Что - то пошло не так")
    except:
        print("Error")
        
rodi_mailing()

def MailingEvening():
    try:
        nextmorning = datetime.now() + timedelta(days=0,hours = 13)
        temp = ((nmwea.get_weather_at(nextmorning)).get_temperature('celsius')['temp'])
        tomorrow = datetime.today() + timedelta(days=1)
        w_pari = [((nmwea.get_weather_at(tomorrow.replace(hour=10,minute=00,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=11,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=13,minute=50,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=15,minute=30,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=17,minute=10,second=00))).get_temperature('celsius')['temp']),
                  ((nmwea.get_weather_at(tomorrow.replace(hour=18,minute=50,second=00))).get_temperature('celsius')['temp'])]
        for i in range(len(w_pari)):
            print(w_pari[i])
    except:
        temp = "хз, погода не загрузилась"
    try:
        vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение
    except:
        print(("=== Соединение восстановленно ===").upper())
    print("Рассылка началась")
    for client in base.GetAllUsersForMailing():
        try:
            print("Проверка клиента id : " + client[0])
            if base.GetSubToSchedule(client[0]) == 1:
                try:
                    GroupId = base.GetGroupId(client[0])
                    if GroupId == 1 or GroupId == 0 :
                        continue
                    Lessions = tpc.GetLession(GroupId,datetime.today().weekday() + 2,tpc.GetWeekColor(),w_pari)
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
schedule.every().day.at("18:00").do(MailingEvening)

tpc.send(297621144,"Клиент запущен")

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except:
        time.sleep(5)
        schedule.run_pending()
