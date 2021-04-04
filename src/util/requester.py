import csv
import json
import traceback
import requests
import random
from requests import Timeout
from aiohttp import ClientSession

from src.config.definitions import config
from src.util import timer
from src.util.logger import log
from src.util.cache import fetch, store, exist, asyncexist, asyncfetch, asyncstore

# get user-agent database
f = open('config/reference/ua.csv')
csv = csv.DictReader(f)
ua = []
for k in csv:
    ua.append(k['ua'])
f.close()

# get user-agent
def get_random_ua():
    return ua[random.randint(0, len(ua))]

def get_ua():
    if config.USER_AGENT:
        return config.USER_AGENT
    else:
        return get_random_ua()

def get_headers():
    target_ua = get_ua()
    # log.info('use User-Agent: {}'.format(target_ua))
    return {
        'User-Agent': target_ua
    }

def get_json_dict_raw(url, cookies = {}, proxy = False, times = 1, is_steam_request = 0):
    headers = get_headers()

    if times > config.RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, config.RETRY_TIMES))
        return None

    try:
        if proxy and config.PROXY != {}:
            return requests.get(url, headers = headers, cookies = cookies, timeout = 5, 
                proxies = { "http": config.PROXY, "https": config.PROXY }).text
        return requests.get(url, headers = headers, cookies = cookies, timeout = 5).text
    except Timeout:
        log.warn("Timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("Unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())

    data = get_json_dict_raw(url, cookies, proxy, times + 1)
    return data

def get_json_dict(url, cookies = {}, proxy = False, times = 1, is_steam_request = 0):
    if exist(url):
        return json.loads(fetch(url))
    json_data = get_json_dict_raw(url, cookies, proxy, times, is_steam_request)

    if json_data is None:
        return None
    else:
        # can not store None
        store(url, json_data)
        return json.loads(json_data)

async def async_get_json_dict_raw(url, cookies, session: ClientSession, proxy = False, times = 1):
    if times > config.RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, config.RETRY_TIMES))
        return None

    try:
        async with session.get(url) as resp:
            return await resp.text()
        # return requests.get(url, headers=get_headers(), cookies=cookies, timeout=5).text
    except Timeout:
        log.warn("Timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("Unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())

    # 首次出错时异步休眠，第二次出错时全体任务休眠。
    await timer.async_sleep_awhile()
    if times == 2:
        log.error('aio http error happens 2 times. use sync wait')
        timer.sleep_awhile()

    data = await async_get_json_dict_raw(url, cookies, session, proxy, times + 1)
    return data

async def async_get_json_dict(url, cookies, session, proxy = False, times = 1):
    if await asyncexist(url):
        return json.loads(await asyncfetch(url))
    json_data = await async_get_json_dict_raw(url, cookies, session, proxy, times)

    if json_data is None:
        return None
    else:
        # can not store None
        await asyncstore(url, json_data)
        return json.loads(json_data)
