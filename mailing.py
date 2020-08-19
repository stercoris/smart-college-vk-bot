from datetime import datetime, timedelta
from datetime import date
import requests
import time
import re
import sqlite3
import schedule
import pyowm
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


## Тут должна быть Рассылка

while True:
    schedule.run_pending()
    time.sleep(1)
