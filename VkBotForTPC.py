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
import threading
import sys
import hltv 





# Авторизация ВК
vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, "184728287")
# Авторизация ВК

#Обновленя БД
print("========================================================== ")
print("== Обновление БД Учителей начато == ")
base.UpdateTeachers()
print("== Обновление БД Учителей завершено == ")
print("========================================================== ")
#Обновленя БД

# Запуск рассылки
# subprocess.Popen([sys.executable, 'mailing.py'])
# Запуск рассылки

error = ["Ашибка", "Еррор", "Ошибка", "Оплошность","просчет"]
admin = ["ніяк, прав немає" , "Прав нет да", "Прав а", "Можно права?", "Никак","Дайб прав"]

Rasp = ("подписаться","отписаться","опции","сегодня","завтра","экзамены","расписание")
nl = '\n'
ZvonKi = '1 : 8:30 - 10:00 ' + nl + '2 : 10:20 - 11:50' + nl + '3 : 12:20 - 13:50' + nl + '4 : 14:00 - 15:30' + nl + '5 : 15:40 - 17:10'

#Keyboards
def get_func_key(userid):
    if(base.GetSubToSchedule(userid) == 1):
        subcont = "Отписаться"
    else:
        subcont = "Подписаться"

        
    KeyboardSubToSchedule = {
        "one_time": False,
        "buttons" : [
                [tpc.GetButton(label = "Сегодня",color="default"),
                 tpc.GetButton(label = "Завтра",color="default")],
                [tpc.GetButton(label = subcont,color="default"),
                tpc.GetButton(label = "Экзамены",color="default")],
                [tpc.GetButton(label = "Главное меню",color="negative")]
            ]
        }
    KeyboardSubToSchedule = json.dumps(KeyboardSubToSchedule, ensure_ascii=False).encode("utf-8")
    KeyboardSubToSchedule = str(KeyboardSubToSchedule.decode("utf-8"))
    return(KeyboardSubToSchedule)

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
        GetMembersOfConv(sendid)
        return(True)
    except vk_api.exceptions.ApiError:
        if userid == 271961752:
            time.sleep(2)
            return(False)
        return(True)

def GetMainKeyboard(userid):
    print(base.GetGroupId(userid))
    if base.GetGroupId(userid) == 1:
        GroupB = tpc.GetButton(label = "Отмена",color="negative")
    else: 
        GroupB = tpc.GetButton(label = "Группа",color="default")
    if base.GetTeacherId(userid) == 1:
        TeacherB = tpc.GetButton(label = "Отмена",color="negative")
    else:
        TeacherB = tpc.GetButton(label = "Учителя",color="default")
    KeyboardMain = {
        "one_time": False,
        "buttons" : [
                   [GroupB,TeacherB],
                   [tpc.GetButton(label = "Опции",color="default")],
            ]
        }
    KeyboardMain = json.dumps(KeyboardMain, ensure_ascii=False).encode("utf-8")
    KeyboardMain = str(KeyboardMain.decode("utf-8"))
    return(KeyboardMain)



def GoToMainMenu(userid):
    if base.GetGroupId(userid) == 1:
        base.SetGroupId(userid,0)
    if base.GetTeacherId == 1 or base.GetTeacherId == 2:
        base.SetTeacherId(userid,0)
    send(userid,"Выберите опцию",GetMainKeyboard(userid))

def GetTeachersKeyboard(letter):
    TeachersList = base.GetTeachersByFirstL(letter)
    buttons = list()
    for Teacher in TeachersList:
        print(len(buttons)%2)
        if len(buttons) > 0 and len(buttons[-1])%2 == 1:
            buttons[-1].append(tpc.GetButton(label = Teacher[0],color="default"))
        else:
            buttons.append([tpc.GetButton(label = Teacher[0],color="default")],)

    print(str(buttons))
    if len(buttons[-1])%2 == 1:
        buttons[-1].append(tpc.GetButton("Главное меню",color="negative"))
    else:
        buttons.append([tpc.GetButton("Главное меню",color="negative")],)
    TeaherKeyboard = {
    "one_time": False,
    "buttons" : buttons
        
    }
    TeaherKeyboard = json.dumps(TeaherKeyboard, ensure_ascii=False).encode("utf-8")
    TeaherKeyboard = str(TeaherKeyboard.decode("utf-8"))
    return(TeaherKeyboard)




def CsGoSort(text):
    for Team in hltv.top30teams():
        if (Team["name"].lower() in text.lower() or text.lower() in Team["name"].lower()):
            print(f"Выбранная команда : {Team['name']}")
            Matches = hltv.get_matches()
            Results = hltv.get_results()
            Message = "     Матчи : \n".upper()
            for match in Matches: 
                 if(match["team1"] == None):
                    continue
                 if ((match["team1"]).decode() == Team["name"]) or ((match["team2"]).decode() == Team["name"]):
                     Message+= f"------------\nДата : {(match['date']).decode()}\nМатч : '{(match['team1']).decode()}' vs '{(match['team2']).decode()}'\nEvent : {(match['event']).decode()}\n"
            Message+= f"------------\n    Результаты :\n".upper()
            for result in Results:
                 print(result)
                 if(result["team1"] == None):
                    continue
                 if ((result["team1"]).decode() == Team["name"]) or ((result["team2"]).decode() == Team["name"]):
                     try:
                         date = (match['date']).decode()
                     except:
                         date = match['date']
                     Message+= f"------------\nДата : {date}\nМатч : '{(result['team1']).decode()}' vs '{(result['team2']).decode()}'\nEvent : {(result['event']).decode()}\nСчет : {(result['team1score'])} -- {(result['team2score'])}\n"
            return(Message)



def VkChecking(event):
    try:
        if event.type == VkBotEventType.MESSAGE_NEW:


            # Проверка соединения  / Запрос к ВК
            try:
                vk.method("users.get",  {"user_ids": "297621144",}) #Херь , которая поддерживает соединение
            except:
                print(("=== Соединение восстановленно ===").upper())
            # Проверка соединения  / Запрос к ВК


            # Вывод Логов
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
            # Вывод Логов


            if event.from_user:
                if base.GetUser(userid) == False:
                        base.AddToUserList(userid)
                print("Есть ли пользователь в базе :" + str(base.GetUser(userid)))
                #============= ГЛАВНОЕ МЕНЮ =============
                if text == "главное меню" or text == "отмена":
                    try:
                        if base.GetGroupId(userid) == 1:
                            base.SetGroupId(userid,0)
                        if base.GetTeacherId(userid) == 1 or base.GetTeacherId(userid) == 2:
                            base.SetTeacherId(userid,0)
                        send(userid,"Выберите опцию",GetMainKeyboard(userid))
                    except:
                        print("Ошибка в главном меню")
                    return
                #============= ГЛАВНОЕ МЕНЮ =============
                #--------------Установка группы пользователя---------------------#
                elif base.GetGroupId(userid) == 1:
                    print("--- Указание группы ---")
                    GroupID = base.GetGroupByName(text.lower())
                    print("Получение id группы по названию : " + str(GroupID))
                    if int(GroupID) == 0:
                        print("Группа не найдена")
                        send(userid,"Такой группы в базе нет")
                    else:
                        print("Группа найдена :" + text + ", " + str(GroupID))
                        base.SetGroup(userid,text,str(GroupID))
                        send(userid,"Успешно",GetMainKeyboard(userid))
                        base.SetTeacherId(userid,0)

                    return
                #----------------------------------------------------------------#
                #--------------Установка "Учителя" пользователя---------------------#
                elif base.GetTeacherId(userid) == 1:
                    print("--- Указание 'Учителя' ---")
                    Teachers = base.GetTeachersByFirstL(text)
                    if Teachers == 0: 
                        send(userid,"Учителя не найдены")
                    else:
                        print("Учителя найдены" + str(Teachers))
                        Keyboard = GetTeachersKeyboard(text)
                        send(userid,"Выберите учителя",Keyboard)
                        base.SetTeacherId(userid,2)
                    return
                elif base.GetTeacherId(userid) == 2:
                    Teacher = base.GetTeachersBySName(text)
                    if Teacher == 0:
                        send(userid,"Нажмите кнопку")
                    else:
                        base.SetTeacherId(userid,Teacher[0][1])
                        send(userid,"Успешно", GetMainKeyboard(userid))
                        base.SetGroupId(userid,0)
                #----------------------------------------------------------------#
                elif text == "привет" or  text == "начать":
                    send(userid,"Я ТПК бот",GetMainKeyboard(userid))
                else: 
                    if text == "группа":
                        base.SetGroupId(userid, 1)
                        send(userid,"Отправьте название вашей группы",GetMainKeyboard(userid))
                    elif text == "учителя":
                        base.SetTeacherId(userid,1)
                        send(userid,"Отправьте первую букву вашей фамилии",GetMainKeyboard(userid))
                    elif text in Rasp:
                        UserGroup = base.GetGroupId(userid)
                        TeacherId = base.GetTeacherId(userid)
                        if UserGroup == 0 and TeacherId == 0:
                            send(userid,"Для начала выставите название своей группы или учителя")
                        else:
                            if UserGroup != 0:
                                if text == "подписаться":
                                        base.SubToSchedule(userid)
                                        send(userid,"Вы успешно подписались",get_func_key(userid))
                                elif text == "отписаться":
                                        base.UnSubToSchedule(userid)
                                        send(userid,"Вы отписались",get_func_key(userid))
                                elif text == "опции":
                                    send(userid,"Выберите опцию",get_func_key(userid))
                                elif text == "завтра":
                                    send(userid,tpc.GetLession(base.GetGroupId(userid),datetime.today().weekday() + 2,tpc.GetWeekColor()))
                                elif text == "сегодня":
                                    send(userid,tpc.GetLession(base.GetGroupId(userid),datetime.today().weekday() + 1,tpc.GetWeekColor())) 
                                elif text == "экзамены":
                                    send(userid,tpc.GetExams(base.GetGroupId(userid)))
                                else:
                                    GoToMainMenu(userid)

                            elif TeacherId != 0:

                                if text == "подписаться":
                                        base.SubToSchedule(userid)
                                        send(userid,"Вы успешно подписались",get_func_key(userid))
                                elif text == "отписаться":
                                        base.UnSubToSchedule(userid)
                                        send(userid,"Вы отписались",get_func_key(userid))
                                elif text == "опции":
                                        send(userid,"Выберите опцию",get_func_key(userid))
                                elif text == "завтра":
                                         send(userid,tpc.GetTeacherLession(base.GetTeacherId(userid),datetime.today().weekday() + 2,tpc.GetWeekColor()))
                                elif text == "сегодня":
                                         send(userid,tpc.GetTeacherLession(base.GetTeacherId(userid),datetime.today().weekday() + 1,tpc.GetWeekColor()))
                                elif text == "экзамены":
                                        send(userid,"Скоро будет")
                                else:
                                    GoToMainMenu(userid)

                    elif fromid == 297621144 : 
                        res = CsGoSort(text)
                        if res != None:
                            send(fromid,res)
                            
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
                        return
                    commands = "хаха жопа"
                    send(fromid,commands)
                #Кик Пользователей
                elif text == "!ak" and fromid == "297621144":
                    a = isadmin(fromid,userid)
                    if a != "yes":
                        send(fromid,"Вы челядь")
                        return
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
                            return
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


while True:
        try:
            try:
                for event in longpoll.check():
                    x = threading.Thread(target=VkChecking, args=(event,))
                    x.start()
            except Exception as err:
                vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
                print(err)
                print("123123123 CRIT ERRROR 123123123")
                time.sleep(60)
        except Exception as err:
            vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
            print(err)
            print("123123123 CRIT ERRROR 123123123")
            time.sleep(60)
    