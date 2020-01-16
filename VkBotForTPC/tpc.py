# -*- coding: utf-8 -*-
import requests
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import vk_api
import random 
import datetime
import time
import os
from PIL import Image
from io import BytesIO
from datetime import datetime
from lxml import html
from lxml import etree
import lxml.html
from bs4 import BeautifulSoup
import re
import traceback
import sqlite3
import base

vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")


def GetLession(group, day, week):
    if day > 7:
        day-=7
    Today = datetime.today().weekday() + 1
    print(f"Today : {Today}")
    if Today > 7:
        Today = Today - 7
    Tomorrow = datetime.today().weekday() + 2
    if Tomorrow > 7:
        Tomorrow = Tomorrow - 7
    print(f"Tomorrow : {Tomorrow}")
    url = "http://www.tpcol.ru/asu/timetablestud.php?f=1"
    values = {'group': group,
              'day': day,
              'week' : week}
    response  = requests.post(url, data=values)
    response.encoding = 'cp1251'
    parsed_body = html.fromstring(response.text)
    LessionIdArray = []
    LessionArray = []
    rasp,zamtood = True,True
    for head in parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr/td[@class='head3']/text()"):
        head = "".join(head)
        if "расписания нет!" in head:
            print("Нет расписания на сегодня")
            rasp = False
        elif ("нет" in head) and ("сегодня" in head):
            print("Нет замен на сегодня")
            zamtood = False
    if (rasp == False) and (zamtood == False):
        zamtood = 3
    elif ((rasp == False) and (zamtood == True)) or ((rasp == True) and (zamtood == False)):
        zamtood = 4
    elif (zamtood == True) and (rasp == True):
        zamtood = 5
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{3}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"
        LessionId = "".join(parsed_body.xpath(link))
        if LessionId == "":
            continue
        LessionId = re.sub(" +", "", LessionId)
        LessionId = re.sub("\xa0+", "", LessionId)
        LessionIdArray.append(LessionId)
    print("ИД занятий : " + str(LessionIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{3}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[2]/text()"
        Lession = "".join(parsed_body.xpath(link))
        if Lession == "":
            continue
        Lession = re.sub(" +", " ", Lession)
        Lession = re.sub("\xa0+", " ", Lession)
        LessionArray.append(Lession)
    print("Занятия : " + str(LessionArray))
    ZamenaTodayIdArray = []
    ZamenaTodayArray = []
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"
        ZamenaTodayId = "".join(parsed_body.xpath(link))
        if ZamenaTodayId == "":
            continue
        ZamenaTodayId = re.sub(" +", "", ZamenaTodayId)
        ZamenaTodayId = re.sub("\xa0+", "", ZamenaTodayId)
        ZamenaTodayIdArray.append(ZamenaTodayId)
    print("Замены ИД сегодня : " + str(ZamenaTodayIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[3]/text()"
        ZamenaToday = "".join(parsed_body.xpath(link))
        if ZamenaToday == "":
            continue
        ZamenaToday = re.sub(" +", " ", ZamenaToday)
        ZamenaToday = re.sub("\xa0+", " ", ZamenaToday)
        ZamenaTodayArray.append(ZamenaToday)
    print("Замены сегодня : " + str(ZamenaTodayArray))
    ZamenaTomorrowIdArray = []
    ZamenaTomorrowArray = []
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood+2}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"    
        ZamenaTomorrowId = "".join(parsed_body.xpath(link))
        if ZamenaTomorrowId == "":
            continue
        ZamenaTomorrowId = re.sub(" +", "", ZamenaTomorrowId)
        ZamenaTomorrowId = re.sub("\xa0+", "", ZamenaTomorrowId)
        ZamenaTomorrowIdArray.append(ZamenaTomorrowId)
    print("Замены ИД Завтра : " + str(ZamenaTomorrowIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood+2}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[3]/text()"
        ZamenaTomorrow = "".join(parsed_body.xpath(link))
        if ZamenaTomorrow == "":
            continue
        ZamenaTomorrow = re.sub(" +", " ", ZamenaTomorrow)
        ZamenaTomorrow = re.sub("\xa0+", " ", ZamenaTomorrow)
        ZamenaTomorrowArray.append(ZamenaTomorrow)
    print("Замены Завтра : " + str(ZamenaTomorrowArray))
    Les = {}
    for i in range(len(LessionIdArray)):
            Les[LessionIdArray[i]] = LessionArray[i]
    print(Les)   
    print("День : " + str(day))
    if day == Today:
        print("Замены сегодня")
        Zamena = list(ZamenaTodayIdArray)
        for i in range(len(Zamena)):
            if Zamena[i] not in Les:
                Les[Zamena[i]] = "----------"
            print(f"'{Les[Zamena[i]]}' = Заменен = '{ZamenaTodayArray[i]}'")
            Les[Zamena[i]] = ZamenaTodayArray[i]
    if day == Tomorrow:
        Zamena = list(ZamenaTomorrowIdArray)
        print("Замены завтра")
        for i in range(len(Zamena)):
            if Zamena[i] not in Les:
                Les[Zamena[i]] = "----------"
            print(f"'{Les[Zamena[i]]}'  = Заменен =  '{ZamenaTomorrowArray[i]}'")
            Les[Zamena[i]] = ZamenaTomorrowArray[i] 
    print(Les)
    Lessions = ""
    Keys = list(Les.keys())
    try:
        Start = min(Keys)
    except:
        Start = 1;
    try:
        End = max(Keys)
    except:
        End = 0;
    for i in range(int(Start),int(End) + 1):
        Lessions = Lessions + f"{i} : {Les.get(str(i), '--------------')}" + "\n"
    if Lessions == "":
        return("Расписания на этот день нет")
    return(Lessions)

def GetTeacherLession(group, day, week):
    if day > 7:
        day-=7
    Today = datetime.today().weekday() + 1
    print(f"Today : {Today}")
    if Today > 7:
        Today = Today - 7
    Tomorrow = datetime.today().weekday() + 2
    if Tomorrow > 7:
        Tomorrow = Tomorrow - 7
    print(f"Tomorrow : {Tomorrow}")
    url = "http://www.tpcol.ru/asu/timetableprep.php?f=1"
    values = {'fio': group,
              'day': day,
              'week' : week}
    response  = requests.post(url, data=values)
    response.encoding = 'cp1251'
    parsed_body = html.fromstring(response.text)
    rasp,zamtood = True,True
    for head in parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr/td[@class='head3']/text()"):
        head = "".join(head)
        if "расписания нет!" in head:
            print("Нет расписания на сегодня")
            rasp = False
        elif ("нет" in head) and ("сегодня" in head):
            print("Нет замен на сегодня")
            zamtood = False
    if (rasp == False) and (zamtood == False):
        zamtood = 3
    elif ((rasp == False) and (zamtood == True)) or ((rasp == True) and (zamtood == False)):
        zamtood = 4
    elif (zamtood == True) and (rasp == True):
        zamtood = 5
    #Лекции сегодня
    LessionIdArray = []
    LessionArray = []
    GroupsArray = []
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{3}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"
        LessionId = "".join(parsed_body.xpath(link))
        if LessionId == "":
            continue
        LessionId = re.sub(" +", "", LessionId)
        LessionId = re.sub("\xa0+", "", LessionId)
        LessionIdArray.append(LessionId)
    print("ИД занятий : " + str(LessionIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{3}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[2]/text()"
        Group = "".join(parsed_body.xpath(link))
        if Group == "":
            continue
        Group = re.sub(" +", " ", Group)
        Group = re.sub("\xa0+", " ", Group)
        GroupsArray.append(Group)
    print("Группы : " + str(GroupsArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{3}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[3]/text()"
        Lession = "".join(parsed_body.xpath(link))
        if Lession == "":
            continue
        Lession = re.sub(" +", " ", Lession)
        Lession = re.sub("\xa0+", " ", Lession)
        LessionArray.append(Lession)
    print("Занятия : " + str(LessionArray))
    #Заменый сегодня
    ZamenaTodayIdArray = []
    ZamenaTodayArray = []
    ZamenaTodayGroupsArray = []
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"
        ZamenaTodayId = "".join(parsed_body.xpath(link))
        if ZamenaTodayId == "":
            continue
        ZamenaTodayId = re.sub(" +", "", ZamenaTodayId)
        ZamenaTodayId = re.sub("\xa0+", "", ZamenaTodayId)
        ZamenaTodayIdArray.append(ZamenaTodayId)
    print("Замены ИД сегодня : " + str(ZamenaTodayIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[2]/text()"
        ZamenaTodayGroup = "".join(parsed_body.xpath(link))
        if ZamenaTodayGroup == "":
            continue
        ZamenaTodayGroup = re.sub(" +", " ", ZamenaTodayGroup)
        ZamenaTodayGroup = re.sub("\xa0+", " ", ZamenaTodayGroup)
        ZamenaTodayGroupsArray.append(ZamenaTodayGroup)
    print("Группы(замены сегодня) : " + str(ZamenaTodayGroupsArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[3]/text()"
        ZamenaToday = "".join(parsed_body.xpath(link))
        if ZamenaToday == "":
            continue
        ZamenaToday = re.sub(" +", " ", ZamenaToday)
        ZamenaToday = re.sub("\xa0+", " ", ZamenaToday)
        ZamenaTodayArray.append(ZamenaToday)
    print("Замены сегодня : " + str(ZamenaTodayArray))
    #Заменый завтра
    ZamenaTomorrowIdArray = []
    ZamenaTomorrowArray = []
    ZamenaTomorrowGroupArray = []
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood+2}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[1]/text()"    
        ZamenaTomorrowId = "".join(parsed_body.xpath(link))
        if ZamenaTomorrowId == "":
            continue
        ZamenaTomorrowId = re.sub(" +", "", ZamenaTomorrowId)
        ZamenaTomorrowId = re.sub("\xa0+", "", ZamenaTomorrowId)
        ZamenaTomorrowIdArray.append(ZamenaTomorrowId)
    print("Замены ИД Завтра : " + str(ZamenaTomorrowIdArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood+2}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[2]/text()"
        ZamenaTomorrowGroup = "".join(parsed_body.xpath(link))
        if ZamenaTomorrowGroup == "":
            continue
        ZamenaTomorrowGroup = re.sub(" +", " ", ZamenaTomorrowGroup)
        ZamenaTomorrowGroup = re.sub("\xa0+", " ", ZamenaTomorrowGroup)
        ZamenaTomorrowGroupArray.append(ZamenaTomorrowGroup)
    print("Группы(замены сегодня) : " + str(ZamenaTomorrowGroupArray))
    for i in range(1,8):
        link = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[{zamtood+2}]//tr/td[2]/table//tr[1]/td[2]/table//tr[@class='ttext'][{i}]/td[3]/text()"
        ZamenaTomorrow = "".join(parsed_body.xpath(link))
        if ZamenaTomorrow == "":
            continue
        ZamenaTomorrow = re.sub(" +", " ", ZamenaTomorrow)
        ZamenaTomorrow = re.sub("\xa0+", " ", ZamenaTomorrow)
        ZamenaTomorrowArray.append(ZamenaTomorrow)
    #Сортировка
    print("Замены Завтра : " + str(ZamenaTomorrowArray))
    Les = {}
    for i in range(len(LessionIdArray)):
            Les[LessionIdArray[i]] = GroupsArray[i] + " - " + LessionArray[i]
    print(Les)   
    print("День : " + str(day))
    if day == Today:
        print("Замены сегодня")
        Zamena = list(ZamenaTodayIdArray)
        for i in range(len(Zamena)):
            if Zamena[i] not in Les:
                Les[Zamena[i]] = "----------"
            print(f"'{Les[Zamena[i]]}' = Заменен = '{ZamenaTodayArray[i]}'")
            Les[Zamena[i]] = ZamenaTodayGroupsArray[i] + " - " + ZamenaTodayArray[i]
    if day == Tomorrow:
        Zamena = list(ZamenaTomorrowIdArray)
        print("Замены завтра")
        for i in range(len(Zamena)):
            if Zamena[i] not in Les:
                Les[Zamena[i]] = "----------"
            print(f"'{Les[Zamena[i]]}'  = Заменен =  '{ZamenaTomorrowArray[i]}'")
            Les[Zamena[i]] = ZamenaTomorrowGroupArray[i] + " - " + ZamenaTomorrowArray[i] 
    print(Les)
    Lessions = ""
    Keys = list(Les.keys())
    try:
        Start = min(Keys)
    except:
        Start = 1;
    try:
        End = max(Keys)
    except:
        End = 0;
    for i in range(int(Start),int(End) + 1):
        Lessions = Lessions + f"{i} : {Les.get(str(i), '--------------')}" + "\n"
    if Lessions == "":
        return("Расписания на этот день нет")
    return(Lessions)

vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
 



def send(sendid,sendmessage,keyboard=""):
    print("Ответ :" + sendmessage) 
    try:
        vk.method("messages.send",   {
                "peer_id": sendid,
                "random_id": random.randint(1, 9999999999999999),
                "message": sendmessage,
                "keyboard": keyboard
                })
    except Exception as err:
        print(err)
        vk.method("messages.send",   {
                "peer_id": sendid,
                "random_id": random.randint(1, 9999999999999999),
                "message": sendmessage,
                "keyboard": keyboard
                })

def GetExams(group):
    url = "http://www.tpcol.ru/asu/exams.php?f=0"
    values = {'group':str(group),}
    response  = requests.post(url, data=values)
    response.encoding = 'cp1251'
    parsed_body = html.fromstring(response.text)
    ExamsArray = []
    r = ""
    for a in range(2,33):
        ExamsTime = parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[2]//tr[" + str(a) + "]/td[1]/text()")
        ExamsTime = "".join(ExamsTime)
        if ExamsTime == "":
            break
        ExamsName = parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[2]//tr[" + str(a) + "]/td[2]/text()")
        ExamsName = "".join(ExamsName)
        ExamsTeacher = parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[2]//tr[" + str(a) + "]/td[3]/text()")
        ExamsTeacher = "".join(ExamsTeacher)
        ExamsArray = ExamsArray + [[ExamsTime,ExamsName,ExamsTeacher]]
    for a in range(len(ExamsArray)):
        r = r + "------------------------"  + "\n" + str(ExamsArray[a][0]) + "\n" + ExamsArray[a][1] + "\n" + ExamsArray[a][2] + "\n"
    s = re.sub(" +", " ", r)
    if s != "":
        return(s)
    else:
        return("Расписание экзаменов для выбранной группы отсутствует!")


def GetChat(chat_id):
    try:
        a = vk.method("messages.getConversationsById",
                                        {
                                        "peer_ids": chat_id,
                                        })
    except:
         a = vk.method("messages.getConversationsById",
                                        {
                                        "peer_ids": chat_id,
                                        })
    print(a)
    if a["items"][0]["peer"]["type"] != "chat":
        return("556")
    try: 
        ChatName = a["items"][0]["chat_settings"]["title"]
        return(base.GetGroupByName(ChatName))
    except:
        return("556")
                    

def GetWeekColor():
    url = "http://www.tpcol.ru/asu/timetablestud.php?f=0"
    response  = requests.get(url)
    response.encoding = 'cp1251'
    Today = datetime.today().weekday() + 1
    if Today > 7:
        Today = Today - 7
    parsed_body = html.fromstring(response.text)
    WeekColor = parsed_body.xpath("/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/font/text()")
    WeekColor = "".join(WeekColor)
    print(WeekColor)
    if WeekColor == "КРАСНАЯ неделя":
        print("Нынешняя неделя - Красная")
        if Today == 7:
            return("1")
        return("0")
    else:
        print("Нынешняя неделя - Зеленая")
        if Today == 7:
            return("0")
        return("1")


def GetButton(label, color, payload=""):
    return{
        "action": {
            "type":"text",
            "payload": json.dumps(payload),
            "label": label
            },
        "color": color
        }



