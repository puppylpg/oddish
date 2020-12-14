import datetime
import random
import time
import asyncio

from src.config.definitions import FREQUENCY_INTERVAL_LOW, FREQUENCY_INTERVAL_HIGH
from src.util.logger import log


def sleep_awhile(mode = 0):
    low = max(FREQUENCY_INTERVAL_LOW, 2)
    high = max(2, FREQUENCY_INTERVAL_HIGH)
    if mode == 1:
        interval = 1/(random.randint(5, 10))
    else:
        interval = random.randint(low, high)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    time.sleep(interval)

async def async_sleep_awhile(mode = 0):
    low = max(FREQUENCY_INTERVAL_LOW, 2)
    high = max(2, FREQUENCY_INTERVAL_HIGH)
    if mode == 1:
        interval = 1/(random.randint(5, 10))
    else:
        interval = random.randint(low, high)
    log.info("sleep {}s at {}".format(interval, datetime.datetime.now()))
    await asyncio.sleep(interval)
