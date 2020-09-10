import requests
from requests import Timeout
import traceback

from src.config.definitions import PROXY, BUFF_COOKIE, STEAM_COOKIE, RETRY_TIMES
from src.util import timer
from src.util.logger import log

buff_cookie_str = BUFF_COOKIE
buff_cookies = {}
for line in buff_cookie_str.split(';'):
    k, v = line.split('=', 1)
    buff_cookies[k] = v

steam_cookie_str = STEAM_COOKIE
steam_cookies = {}
for line in steam_cookie_str.split(';'):
    k, v = line.split('=', 1)
    steam_cookies[k] = v

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}
proxies = {
    "http":PROXY,"https":PROXY
}


def get_json_dict(url, cookies, proxy=False, times=1):
    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    timer.sleep_awhile()
    try:
        if proxy:
            return requests.get(url, headers=headers, cookies=cookies, timeout=5, proxies=proxies).json()
        else:
            return requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
    except Timeout:
        log.warn("timeout for {}. Try again.".format(url))
    except Exception as e:
        log.error("unknown error for {}. Try again. Error string: {}".format(url, e))
        log.error(traceback.format_exc())
    return get_json_dict(url, cookies, proxy, times + 1)
