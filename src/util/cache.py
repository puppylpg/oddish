import os
import time
import hashlib
from src.config.definitions import CACHE_DIR, FORCE_CRAWL, GRANULARITY_HOUR

cache_root = os.path.join(os.getcwd(), CACHE_DIR)
if not os.path.exists(cache_root):
    os.mkdir(cache_root)

def exist(url):
    if FORCE_CRAWL:
        return False

    urlid = hashlib.sha1(url.encode("utf-8")).hexdigest()
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= GRANULARITY_HOUR

def fetch(url):
    urlid = hashlib.sha1(url.encode("utf-8")).hexdigest()
    with open(os.path.join(cache_root, urlid), "r") as f:
        return f.read()

def store(url, data):
    urlid = hashlib.sha1(url.encode("utf-8")).hexdigest()
    f = open(os.path.join(cache_root,urlid), "w")
    f.write(data)
    f.close()
