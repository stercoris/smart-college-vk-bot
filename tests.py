import sqlite3
import os
import json
import ast
import user

## В какойта момент база перестала отвечать на запросы, пришлось указать абсолютный путь
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tests.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()



def getTests(find):
    cursor.execute("SELECT * FROM tests")
    tests = cursor.fetchall()
    probs = []
    for test in tests:
        for question in ast.literal_eval(test["questions"]):
            if(find.lower() in str(question["q"]).lower()):
                probs.append(question["q"])
                print(question["a"])
                print(test["name"])
    if(len(probs) > 10): raise Exception('Слишлком много вариантов')
    
    
    
    buttons = []
    for prob in probs:
            buttons.append([user.GetButton(prob[:30]+"...","secondary")])

    Keyboard = {
        "one_time": False,
        "buttons" : buttons
    }
    Keyboard = json.dumps(Keyboard, ensure_ascii=False).encode("utf-8")
    Keyboard = str(Keyboard.decode("utf-8"))
    return(Keyboard)

def refind(find):
    cursor.execute("SELECT * FROM tests")
    tests = cursor.fetchall()
    for test in tests:
        for question in ast.literal_eval(test["questions"]):
            if(find.lower()[0:-3] in str(question["q"]).lower()):
                return(test["name"])

def questToAns(name):
    cursor.execute("SELECT * FROM tests")
    tests = cursor.fetchall()
    questToAns = ""
    for test in tests:
        if(test["name"] == name):
            for question in ast.literal_eval(test["questions"]):
                normalize = ""
                for q in question["q"]:
                    normalize += f"{q}\n"
                questToAns += f"Вопрос:{normalize} \nОтвет:{question['a']}" 
    return(questToAns)
    
