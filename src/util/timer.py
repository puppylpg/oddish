import datetime
import random
import time

from src.util.logger import log


def sleep_awhile():
    interval = random.randint(1, 2)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)
