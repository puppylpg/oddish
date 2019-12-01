import requests
from requests import Timeout

from src.config.definitions import COOKIES
from src.util import timer

cookie_str = COOKIES
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
        return requests.get(url, headers=headers, cookies=cookies).json()
    except Timeout:
        print("timeout for {}".format(url))
        return None
