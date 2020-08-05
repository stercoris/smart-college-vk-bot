import sqlite3
import requests
import json
import datetime

conn = sqlite3.connect('tpc.db',check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

class User:

    


    def __init__(self, userid, name, secname):
        self.userid = userid
        
        command = f"INSERT OR IGNORE INTO  VkUsers (VkId, Name , SecondName) VALUES ({userid},'{name}','{secname}');"
        cursor.execute(command)
        conn.commit()
        

    ## Статус выбора группы( 1 = выбор осуществяется, 0 = выбор группы не активен).
    dialogueStart = 1
    dialogueEnd = 0

    @property
    def isInGroupSetup(self):
        self.isInDiaologue = None

    @isInGroupSetup.setter
    def isInGroupSetup(self, DialogueStatus):
        command = f"UPDATE VkUsers SET isingroupsetup = {str(DialogueStatus)} WHERE VkId = '{str(self.userid)}'"
        cursor.execute(command)
        conn.commit()
    
    @isInGroupSetup.getter
    def isInGroupSetup(self):
        command = f"SELECT isingroupsetup FROM VkUsers WHERE VkId = '{self.userid}'"
        cursor.execute(command)
        result = cursor.fetchone()
        if( int(result["isingroupsetup"]) == self.dialogueStart):
            return (True)
        else:
            return(False)



    ## Группа пользователя
    @property
    def UserGroup(self):
        self.UserGroup = None

    @UserGroup.setter
    def UserGroup(self, RawGroup):
        data = {'fname': RawGroup}
        group = requests.post('http://wrongdoor.ddns.net/college/getGroupByName/',data=data)
        group = dict(json.loads(group.text))
        command = f"UPDATE VkUsers SET GroupName = '{group['name']}',GroupId = {str(group['id'])} WHERE VkId = '{str(self.userid)}'"
        cursor.execute(command)
        conn.commit()

    @UserGroup.getter
    def UserGroup(self):
        command = f"SELECT GroupName, GroupID FROM VkUsers WHERE VkId = '{self.userid}'"
        cursor.execute(command)
        result = cursor.fetchone()
        return(result["GroupName"], result["GroupId"])

    ## Подписка на рассылку расписания
    signedToSchedule = 1
    unsignedToSchedule = 0

    @property 
    def isSubedToSchedule(self):
        self.isSubedToSchedule = None
    
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

    today = datetime.datetime.today().weekday() + 1
    tomorrow = datetime.datetime.today().weekday() + 2 
    tomorrow = tomorrow if tomorrow <= 7 else 1

    
    def getSchedule(self, weekday):
        *_, gid = self.UserGroup
        print(gid)

        data = {'groupid': gid,'day': weekday}
        lsns = requests.post('http://wrongdoor.ddns.net/college/getLsnByGroup/',data=data)
        lsns = json.loads(lsns.text)
        return(lsns)

    
    ## Расписание 
    def getExams(self):
        *_,gid = self.UserGroup

        data = {'groupid': gid}
        exams = requests.post('http://wrongdoor.ddns.net/college/getExamsByGroup/',data=data)
        print(exams)
        exams = json.loads(exams.text)
        return(exams)





## "ЮНИТ" Тесты!!

user = User(297621144, "Дмитртий", "Родин")


print("Подписан на расписание?")
user.isSubedToSchedule = user.signedToSchedule
print(user.isSubedToSchedule)

print("Группа пользователя('вп31')")
user.UserGroup = "вп31"
gname, id = user.UserGroup
print(gname)
print(id)

print("В стадии диалога изменения группы?")
print(user.isInGroupSetup)


print("Расписание : ")
print(user.getSchedule(user.today))

print("Экзамены : ")
print(user.getExams())
