# -*- coding: utf-8 -*-
import requests
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random 
import datetime
import requests
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
import tpc
import base
import subprocess
import sys
import hltv 

print("aaa") 

for Player in hltv.top_players():
    print(f"{(Player['nickname']).decode()} {Player['name']}")
vk = vk_api.VkApi(token="c5eff1b045b1c04f154d9255e57bef5224af5f21cd2dad94394f21bb3378eb014ee59b5fb2dbc5a83160b")
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, "184728287")

nl = '\n'

ZvonKi = '1 : 8:30 - 10:00 ' + nl + '2 : 10:20 - 11:50' + nl + '3 : 12:20 - 13:50' + nl + '4 : 14:00 - 15:30' + nl + '5 : 15:40 - 17:10'


def GetMembersOfConv(id):
    try:
        a = vk.method("messages.getConversationMembers",
                      {"peer_id": id,"fields": "is_admin"})
    except:
        a = vk.method("messages.getConversationMembers",
                      {"peer_id": id,"fields": "is_admin"})
    return(a)
    
def send(sendid,sendmessage,keyboard=""):
    print(f"Ответ : {nl} {sendmessage}") 
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
    print("----------------- END ---------------------")

def isadmin(sendid,userid):
    a = GetMembersOfConv(sendid)
    for i in a["items"]:
        print(i)
        print(userid)
        try:
            if i["member_id"] == userid and i["is_admin"] == True:
                return("yes")
        except KeyError:
            return("say")

def iskyamran(userid,sendid):
    try:
        a = GetMembersOfConv(sendid)
        return(True)
    except vk_api.exceptions.ApiError:
        if userid == 271961752:
            time.sleep(2)
            return(False)
        return(True)

def photo(user_id):
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open("screenshot.png", 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])
    vk.method("messages.send",   {
                "peer_id": user_id,
                "message": " ",
                "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                "random_id": random.randint(1, 9999999999999999)
                })

KeyboardMain = {
    "one_time": False,
    "buttons" : [
                [tpc.GetButton(label = "Группа",color="default")],
               [tpc.GetButton(label = "Опции",color="default")],
        ]
    }
KeyboardMain = json.dumps(KeyboardMain, ensure_ascii=False).encode("utf-8")
KeyboardMain = str(KeyboardMain.decode("utf-8"))

KeyboardGroup = {
    "one_time": False,
    "buttons" : [
            [tpc.GetButton(label = "Установить группу",color="default")],
            [tpc.GetButton(label = "Главное меню",color="negative")]
        ]
    }
KeyboardGroup = json.dumps(KeyboardGroup, ensure_ascii=False).encode("utf-8")
KeyboardGroup = str(KeyboardGroup.decode("utf-8"))

def GoToMainMenu(userid):
    if base.GetGroupId(userid) == "1":
        base.SetGroupId(userid,0)
    send(userid,"Выберите опцию",KeyboardMain)

KeyboardSubToSchedule = {
    "one_time": False,
    "buttons" : [
            [tpc.GetButton(label = "Сегодня",color="default"),
             tpc.GetButton(label = "Завтра",color="default")],
            [tpc.GetButton(label = "Подписаться",color="default"),
            tpc.GetButton(label = "Отписаться",color="default")],
            [tpc.GetButton(label = "Экзамены",color="default"),
            tpc.GetButton(label = "Главное меню",color="negative")]
        ]
    }
KeyboardSubToSchedule = json.dumps(KeyboardSubToSchedule, ensure_ascii=False).encode("utf-8")
KeyboardSubToSchedule = str(KeyboardSubToSchedule.decode("utf-8"))

error = ["Ашибка", "Еррор", "Ошибка", "Оплошность","просчет"]
admin = ["ніяк, прав немає" , "Прав нет да", "Прав а", "Можно права?", "Никак","Дайб прав"]

Rasp = ("подписаться","отписаться","опции","сегодня","завтра","экзамены","расписание")

def ReRoll():
    try:
        longpoll.update_longpoll_server()
        for event in longpoll.check():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        XKPS = vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение
                    except:
                        print(("=== Соединение восстановленно ===").upper())
                    print("----------------- Event ---------------------")
                    print(event)
                    print("----------------- Event ---------------------")
                    print("----------------- User ---------------------")
                    text = event.object.text.lower()
                    print("Сообщение :" + text)
                    fromid = event.object.peer_id
                    print("Из :" + str(fromid))
                    userid = event.object.from_id
                    print("От :" + str(userid))
                    print(datetime.now())
                    print("----------------- User ---------------------")
                    if event.from_user:
                        if base.GetUser(userid) == False:
                                base.AddToUserList(userid)
                        print("Есть ли пользователь в базе :" + str(base.GetUser(userid)))
                        #============= ГЛАВНОЕ МЕНЮ =============
                        if text == "главное меню":
                            try:
                                if base.GetGroupId(userid) == "1":
                                    base.SetGroupId(userid,0)
                                send(userid,"Выберите опцию",KeyboardMain)
                            except:
                                print("Ошибка в главном меню")
                        #============= ГЛАВНОЕ МЕНЮ =============
                        #--------------Установка группы пользователя---------------------#
                        elif base.GetGroupId(userid) == "1":
                            print("--- Указание группы ---")
                            GroupName = tpc.GetGroup(text)
                            print("Получение id группы по названию : " + str(GroupName))
                            if int(GroupName) == 0:
                                print("Группа не найдена")
                                send(userid,"Такой группы в базе нет")
                            else:
                                print("Группа найдена :" + text + ", " + str(GroupName))
                                base.SetGroup(userid,text,str(GroupName))
                                send(userid,"Успешно",KeyboardMain)
                            continue
                        #----------------------------------------------------------------#
                        elif text == "привет" or  text == "начать":
                            send(userid,"Я ТПК бот",KeyboardMain)
                        else: 
                            if text == "группа":
                                send(fromid,"Выберите опцию",KeyboardGroup)
                            elif text == "установить группу":
                                send(userid,"Отправьте название вашей группы")
                                base.SetGroupId(userid, 1)
                            elif text in Rasp:
                                UserGroup = base.GetGroupId(userid)
                                if UserGroup == "0":
                                    send(userid,"Для начала выставите название своей группы")
                                    continue
                                elif text == "подписаться":
                                        base.SubToSchedule(userid)
                                        send(userid,"Вы успешно подписались",KeyboardMain)
                                elif text == "отписаться":
                                        base.UnSubToSchedule(userid)
                                        send(userid,"Вы отписались",KeyboardMain)
                                elif text == "опции":
                                    send(userid,"Выберите опцию",KeyboardSubToSchedule)
                                elif text == "завтра":
                                    send(userid,tpc.GetLession(base.GetGroupId(userid),datetime.today().weekday() + 2,tpc.GetWeekColor()))
                                elif text == "сегодня":
                                    send(userid,tpc.GetLession(base.GetGroupId(userid),datetime.today().weekday() + 1,tpc.GetWeekColor())) 
                                elif text == "экзамены":
                                    send(userid,tpc.GetExams(base.GetGroupId(userid)))
                                else:
                                    GoToMainMenu(userid)

                            
                    if event.from_chat:
                        if text[0:3] == "!по" or text[0:3] == "!вт" or text[0:3] == "!ср" or text[0:3] == "!чт" or text[0:3] == "!пя":
                            ColorOfWeek = tpc.GetWeekColor()
                            print("Нынений - ColorOfWeek : " + str(ColorOfWeek))
                            try:
                                if text[3] == "з": 
                                    ColorOfWeek = 1
                                    print(ColorOfWeek)
                                elif text[3] == "к":
                                    ColorOfWeek = 0
                                    print(ColorOfWeek)
                            except:
                                print("Выполнен запрос без указания недели")
                                ColorOfWeek = tpc.GetWeekColor()
                                print("День недели - ColorOfWeek : " + str(ColorOfWeek))
                            
                            #Cегодня
                            if text[0:3] == "!по":
                                weekday = 1
                            if text[0:3] == "!вт":
                                weekday = 2
                            if text[0:3] == "!ср":
                                weekday = 3
                            if text[0:3] == "!чт":
                                weekday = 4
                            if text[0:3] == "!пя":
                                weekday = 5
                            print("ass")
                            try:
                                message = tpc.GetLession(tpc.GetChat(fromid),int(weekday),int(ColorOfWeek))
                                send(fromid,message)
                            except vk_api.exceptions.ApiError:
                                i = random.randint(0,5)
                                send(fromid,admin[i])
                        elif text == "!команды":
                            commands = """  !по - + по(понедельник)/вт(вторник) и т.д.
                                            !пок/!поз + по(понедельник)/вт(вторник) + к(красная)/з(зеленая)
                                            !р - расписание.!рк/!рз + к(красная)/з(зеленая)
                                            !з - расписание на завтра.!зк/!зз + к(красная)/з(зеленая)
                                            !рулетка
                                            !рулет
                                            """  
                            send(fromid,commands)
                        elif text == "!жопа":
                            a = isadmin(fromid,userid)
                            if a != "yes":
                                send(fromid,"Вы челядь")
                                continue
                            commands = "хаха жопа"
                            send(fromid,commands)
                        #Кик Пользователей
                        elif text == "!ak" and fromid == "297621144":
                            a = isadmin(fromid,userid)
                            if a != "yes":
                                send(fromid,"Вы челядь")
                                continue
                            try:
                                a = GetMembersOfConv(fromid)
                                count = (a['count'])
                                for i in range(0,count):
                                    try:      
                                        if (a['items'][i]['member_id']) == (-184728287) or (a['items'][i]['member_id']) == (297621144) or (a['items'][i]['member_id']) == (271961752):
                                            continue
                                        vk.method("messages.removeChatUser",
                                                                {
                                                                "chat_id": event.object.peer_id - 2000000000,
                                                                "member_id": a['items'][i]['member_id']
                                                                }
                                                    )
                                    except vk_api.exceptions.ApiError:
                                        i = random.randint(0,5)
                                        send(fromid,admin[i])
                            except vk_api.exceptions.ApiError:
                                i = random.randint(0,5)
                                send(fromid,admin[i])
                        #ЭКЗАМЕНЫ
                        elif text == "!э":
                            try:
                                message = tpc.GetExams(tpc.GetChat(fromid))
                                send(fromid,message)
                            except:
                                i = random.randint(0,5)
                                send(fromid,admin[i])
                        #Упрощенное расписание
                        elif text == "!р" or text == "!з":
                            if text == "!з":
                                weekday = datetime.today().weekday() + 2
                            else:
                                print(datetime.today().weekday() + 1)
                                weekday = datetime.today().weekday() + 1
                            try:
                                message = tpc.GetLession(tpc.GetChat(fromid),int(weekday),tpc.GetWeekColor())
                                send(fromid,message)
                            except vk_api.exceptions.ApiError:
                                i = random.randint(0,5)
                                send(fromid,admin[i])
                        elif text == "!time":     
                            now = datetime.strftime(datetime.now(), "%H:%M:%S")
                            send(fromid,now)
                        elif text == "!звон":
                            send(fromid,ZvonKi)
                        elif text == "!рулетка":
                            try:
                                a = isadmin(fromid,userid)
                                if a != "yes":
                                    send(fromid,"Вы челядь")
                                    continue
                                a = GetMembersOfConv(fromid)
                                count = (a['count'])
                                while True:
                                    if count == 2: 
                                        send(fromid,"Вы проиграли")
                                        break
                                    noname = 0
                                    for i in range(0, count - 2):
                                        name = a['profiles'][i]['id']
                                        if name == (297621144) or name == (271961752) or name == (250908339):
                                            noname = noname + 1
                                    if (noname == (count - 1)) and (fromid != 2000000001):
                                        send(fromid,"В беседе " + str(count-1) + " дебила")
                                        break
                                    i = random.randint(0, count - 2)
                                    p = a['profiles'][i]['id']
                                    if (p == (297621144) or p == (271961752) or p == (250908339)) and (fromid != 2000000001):
                                        send(fromid,"ніяк, прав немає")
                                        continue
                                    try: 
                                        try:
                                            vk.method("messages.removeChatUser",
                                                                    {
                                                                    "chat_id": event.object.peer_id - 2000000000,
                                                                    "member_id": a['profiles'][i]['id']
                                                                    }
                                                        )
                                        except:
                                            vk.method("messages.removeChatUser",
                                                                    {
                                                                    "chat_id": event.object.peer_id - 2000000000,
                                                                    "member_id": a['profiles'][i]['id']
                                                                    }
                                                        )
                                        first_name = a['profiles'][i]['first_name']
                                        last_name = a['profiles'][i]['last_name']
                                        sendm = "Проиграл - " + first_name + " " + last_name
                                        send(fromid,sendm)
                                        break
                                        time.sleep(5)
                                    except vk_api.exceptions.ApiError:
                                        time.sleep(5)
                                        sendm = "Програв - " + first_name + " " + last_name + ".Але він є адміністратором або творцем каналу."
                                        send(fromid,sendm)
                                        break
                            except vk_api.exceptions.ApiError:
                                time.sleep(5)
                                i = random.randint(0,5)
                                send(fromid,admin[i])
                        elif text == "!рулет":
                            try:
                                a = GetMembersOfConv(fromid)
                                count = (a['count'])
                                while True:
                                    if count == 2:
                                        send(fromid,"Вы проиграли")
                                        break
                                    i = random.randint(0, count - 2)
                                    p = a['profiles'][i]['id']
                                    first_name = a['profiles'][i]['first_name']
                                    last_name = a['profiles'][i]['last_name']
                                    sendm = "Проиграл - " + first_name + " " + last_name
                                    send(fromid,sendm)
                                    break
                            except vk_api.exceptions.ApiError:
                                time.sleep(5)
                                i = random.randint(0,5)
                                send(fromid,admin[i])
            except IndexError: 
                i = random.randint(0,4)
                send(fromid,error[i])
            except vk_api.exceptions.ApiError:
                i = random.randint(0,5)
                send(fromid,admin[i])      
    except Exception as err:
        vk = vk_api.VkApi(token="c5eff1b045b1c04f154d9255e57bef5224af5f21cd2dad94394f21bb3378eb014ee59b5fb2dbc5a83160b")
        print(err)
        print("123123123 CRIT ERRROR 123123123")
        time.sleep(60)
while True:
    try:
        ReRoll()
    except Exception as err:
        vk = vk_api.VkApi(token="c5eff1b045b1c04f154d9255e57bef5224af5f21cd2dad94394f21bb3378eb014ee59b5fb2dbc5a83160b")
        print(err)
        print("123123123 CRIT ERRROR 123123123")
        time.sleep(180)
        ReRoll()
    