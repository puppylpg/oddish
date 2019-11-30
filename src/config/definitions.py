import os
from datetime import datetime

COOKIES = r'_ga=GA1.2.162602080.1551374933; _ntes_nnid=8ce0cf6bdce55512e73f49cb8a49960e,1552104955025; _ntes_nuid=8ce0cf6bdce55512e73f49cb8a49960e; mail_psc_fingerprint=d80ec72871726e9b192181fd1a3633d6; usertrack=CrH5y11BrGaqLV9AAwiDAg==; vinfo_n_f_l_n3=d81bf3a25989eb31.1.2.1561837557589.1561866895199.1568433963014; __f_=1571910788620; OUTFOX_SEARCH_USER_ID_NCOO=29659292.15961449; Device-Id=33u998YqmNWbhH5GbWUo; nts_mail_user=thingsregister@163.com:-1:1; _gid=GA1.2.1251254888.1575035437; csrf_token=Ijc2ZDZlYmRlODA1NDJmYTQ4ZGE4ZWE2YzUxMzkyOWU3NjRiMGZhYmIi.EMNu-A.ubwCyN39txCV9KH1rnNjj4tvKq4; game=csgo; NTES_YD_SESS=yiLMV18d3U0I6i27zHovpGud6JHeyrHtcR.DNY0ik.Yt3iTX3xgZlsrDojmGWp5B_TiJyoEFUUBIB_pObLER1b2g51nq88XlOEdEs7mx3NIG1NXOg0FgmHe6ONZ1L96zjNndSMwD1d_HLuZ0.JanCWlbzUaxALnSGH25Kk.ubhcNKOhVzTrhtEEXugbqhxgfDcCUveGrwJfQY2SXq3BATUEgPhro6HhkecpZb8MyxPiJ9; S_INFO=1575083394|0|3&80##|18810702051; P_INFO=18810702051|1575083394|1|netease_buff|00&99|bej&1575049340&netease_buff#bej&null#10#0#0|&0|null|18810702051; session=1-5IzNgIkeFViNv9gb1zmqcLGeg-B2jH8y8tXIWWORD7HX2046524528; Locale-Supported=zh-Hans; _gat_gtag_UA_109989484_1=1'

TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

# 保存文件粒度
GRANULARITY_HOUR = True

# 强制爬取
FORCE_CRAWL = False

# 汇率
DOLLAR_TO_CNY = 7.0

# filter
# 爬取历史价格的话，每个都要单独爬一次，爬取量翻了好几十倍，所以扔掉一些……
# 大致价格分位点：0 - 10000; 20 - 5000; 50 - 4000; 100 - 3400; 200 - 3000; 500 - 2200; 1000 - 1200
CRAWL_MIN_PRICE_ITEM = 20
# buff最低价门槛，低于该价格的条目忽略（要不然统计出来很多封装的涂鸦……）
MIN_PRICE_THRESHOLD = 10
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
