import datetime
import random
import time

from src.config.definitions import FREQUENCY_INTERVAL_LOW, FREQUENCY_INTERVAL_HIGH
from src.util.logger import log


def sleep_awhile():
    low = max(FREQUENCY_INTERVAL_LOW, 2)
    high = max(2, FREQUENCY_INTERVAL_HIGH)
    interval = random.randint(low, high)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)
