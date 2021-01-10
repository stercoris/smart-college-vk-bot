import sqlite3
import requests
import json
import datetime
import os.path
import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



# Авторизация ВК
token = open("token.txt", "r")
vk = vk_api.VkApi(token=token.read())
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk, "184728287")
# Авторизация ВК


## В какойта момент база перестала отвечать на запросы, пришлось указать абсолютный путь
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tpc.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()





class GroupNotFound(Exception):
    pass

class User:

    


    def __init__(self, userid):
        self.userid = userid
        command = f"INSERT OR IGNORE INTO  VkUsers (VkId) VALUES ({userid});"
        cursor.execute(command)
        conn.commit()
        

    ## Статус выбора группы( True = выбор осуществяется, False = выбор группы не активен).
    inMainMenu = 0
    inScheduleMenu = 1
    inGroupSetup = 2
    inTestInput = 3
    inTestSelect = 4

    @property
    def dialstage(self):
        pass

    @dialstage.setter
    def dialstage(self, DialogueStatus):
        command = f"UPDATE VkUsers SET dialstage = {str(DialogueStatus)} WHERE VkId = '{str(self.userid)}'"
        cursor.execute(command)
        conn.commit()
    
    @dialstage.getter
    def dialstage(self):
        command = f"SELECT dialstage FROM VkUsers WHERE VkId = '{self.userid}'"
        cursor.execute(command)
        result = cursor.fetchone()
        return(int(result["dialstage"]))
        



    ## Группа пользователя
    @property
    def UserGroup(self):
        pass

    @UserGroup.setter
    def UserGroup(self, RawGroup):
        data = {'fname': RawGroup}
        group = requests.post('http://wrongdoor.ddns.net/college/getGroupByName/',data=data)
        try:
            group = dict(json.loads(group.text))
            command = f"UPDATE VkUsers SET GroupName = '{group['name']}',GroupId = {str(group['id'])} WHERE VkId = '{str(self.userid)}'"
            cursor.execute(command)
            conn.commit()
        except:
            raise GroupNotFound("request to server return zero")



    @UserGroup.getter
    def UserGroup(self):
        command = f"SELECT GroupName, GroupID FROM VkUsers WHERE VkId = '{self.userid}'"
        cursor.execute(command)
        result = cursor.fetchone()
        if(result["GroupName"] != None or result["GroupId"] != None):
            return(result["GroupName"], result["GroupId"])
        else: 
            return(None)

    ## Подписка на рассылку расписания
    signedToSchedule = 1
    unsignedToSchedule = 0

    @property 
    def isSubedToSchedule(self):
        pass
    
    @isSubedToSchedule.setter
    def isSubedToSchedule(self, SubStatus):
        command = f"UPDATE VkUsers SET SubToSchedule = {SubStatus} WHERE VkId = '{str(self.userid)}'"
        cursor.execute(command)
        conn.commit()

    @isSubedToSchedule.getter
    def isSubedToSchedule(self):
        command = f"SELECT SubToSchedule FROM VkUsers WHERE VkId = '{self.userid}'"
        cursor.execute(command)
        result = cursor.fetchone()
        if(result["SubToSchedule"] == self.signedToSchedule):
            return(True)
        else:
            return(False)


    

    ## Расписание
    def today(self):
        today = datetime.datetime.today().weekday() + 1
        return(today)

    def tomorrow(self):
        tomorrow = datetime.datetime.today().weekday() + 2 
        tomorrow = tomorrow if tomorrow <= 7 else 1
        return(tomorrow)

    def getSchedule(self, weekday,raw=False):
        *_, gid = self.UserGroup
        data = {'groupid': gid,'day': weekday}
        lsns = requests.post('http://wrongdoor.ddns.net/college/getLsnByGroup/',data=data)
        lsns = json.loads(lsns.text)
        if(len(lsns) == 0):
            return(None)
        else: 
            if(raw):
                return(lsns)
            
            ## Нормализация
            text = ""
            for lsn in lsns:
                text += f"{lsn['id']} - {lsn['title']}\n"
            return(text)




    
    ## Расписание 
    def getExams(self,raw=False):
        *_,gid = self.UserGroup
        data = {'groupid': gid}
        exams = requests.post('http://wrongdoor.ddns.net/college/getExamsByGroup/',data=data)
        exams = json.loads(exams.text)
        if(raw):
            return(exams)

        ## Нормализация
        text = ""
        for exam in exams:
            text += f"{exam['date']} | {exam['les']}\n{exam['teacher']} | {exam['cab']}\n-----------\n"
        return(text)


    ## Клавиатуры
    def getUserKeyboard(self):
        dialstage = self.dialstage
        if(dialstage == self.inGroupSetup):
            buttons = [
                [GetButton("Отмена","negative")]
            ]

        elif(dialstage == self.inMainMenu):
            buttons = [
                [GetButton(f"Группа","positive"),GetButton("Опции","primary")]
            ]

        elif(dialstage == self.inScheduleMenu):
            if(self.isSubedToSchedule):
                subbtn = GetButton("Отписаться","negative")
            else:
                subbtn = GetButton("Подписаться","positive")

            buttons = [
                [GetButton("Сегодня","primary"),GetButton("Завтра","primary")],
                [subbtn,GetButton("Экзамены","primary")],
                [GetButton("Главное меню","secondary")]
            ]
        Keyboard = {
            "one_time": False,
            "buttons" : buttons
            }
        Keyboard = json.dumps(Keyboard, ensure_ascii=False).encode("utf-8")
        Keyboard = str(Keyboard.decode("utf-8"))
        return(Keyboard)



    ## Отправка сообщения
    def send(self,message,keyboard=""):
        if(keyboard == ""):
            keyboard = self.getUserKeyboard()
        vk.method("messages.send",   {
                "peer_id": self.userid,
                "random_id": random.randint(1, 9999999999999999),
                "message": message,
                "keyboard": keyboard
                })



def GetButton(label, color):
    return{
        "action": {
            "type":"text",
            "label": label,
            "payload": [] #json.dumps(label) 
            },
        "color": color
        }

