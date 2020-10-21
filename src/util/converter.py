import json
from collections import defaultdict

import pandas as pd

from src.data.item import Item



def df_to_list(table):
    csgo_items = []

    for item in table.iterrows():
        item_id = item[0]
        item_info = item[1]

        item_name = item_info['name']
        item_price = item_info['price']
        item_sell_num = item_info['sell_num']
        item_steam_url = item_info['steam_url']
        item_steam_predict_price = item_info['steam_predict_price']
        item_buy_max_price = item_info['buy_max_price']

        # 直接构造的DataFrame，这一列是list(float)，如果是从文件反序列化的，这一列是plain string
        # 使用`json.loads`讲plain string转换为list
        history_prices = item_info['history_prices']
        item_history_prices = history_prices \
            if isinstance(history_prices, list) else json.loads(history_prices)
        item_history_days = item_info['history_days']

        part_item = Item(
            item_id,
            item_name,
            item_price,
            item_sell_num,
            item_steam_url,
            item_steam_predict_price,
            item_buy_max_price
        )
        # add history price info
        part_item.set_history_prices(item_history_prices, item_history_days)
        csgo_items.append(part_item)

    return csgo_items


def list_to_df(csgo_items):
    rows_dict = defaultdict(list)
    index = []
    for item in csgo_items:
        for k, v in item.to_dict().items():
            rows_dict[k].append(v)
        index.append(item.id)

    table = pd.DataFrame(data=rows_dict, index=index)
    pd.set_option('display.expand_frame_repr', False)

    return table
