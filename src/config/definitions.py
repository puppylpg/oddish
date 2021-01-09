import configparser
import json
import os
from datetime import datetime


config = configparser.RawConfigParser()

# config
CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.ini'
CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_DIR, CONFIG_FILE_NAME)

try:
    config.read(CONFIG_PATH, encoding='utf-8')
except IOError:
    print('File {} does not exist. Exit!'.format(CONFIG_PATH))
    exit(1)

# `__file__` is relative to the current working directory
# `os.chdir()` can change current working directory, but don't change `__file__`
# so if `os.chdir()` is used, this method fails to get current directory
# current_dir = os.path.dirname(os.path.realpath(__file__))
# COOKIES = open(os.path.join(current_dir, 'cookie.txt'), 'r').readline().strip()

# cookie and api
BUFF_COOKIE = config['BASIC']['buff_cookie']
USER_AGENT = config['BASIC']['buff_user_agent']
STEAM_COOKIE = config['BASIC']['steam_cookie']

# proxy
PROXY = config['BASIC']['proxy']

# behavior
config_behavior = config['BEHAVIOR']
FREQUENCY_INTERVAL_LOW = int(config_behavior['frequency_interval_low'])
FREQUENCY_INTERVAL_HIGH = int(config_behavior['frequency_interval_high'])
URL_CACHE_HOUR = int(config_behavior['url_cache_hour'])
FORCE_CRAWL = config_behavior.getboolean('force_crawl')
RETRY_TIMES = int(config_behavior['retry_times'])
CRAWL_STEAM_ASYNC = config_behavior.getboolean('crawl_steam_async')

# common
config_common = config['COMMON']
STEAM_SELL_TAX = float(config_common['steam_sell_tax'])
TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
BUFF_GOODS_LIMITED_MIN_PRICE = 0.0
# buff系统设定的最高售价，价格查询时不得高于此价格
BUFF_GOODS_LIMITED_MAX_PRICE = 150000.0

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些，只爬取某个价格区间内的饰品……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
config_filter = config['FILTER']
# 最低价不小于0
CRAWL_MIN_PRICE_ITEM = max(BUFF_GOODS_LIMITED_MIN_PRICE, float(config_filter['crawl_min_price_item']))
# 最低价 <= 最高价 <= 系统最高限价
CRAWL_MAX_PRICE_ITEM = min(max(CRAWL_MIN_PRICE_ITEM, float(config_filter['crawl_max_price_item'])), BUFF_GOODS_LIMITED_MAX_PRICE)
# steam该饰品7天最低销售数
MIN_SOLD_THRESHOLD = int(config_filter['min_sold_threshold'])
# 黑白名单
CATEGORY_BLACK_LIST = json.loads(config_filter['category_black_list'])
CATEGORY_WHITE_LIST = json.loads(config_filter['category_white_list'])

# result
TOP_N = int(config['RESULT']['top_n'])

# 文件
DATE_DAY = str(datetime.now().strftime('%Y-%m-%d'))
DATE_HOUR = str(datetime.now().strftime('%Y-%m-%d-%H'))
DATE_TIME = DATE_HOUR
PRICE_SECTION = '_{}_{}'.format(CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM)

# log file
LOG_PATH = "log"
NORMAL_LOGGER = os.path.join(LOG_PATH, 'log_' + DATE_TIME + PRICE_SECTION + '.log')

# suggestion file
SUGGESTION_PATH = "suggestion"
SUGGESTION_LOGGER = os.path.join(SUGGESTION_PATH, 'suggestion_' + DATE_TIME + PRICE_SECTION + '.txt')

# cache file
CACHE_DIR = 'cache'
