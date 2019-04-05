import schedule
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import threading
import subprocess
import sys
import os
from threading import Timer

from utils import sync,connect

# change path of config file if required
# print(sys.path)
filepath = 'config.json'
with open(filepath) as f :
    data = json.load(f)

# time interval in seconds
sec = int(data["interval"])
print(sec)

sched = BlockingScheduler()

def job():
    print("Syncing....")
    sched.add_job(sync.main, 'interval', seconds = sec)
    sched.start()
    

thread1 = threading.Thread(target=job,name="thread1")

thread2 = threading.Thread(target=connect.main,name="thread2")

thread1.start()
thread2.start()

thread1.join()