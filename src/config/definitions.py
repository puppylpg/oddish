import os
from datetime import datetime

# `__file__` is relative to the current working directory
# `os.chdir()` can change current working directory, but don't change `__file__`
# so if `os.chdir()` is used, this method fails to get current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
COOKIES = open(os.path.join(current_dir, 'cookie.txt'), 'r').readline().strip()

TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

# 保存文件粒度
GRANULARITY_HOUR = True

# 强制爬取
FORCE_CRAWL = False

# 汇率
DOLLAR_TO_CNY = 7.0
# steam饰品售卖税率，steam 5%，csgo 10%
STEAM_SELL_TAX = 0.15

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些，只爬取某个价格区间内的饰品……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
CRAWL_MIN_PRICE_ITEM = 100
CRAWL_MAX_PRICE_ITEM = 200
# 交易记录阈值，冷门物品不在考虑范围
MIN_SOLD_THRESHOLD = 10
# 太大都是steam定价虚高，实际卖不掉的……有了steam求购价之后就不需要这个了
MAX_GAP_PERCENTAGE = 0.8
# 每一项指标的输出个数
TOP_N = 50

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
