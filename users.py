import sqlite3
import user
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tpc.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

class Users:
    
    def subbed(self):
        command = f"SELECT * FROM VkUsers WHERE (SubToSchedule = 1)"
        cursor.execute(command)
        result = cursor.fetchall()
        subbed = []
        for u in result:
            subbed.append(user.User(u["VkID"]))
        return(subbed)
        
        
