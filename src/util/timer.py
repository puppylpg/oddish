import datetime
import random
import time


def sleep_awhile():
    interval = random.randint(1, 2)
    print("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)
