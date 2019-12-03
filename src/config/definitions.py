import configparser
import json
import os
from datetime import datetime


config = configparser.ConfigParser()

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

# cookie
COOKIE = config['BASIC']['cookie']

# behavior
config_behavior = config['BEHAVIOR']
GRANULARITY_HOUR = config_behavior.getboolean('granularity_hour')
FORCE_CRAWL = config_behavior.getboolean('force_crawl')

# common
config_common = config['COMMON']
DOLLAR_TO_CNY = float(config_common['dollar_to_cny'])
STEAM_SELL_TAX = float(config_common['steam_sell_tax'])
TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些，只爬取某个价格区间内的饰品……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
config_filter = config['FILTER']
CRAWL_MIN_PRICE_ITEM = int(config_filter['crawl_min_price_item'])
CRAWL_MAX_PRICE_ITEM = int(config_filter['crawl_max_price_item'])
MIN_SOLD_THRESHOLD = int(config_filter['min_sold_threshold'])
# https://stackoverflow.com/questions/335695/lists-in-configparser
# CATEGORY_BLACK_LIST = json.loads(config_filter['category_black_list'])

# result
TOP_N = int(config['RESULT']['top_n'])

# 文件
DATE_DAY = str(datetime.now().strftime('%Y-%m-%d'))
DATE_HOUR = str(datetime.now().strftime('%Y-%m-%d-%H'))
DATE_TIME = DATE_HOUR if GRANULARITY_HOUR else DATE_DAY

# data file
DATABASE_PATH = "database"
DATABASE_FILE = os.path.join(DATABASE_PATH, "csgo_skins_" + DATE_TIME + ".csv")
DATABASE_FILE_DAY = os.path.join(DATABASE_PATH, "csgo_skins_" + DATE_DAY + ".csv")

# log file
LOG_PATH = "log"
NORMAL_LOGGER = os.path.join(LOG_PATH, 'log_' + DATE_TIME + '.log')

# suggestion file
SUGGESTION_PATH = "suggestion"
SUGGESTION_LOGGER = os.path.join(SUGGESTION_PATH, 'suggestion_' + DATE_TIME + '.txt')
