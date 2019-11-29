import random
import time


def sleep_awhile():
    interval = random.randint(1, 2)
    print("sleep {}s".format(interval))
    time.sleep(interval)
