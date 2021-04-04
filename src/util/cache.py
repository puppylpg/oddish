# import asyncio
import os
import time
import json
import hashlib
from src.config.definitions import config
import aiofiles
from src.util.logger import log

cache_root = os.path.join(os.getcwd(), config.CACHE_DIR)
if not os.path.exists(cache_root):
    os.mkdir(cache_root)

def vaild_json(js):
    try:
        json_object = json.loads(js)
        if (json_object == []) or ('error' in json_object):
            return False
    except ValueError as e:
        return False
    return True

def url_id(url):
    return hashlib.sha1(url.encode("utf-8")).hexdigest()

def exist(url):
    if config.FORCE_CRAWL:
        return False

    urlid = url_id(url)
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    with open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        if not vaild_json(f.read()):
            return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= config.URL_CACHE_HOUR

async def asyncexist(url):
    if config.FORCE_CRAWL:
        return False

    urlid = url_id(url)
    if not os.path.exists(os.path.join(cache_root,urlid)):
        return False
    async with aiofiles.open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        if not vaild_json(await f.read()):
            return False
    mtime = os.path.getmtime(os.path.join(cache_root,urlid))
    return (time.time() - mtime) / 3600 <= config.URL_CACHE_HOUR

def fetch(url):
    urlid = url_id(url)
    log.info('Successful attempt to fetch from {}'.format(urlid))
    with open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        return f.read()

async def asyncfetch(url):
    urlid = url_id(url)
    log.info('Successful attempt to fetch from {}'.format(urlid))
    async with aiofiles.open(os.path.join(cache_root, urlid), "r", encoding='utf-8') as f:
        return await f.read()

def store(url, data):
    if exist(url):
        return
    urlid = url_id(url)
    f = open(os.path.join(cache_root,urlid), "w", encoding='utf-8')
    f.write(data)
    f.close()

async def asyncstore(url, data):
    if await asyncexist(url):
        return
    urlid = url_id(url)
    async with aiofiles.open(os.path.join(cache_root,urlid), "w", encoding='utf-8') as f:
        await f.write(data)
