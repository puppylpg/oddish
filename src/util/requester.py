import json
import traceback
import requests
import random
from requests import Timeout

<<<<<<< HEAD
from src.config.definitions import config
=======
from src.config.definitions import PROXY, BUFF_COOKIE, USER_AGENT, STEAM_COOKIE, RETRY_TIMES
>>>>>>> master
from src.util import timer
from src.util.logger import log
from src.util.cache import fetch, store, exist

import pandas as pd

# get user-agent database
csv = pd.read_csv('config/reference/ua.csv')
ua = csv.ua

<<<<<<< HEAD
=======

# get user-agent
def get_ua():
    if USER_AGENT:
        return USER_AGENT
    else:
        return get_random_ua()


>>>>>>> master
def get_random_ua():
    return ua[random.randint(0, ua.size)]

def get_headers():
    target_ua = get_ua()
    log.info('use User-Agent: {}'.format(target_ua))
    return {
        'User-Agent': target_ua
    }

<<<<<<< HEAD
def get_json_dict_raw(url, cookies = {}, proxy = False, times = 1):
=======

headers = get_headers()

proxies = {}
if PROXY:
    proxies["http"] = PROXY
    proxies["https"] = PROXY


def get_json_dict_raw(url, cookies, proxy=False, times=1):
>>>>>>> master
    if exist(url):
        return fetch(url)

    if times > config.RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, config.RETRY_TIMES))
        return None

    timer.sleep_awhile()
    try:
<<<<<<< HEAD
        if proxy and config.PROXY != {}:
            return requests.get(url, headers = get_headers(), cookies = cookies, timeout = 5, 
                proxies = { "http": config.PROXY, "https": config.PROXY }).text
        return requests.get(url, headers = get_headers(), cookies = cookies, timeout = 5).text
=======
        if proxy and proxies != {}:
            return requests.get(url, headers=headers, cookies=cookies, timeout=5, proxies=proxies).text
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).text
>>>>>>> master
    except Timeout:
        log.warn("Timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("Unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())

    data = get_json_dict_raw(url, cookies, proxy, times + 1)
    return data

def get_json_dict(url, cookies = {}, proxy = False, times = 1):
    if exist(url):
        return json.loads(fetch(url))
    json_data = get_json_dict_raw(url, cookies, proxy, times)

    if json_data is None:
        return None
    else:
        # can not store None
        store(url, json_data)
        return json.loads(json_data)
