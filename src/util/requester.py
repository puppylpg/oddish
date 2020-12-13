import json
import traceback
import requests
from requests import Timeout

from src.config.definitions import config
from src.util.logger import log
from src.util.cache import fetch, store, exist
from src.util import timer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}

def get_json_dict_raw(url, cookies = {}, proxy = False, times = 1):
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

def get_json_dict(url, cookies = {}, proxy = False, times = 1):
    if exist(url):
        return json.loads(fetch(url))

    json_data = get_json_dict_raw(url, cookies, proxy, times)
    timer.sleep_awhile()

    if json_data is None:
        return None
    else:
        # can not store None
        store(url, json_data)
        return json.loads(json_data)
