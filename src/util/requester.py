import json
import traceback
import requests
import pandas as pd
import random
from requests import Timeout
from aiohttp import ClientSession

from src.config.definitions import PROXY, BUFF_COOKIE, USER_AGENT, STEAM_COOKIE, RETRY_TIMES
from src.util import timer
from src.util.logger import log
from src.util.cache import fetch, store, exist, asyncexist, asyncfetch, asyncstore

buff_cookie_str = BUFF_COOKIE
buff_cookies = {}
for line in buff_cookie_str.split(';'):
    if len(line) == 0:
        break
    k, v = line.split('=', 1)
    buff_cookies[k] = v

steam_cookie_str = STEAM_COOKIE
steam_cookies = {}
for line in steam_cookie_str.split(';'):
    if len(line) == 0:
        break
    k, v = line.split('=', 1)
    k = k.lstrip()
    steam_cookies[k] = v

# get user-agent database
csv = pd.read_csv('config/reference/ua.csv')
ua = csv.ua


# get user-agent
def get_ua():
    if USER_AGENT:
        return USER_AGENT
    else:
        return get_random_ua()


def get_random_ua():
    return ua[random.randint(0, ua.size)]


def get_headers():
    target_ua = get_ua()
    log.info('use User-Agent: {}'.format(target_ua))
    return {
        'User-Agent': target_ua
    }


headers = get_headers()

proxies = {}
if PROXY:
    proxies["http"] = PROXY
    proxies["https"] = PROXY

def get_json_dict_raw(url, cookies, proxy = False, times = 1, is_steam_request = 0):
    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    timer.sleep_awhile(is_steam_request)
    try:
        if proxy and proxies != {}:
            return requests.get(url, headers=headers, cookies=cookies, timeout=5, proxies=proxies).text
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).text
    except Timeout:
        log.warn("Timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("Unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())

    data = get_json_dict_raw(url, cookies, proxy, times + 1)
    return data

def get_json_dict(url, cookies, proxy = False, times = 1, is_steam_request = 0):
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
    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
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