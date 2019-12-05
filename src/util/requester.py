import requests
from requests import Timeout

from src.config.definitions import COOKIE, RETRY_TIMES
from src.util import timer
from src.util.logger import log

cookie_str = COOKIE
cookies = {}
for line in cookie_str.split(';'):
    k, v = line.split('=', 1)
    cookies[k] = v

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}


def get_json_dict(url, times=1):
    if times > RETRY_TIMES:
        log.error('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, RETRY_TIMES))
        return None

    timer.sleep_awhile()
    try:
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
    except Timeout:
        log.warn("timeout for {}. Try again.".format(url))
        return get_json_dict(url, times + 1)
