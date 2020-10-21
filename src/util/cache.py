import os
import time
import hashlib
from src.config.definitions import CACHE_DIR, FORCE_CRAWL, URL_CACHE_HOUR
from src.util.logger import log

cache_root = os.path.join(os.getcwd(), CACHE_DIR)
if not os.path.exists(cache_root):
    os.mkdir(cache_root)

def url_id(url):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

def exist(url):
    if FORCE_CRAWL:
        return False

    urlid = url_id(url)
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= URL_CACHE_HOUR

def fetch(url):
    urlid = url_id(url)
    log.info('Successful attempt to fetch from {}'.format(urlid))
    with open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        return f.read()

def store(url, data):
    urlid = url_id(url)
    f = open(os.path.join(cache_root,urlid), "w", encoding='utf-8')
    f.write(data)
    f.close()
