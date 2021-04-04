import os
import json
import configparser
from datetime import datetime
from http.cookies import SimpleCookie


configr = configparser.RawConfigParser()

# config
CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.ini'
CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_DIR, CONFIG_FILE_NAME)

try:
    configr.read(CONFIG_PATH, encoding='utf-8')
except IOError:
    print('File {} does not exist. Exit!'.format(CONFIG_PATH))
    exit(1)

# cookie and ua
buff_cookie_simple = SimpleCookie(configr['BASIC']['buff_cookie'])
BUFF_COOKIE = { i.key:i.value for i in buff_cookie_simple.values() }

USER_AGENT = configr['BASIC']['buff_user_agent']
CONSOLE = configr['BASIC'].getboolean('console')

steam_cookie_simple = SimpleCookie(configr['BASIC']['steam_cookie'])
STEAM_COOKIE = { i.key:i.value for i in steam_cookie_simple.values() }

BUFF_USER_AGENT = configr['BASIC']["buff_user_agent"]

# proxy
PROXY = configr['BASIC']['proxy']

# behavior
config_behavior = configr['BEHAVIOR']
FREQUENCY_INTERVAL_LOW = int(config_behavior['frequency_interval_low'])
FREQUENCY_INTERVAL_HIGH = int(config_behavior['frequency_interval_high'])
URL_CACHE_HOUR = int(config_behavior['url_cache_hour'])
FORCE_CRAWL = config_behavior.getboolean('force_crawl')
RETRY_TIMES = int(config_behavior['retry_times'])

# common
config_common = configr['COMMON']
STEAM_SELL_TAX = float(config_common['steam_sell_tax'])
TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

BUFF_GOODS_LIMITED_MIN_PRICE = 0.0
# buff系统设定的最高售价，价格查询时不得高于此价格
BUFF_GOODS_LIMITED_MAX_PRICE = 150000.0

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些，只爬取某个价格区间内的饰品……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
config_filter = configr['FILTER']
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
TOP_N = int(configr['RESULT']['top_n'])

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

class config_export:
    def __init__(self):
        self.CONSOLE = CONSOLE
        self.USER_AGENT = BUFF_USER_AGENT
        self.CONFIG_DIR = CONFIG_DIR
        self.CONFIG_FILE_NAME = CONFIG_FILE_NAME
        self.CONFIG_PATH = CONFIG_PATH
        self.TIMESTAMP = TIMESTAMP
        self.BUFF_GOODS_LIMITED_MIN_PRICE = BUFF_GOODS_LIMITED_MIN_PRICE
        self.BUFF_GOODS_LIMITED_MAX_PRICE = BUFF_GOODS_LIMITED_MAX_PRICE
        self.DATE_DAY = DATE_DAY
        self.DATE_HOUR = DATE_HOUR
        self.DATE_TIME = DATE_TIME
        self.PRICE_SECTION = PRICE_SECTION
        self.LOG_PATH = LOG_PATH
        self.NORMAL_LOGGER = NORMAL_LOGGER
        self.SUGGESTION_PATH = SUGGESTION_PATH
        self.SUGGESTION_LOGGER = SUGGESTION_LOGGER
        self.CACHE_DIR = CACHE_DIR

        self.PROXY = PROXY
        self.BUFF_COOKIE = BUFF_COOKIE
        self.USER_AGENT = USER_AGENT
        self.STEAM_COOKIE = STEAM_COOKIE
        self.FREQUENCY_INTERVAL_LOW = FREQUENCY_INTERVAL_LOW
        self.FREQUENCY_INTERVAL_HIGH = FREQUENCY_INTERVAL_HIGH
        self.URL_CACHE_HOUR = URL_CACHE_HOUR
        self.FORCE_CRAWL = FORCE_CRAWL
        self.RETRY_TIMES = RETRY_TIMES
        self.STEAM_SELL_TAX = STEAM_SELL_TAX
        self.CRAWL_MIN_PRICE_ITEM = CRAWL_MIN_PRICE_ITEM
        self.CRAWL_MAX_PRICE_ITEM = CRAWL_MAX_PRICE_ITEM
        self.MIN_SOLD_THRESHOLD = MIN_SOLD_THRESHOLD
        self.CATEGORY_BLACK_LIST = CATEGORY_BLACK_LIST
        self.CATEGORY_WHITE_LIST = CATEGORY_WHITE_LIST
        self.TOP_N = TOP_N
    def save(self):
        configr['BASIC']['proxy'] = self.PROXY
        configr['BASIC']['buff_cookie'] = SimpleCookie(self.BUFF_COOKIE).output(header = '', sep=';')
        configr['BASIC']['steam_cookie'] = SimpleCookie(self.STEAM_COOKIE).output(header = '', sep=';')
        configr['FILTER']['crawl_min_price_item'] = str(int(config.CRAWL_MIN_PRICE_ITEM))
        configr['FILTER']['crawl_max_price_item'] = str(int(config.CRAWL_MAX_PRICE_ITEM))
        configr['FILTER']['category_black_list'] = json.dumps(config.CATEGORY_BLACK_LIST)
        configr['FILTER']['category_white_list'] = json.dumps(config.CATEGORY_WHITE_LIST)
        with open(os.path.join(os.getcwd(), CONFIG_DIR, CONFIG_FILE_NAME), "w+") as f:
            configr.write(f)

config = config_export()
