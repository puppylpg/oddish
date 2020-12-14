import asyncio
import os
import time
import json
import hashlib
import aiofiles
from src.config.definitions import CACHE_DIR, FORCE_CRAWL, URL_CACHE_HOUR
from src.util.logger import log

cache_root = os.path.join(os.getcwd(), CACHE_DIR)
if not os.path.exists(cache_root):
    os.mkdir(cache_root)

def is_json(js):
    try:
        json_object = json.loads(js)
    except ValueError as e:
        return False
    return True

def url_id(url):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

def exist(url):
    if FORCE_CRAWL:
        return False

    urlid = url_id(url)
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    with open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        if not is_json(f.read()):
            return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= URL_CACHE_HOUR

async def asyncexist(url):
    if FORCE_CRAWL:
        return False

    urlid = url_id(url)
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    async with aiofiles.open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        if not is_json(await f.read()):
            return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= URL_CACHE_HOUR

def fetch(url):
    urlid = url_id(url)
    log.info('Successful attempt to fetch from {}'.format(urlid))
    with open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        return f.read()

async def asyncfetch(url):
    urlid = url_id(url)
    log.info('Successful attempt to fetch from {}'.format(urlid))
    with aiofiles.open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        return await f.read()

def store(url, data):
    if exist(url):
        return
    urlid = url_id(url)
    f = open(os.path.join(cache_root,urlid), "w", encoding='utf-8')
    f.write(data)
    f.close()

async def asyncstore(url, data):
    if asyncexist(url):
        return
    urlid = url_id(url)
    async with aiofiles.open(os.path.join(cache_root,urlid), "w", encoding='utf-8') as f:
        await f.write(data)
