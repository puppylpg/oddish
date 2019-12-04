import requests
from requests import Timeout

from src.config.definitions import COOKIE
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


def get_json_dict(url):
    timer.sleep_awhile()
    try:
        return requests.get(url, headers=headers, cookies=cookies, timeout=5).json()
    except Timeout:
        log.error("timeout for {}. SKIP.".format(url))
        return None
