import os
from datetime import datetime

# `__file__` is relative to the current working directory
# `os.chdir()` can change current working directory, but don't change `__file__`
# so if `os.chdir()` is used, this method fails to get current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
COOKIES = open(os.path.join(current_dir, 'cookie.txt'), 'r').readline().strip()

TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

# 保存文件粒度
GRANULARITY_HOUR = False

# 强制爬取
FORCE_CRAWL = False

# 汇率
DOLLAR_TO_CNY = 7.0
# steam视频售卖税率
STEAM_SELL_TAX = 0.13

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些，只爬取某个价格区间内的饰品……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
CRAWL_MIN_PRICE_ITEM = 100
CRAWL_MAX_PRICE_ITEM = 300
# buff最低价门槛，低于该价格的条目忽略（要不然统计出来很多封装的涂鸦……）
MIN_PRICE_THRESHOLD = 100
# 交易记录阈值，冷门物品不在考虑范围
MIN_SOLD_THRESHOLD = 10
# 太大都是steam定价虚高，实际卖不掉的……有了steam求购价之后就不需要这个了
MAX_GAP_PERCENTAGE = 0.8
# 每一项指标的输出个数
TOP_N = 50

# 文件
DATE_DAY = str(datetime.now().strftime('%Y-%m-%d'))
DATE_HOUR = str(datetime.now().strftime('%Y-%m-%d-%H'))
OUTPUT_PATH = "output"
OUTPUT_NAME_HOUR = "csgo_skins_" + DATE_HOUR
OUTPUT_NAME_DAY = "csgo_skins_" + DATE_DAY
OUTPUT_NAME = OUTPUT_NAME_HOUR if GRANULARITY_HOUR else OUTPUT_NAME_DAY

OUTPUT_FILE_NAME = os.path.join(
    OUTPUT_PATH, OUTPUT_NAME + ".csv"
)
OUTPUT_FILE_NAME_DAY = os.path.join(
    OUTPUT_PATH, OUTPUT_NAME_DAY + ".csv"
)
