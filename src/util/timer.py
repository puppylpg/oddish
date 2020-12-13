import datetime
import random
import time

from src.config.definitions import config
from src.util.logger import log


def sleep_awhile():
    low = max(config.FREQUENCY_INTERVAL_LOW, 4)
    high = max(4, config.FREQUENCY_INTERVAL_HIGH)
    interval = random.randint(low, high)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)
