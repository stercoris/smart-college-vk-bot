# -*- coding: utf-8 -*-
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random 
import time
import threading
import user



# Авторизация ВК
## Проверка закрытия данных 
token = open("token.txt", "r")
vk = vk_api.VkApi(token=token.read())
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, "184728287")
# Авторизация ВК

# Запуск рассылки
# subprocess.Popen([sys.executable, 'mailing.py'])
# Запуск рассылки

def listener(event):
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            text = event.object.text.lower()
            print(f"Новое сообщение '{text}'")
            u = user.User(event.object.from_id)
            
            ## Отмена должна быть сверхуу!1
            if(text == 'отмена' or text == "главное меню"):
                u.dialstage = u.inMainMenu
                u.send("Выберите опцию")

            ## Опции и его дети (Подписки / отписки) (Сегодня / Завтра) (Экзамены)
            elif(text == "опции" and u.dialstage != u.inScheduleMenu):
                if(u.UserGroup != None):
                    u.dialstage = u.inScheduleMenu
                    u.send("Выберите опцию")
                else:
                    u.dialstage = u.inGroupSetup
                    u.send("Отправте название вашей группы")

                ## Дети "Опций"
            elif(u.dialstage == u.inScheduleMenu):
                    ## Подписки / отписки
                if(text == "подписаться"):
                    u.isSubedToSchedule = True
                    u.send("Вы успешно подписались")

                elif(text == "отписаться"):
                    u.isSubedToSchedule = False
                    u.send("Вы успешно отписались")

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
                u.send("Отправте название вашей группы")

            elif(u.dialstage == u.inGroupSetup):
                try:
                    u.UserGroup = text
                    u.dialstage = u.inScheduleMenu
                    u.send("Выберите опцию")
                except:
                    u.send("Такой группы не найдено")

    except Exception as err:
        print(err)

while True:
        try:
            try:
                for event in longpoll.check():
                    x = threading.Thread(target=listener, args=(event,))
                    x.start()
            except Exception as err:
                vk = vk_api.VkApi(token=token.read())
                print(err)
                ## Иногда пропадает соединение с сервером
        except Exception as err:
            vk = vk_api.VkApi(token=token.read())
            print(err)
            ## А иногда вырубается инет или меняется динамический ip
            time.sleep(60)
    