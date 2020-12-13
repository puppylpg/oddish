import json
import traceback
import requests
import pandas as pd
import random
from requests import Timeout
import asyncio
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

proxies = {}
if PROXY:
    proxies["http"] = PROXY
    proxies["https"] = PROXY

def get_json_dict_raw(url, cookies, proxy = False, times = 1, steam_sleep_mode = 0):
    if exist(url):
        return fetch(url)

    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    timer.sleep_awhile(steam_sleep_mode)
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

def get_json_dict(url, cookies, proxy = False, times = 1, steam_sleep_mode = 0):
    if exist(url):
        return json.loads(fetch(url))
    json_data = get_json_dict_raw(url, cookies, proxy, times, steam_sleep_mode)

    if json_data is None:
        return None
    else:
        # can not store None
        store(url, json_data)
        return json.loads(json_data)

async def async_get_json_dict_raw(url, cookies, session: ClientSession, proxy = False, times = 1):
    if exist(url):
        return await asyncfetch(url)

    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    await timer.async_sleep_awhile(mode)
    try:
        if proxy and proxies != {}:
            return await aiohttp.request(method = "GET", url = url, headers=get_headers(), cookies=cookies, timeout=5, proxies=proxies, connector = aiohttp.TCPConnector(limit=5)).text
            # return requests.get(url, headers=get_headers(), cookies=cookies, timeout=5, proxies=proxies).text
        return await aiohttp.request(method = "GET", url = url, headers=get_headers(), cookies=cookies, timeout=5, connector = aiohttp.TCPConnector(limit=5)).text
        # return requests.get(url, headers=get_headers(), cookies=cookies, timeout=5).text

    except Timeout:
        log.warn("Timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("Unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())

    # 首次出错时异步休眠，第二次出错时全体任务休眠。
    await timer.async_sleep_awhile()
    if times == 2:
        timer.sleep_awhile()

    data = await async_get_json_dict_raw(url, cookies, session, proxy, times + 1)
    return data

async def async_get_json_dict(url, cookies, proxy = False, times = 1, mode = 0):
    if await asyncexist(url):
        return json.loads(await asyncfetch(url))
    json_data = await async_get_json_dict_raw(url, cookies, proxy, times, mode)

    if json_data is None:
        return None
    else:
        # can not store None
        await asyncstore(url, json_data)
        return json.loads(json_data)