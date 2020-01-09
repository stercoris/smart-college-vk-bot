import sqlite3
import vk_api
import requests
from lxml import html
from lxml import etree
import lxml.html
import time
import re
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

conn = sqlite3.connect('tpc.db')
cursor = conn.cursor()

vk = vk_api.VkApi(token="14266f2aa070b5f57c9f88496514449211e1ad114c76edf7832732be96483b24bc59762dbba5da4956505")
 

#Новый пользователь
def AddToUserList(VkId):
    try:
        User = vk.method("users.get",  {"user_ids": str(VkId),})
    except:
        User = vk.method("users.get",  {"user_ids": str(VkId),})
    Name = User[0]["first_name"]
    try:
        SecondName = User[0]["last_name"]
    except:
        SecondName = " "
    NewUser = (
        (str(VkId),), 
        (str(Name),), 
        (str(SecondName),)
        )
    command = "INSERT OR IGNORE INTO VkUsers (VkId, Name , SecondName) VALUES (?,?,?);"
    cursor.execute(command,(str(VkId),str(Name),str(SecondName)))
    conn.commit()

def GetUser(VkId):
    command = f"SELECT VkId FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    results = cursor.fetchone()
    try:
        print(f"(Метод GetUser)Запрос : {VkId} Ответ :" + str(results))
    except:
         print("(Метод GetUser)Ответ : Нет")
    if results:
        return(True)
    else:
        return(False)

def GetAllUsersForMailing():
    command = f"SELECT VkId FROM VkUsers"
    cursor.execute(command)
    return(cursor.fetchall())

#Внесение группы пользователя в БД
def SetGroup(VkId,GroupName, GroupId):
    command = f"UPDATE VkUsers SET GroupName = '{GroupName}',GroupId = {str(GroupId)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def SetGroupId(VkId,GroupId):
    command = f"UPDATE VkUsers SET GroupId = {GroupId} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def GetGroupId(VkId):
    command = f"SELECT GroupId FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    results = cursor.fetchall()
    if results:
        return(results[0][0])
    else:
        return(False)

def GetGroupName(VkId):
    command = f"SELECT GroupName FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    results = cursor.fetchall()
    print(results)
    if results:
        return(results[0][0])
    else:
        return(False)

def GetGroup(VkId):
    command = f"SELECT GroupName FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    results = cursor.fetchall()
    if results:
        return(True)
    else:
        return(False)
#Подписка на ежедневное расписание
def SubToSchedule(VkId):
    command = f"UPDATE VkUsers SET SubToSchedule = 1 WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def UnSubToSchedule(VkId):
    command = f"UPDATE VkUsers SET SubToSchedule = 0 WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def ScheduleDialogStage(VkId, DialogStage):
    command = f"UPDATE VkUsers SET ScheduleDialogStage = {int(DialogStage)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def GetScheduleDialogStage(VkId):
    command = f"SELECT ScheduleDialogStage FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    return(cursor.fetchone()[0])

def GetSubToSchedule(VkId):
    command = f"SELECT SubToSchedule FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    return(cursor.fetchone()[0])



#Подписка на ежемесячные статы
def SubToEndMStats(VkId):
    command = f"UPDATE VkUsers SET SubToEndMStats = 1 WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def UnSubToEndMStats(VkId):
    command = f"UPDATE VkUsers SET SubToEndMStats = 0 WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def StatsDialogStage(VkId, DialogStage):
    command = f"UPDATE VkUsers SET StatsDialogStage = {int(DialogStage)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def GetStatsDialogStage(VkId):
    command = f"SELECT StatsDialogStage FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    return(cursor.fetchone()[0])

def GetSubToEndMStats(VkId):
    command = f"SELECT SubToEndMStats FROM VkUsers WHERE VkId = {VkId}"
    cursor.execute(command)
    return(cursor.fetchone()[0])

#Занесение карты пользователя в БД

def AddFirstCardId(FirstCardID,VkId):
    command = f"UPDATE VkUsers SET FirstCardID = {str(FirstCardID)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def AddSecCardId(SecCardID,VkId):
    command = f"UPDATE VkUsers SET SecCardID = {str(SecCardID)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def DayOfBirth(Day,VkId):
    command = f"UPDATE VkUsers SET Day = {str(Day)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def MonthOfBirth(Month,VkId):
    command = f"UPDATE VkUsers SET Month = {str(Month)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()

def YearOfBirth(Year,VkId):
    command = f"UPDATE VkUsers SET Year = {str(Year)} WHERE VkId = '{str(VkId)}'"
    cursor.execute(command)
    conn.commit()


#TEACHERS

def UpdateTeachers():
    url = "http://www.tpcol.ru/asu/timetableprep.php?f=1"
    response  = requests.get(url)
    response.encoding = 'cp1251'
    parsed_body = html.fromstring(response.text)
    Count = "/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table[1]//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option/@value"
    Count = parsed_body.xpath(Count)
    print(Count)
    for i in range(len(Count)):
        TeacherName = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option[{str(i)}]/text()"
        TeacherID =  f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option[{str(i)}]/@value"
        print(parsed_body.xpath(TeacherName))
        print(parsed_body.xpath(TeacherID))

# GROUPS 
def AddToGroupName(GroupName,secname, id):
    command = f"CREATE TABLE IF NOT EXISTS 'Groups' ( 'Group' TEXT NOT NULL UNIQUE)"
    cursor.execute(command)
    conn.commit()
    command = f"INSERT OR IGNORE INTO Groups ('Group') VALUES ('{GroupName}')"
    cursor.execute(command)
    conn.commit()
    command = f"CREATE TABLE  IF NOT EXISTS '{GroupName}' ( 'SecName'	TEXT NOT NULL, 'id'	TEXT NOT NULL , UNIQUE(SecName, id))"
    cursor.execute(command)
    conn.commit()
    command = f"INSERT OR IGNORE INTO {GroupName} (SecName , id ) VALUES ('{secname}' , '{id}')"
    cursor.execute(command)
    conn.commit()
    command = f"UPDATE {GroupName} SET  id = '{id}' Where SecName = '{secname}'"
    cursor.execute(command)
    conn.commit()

def UpdateGroups():
    url = "http://www.tpcol.ru/asu/timetablestud.php?f=0"
    response  = requests.get(url)
    response.encoding = 'cp1251'
    parsed_body = html.fromstring(response.text)
    Count = "/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option"
    Count = parsed_body.xpath(Count)
    for i in range(len(Count)):
        if(i == 1 or i == 0):
            continue
        GroupNameAndId = f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option[{str(i)}]/text()"
        GroupId =  f"/html/body/table//tr[1]/td[2]/table[2]//tr[1]/td[2]/table//tr/td/table//tr[2]/td/table//tr/td[2]/form/table//tr[1]/td[2]/select/option[{str(i)}]/@value"
        GroupNameAndId = (parsed_body.xpath(GroupNameAndId))
        GroupId = (parsed_body.xpath(GroupId))
        GroupName = ((GroupNameAndId[0]).split("-"))[0]
        SecName = ((GroupNameAndId[0]).split("-"))[1]
        print("MainName: " + GroupName.lower() + "   SubName: " +  SecName + " ID: " + GroupId[0])
        GroupId = GroupId[0].replace(' ', '').lower()
        GroupName = GroupName.replace(' ', '').lower()
        SecName = SecName.replace(' ', '').lower()

        if(GroupName == "зст" or GroupName == "зтм"):
            continue
        AddToGroupName(GroupName, SecName ,  GroupId)
def GetGroupByName(Group):
    s  = Group
    for d in '1234567890-':
        s=s.replace(d, '')
        s.strip(' ')
    while s.find(' ') != -1:
        s = s.replace(' ', '')
    GroupMN = s.lower()
    s  = Group
    GroupSecN = re.sub(r'[^0-9]+', r'', s)
    command = f"SELECT * FROM Groups"
    cursor.execute(command)
    id = 0
    groups = cursor.fetchall()
    for DBgroup in groups:
        if(DBgroup[0] == GroupMN):
            command = f"SELECT SecName , id FROM {DBgroup[0]}"
            cursor.execute(command)
            SecNames = cursor.fetchall()
            for SecName in SecNames:
                if(SecName[0] == GroupSecN):
                    id = SecName[1]
                    return(id)
    return(id)
