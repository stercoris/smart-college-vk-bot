# -*- coding: utf-8 -*-
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random 
import time
import threading
import user

# Авторизация ВК
vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, "184728287")
# Авторизация ВК

# Запуск рассылки
# subprocess.Popen([sys.executable, 'mailing.py'])
# Запуск рассылки

error = ["Ашибка", "Еррор", "Ошибка", "Оплошность","просчет"]
admin = ["ніяк, прав немає" , "Прав нет да", "Прав а", "Можно права?", "Никак","Дайб прав"]
ZvonKi = '1 : 8:30 - 10:00  \n 2 : 10:20 - 11:50 \n 3 : 12:20 - 13:50 \n 4 : 14:00 - 15:30 \n 5 : 15:40 - 17:10'

def VkChecking(event):
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            text = event.object.text.lower()
            print(f"Новое сообщение '{text}'")
            u = user.User(event.object.from_id)
            
            ## Отмена должна быть сверхуу!1
            if(text == 'отмена' or text == "главное меню"):
                u.dialstage = u.inMainMenu
                u.send("Выберите опцию",u.getUserKeyboard())

            ## Опции и его дети (Подписки / отписки) (Сегодня / Завтра) (Экзамены)
            elif(text == "опции" and u.dialstage != u.inScheduleMenu):
                if(u.UserGroup != None):
                    u.dialstage = u.inScheduleMenu
                    u.send("Выберите опцию",u.getUserKeyboard())
                else:
                    u.dialstage = u.inGroupSetup
                    u.send("Отправте название вашей группы", u.getUserKeyboard())

                ## Дети "Опций"
            elif(u.dialstage == u.inScheduleMenu):
                    ## Подписки / отписки
                if(text == "подписаться"):
                    u.isSubedToSchedule = True
                    u.send("Вы успешно подписались",u.getUserKeyboard())

                elif(text == "отписаться"):
                    u.isSubedToSchedule = False
                    u.send("Вы успешно отписались",u.getUserKeyboard())

                    ## Расписание по дням
                elif(text == "сегодня"):
                    lsns = u.getSchedule(u.today)
                    u.send(lsns if lsns != None else "Расписания на сегодня нема")
                elif(text == "завтра"):
                    lsns = u.getSchedule(u.tomorrow)
                    u.send(lsns if lsns != None else "Расписания на завтра нема!")

                    ## Экзамены
                elif(text == "экзамены"):
                    u.send(u.getExams())


            ## Установка группы
            elif(text == 'группа' and u.dialstage != u.inGroupSetup):
                u.dialstage = u.inGroupSetup
                u.send("Отправте название вашей группы", u.getUserKeyboard())

            elif(u.dialstage == u.inGroupSetup):
                try:
                    u.UserGroup = text
                    u.dialstage = u.inScheduleMenu
                    u.send("Выберите опцию",u.getUserKeyboard())
                except:
                    u.send("Такой группы не найдено")

    except Exception as err:
        print(err)

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
        except Exception as err:
            vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
            print(err)
            print("123123123 CRIT ERRROR 123123123")
            time.sleep(60)
    