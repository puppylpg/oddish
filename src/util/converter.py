from collections import defaultdict

from src.data.item import Item

import pandas as pd


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

        csgo_items.append(
            Item(
                item_id,
                item_name,
                item_price,
                item_sell_num,
                item_steam_url,
                item_steam_predict_price,
                item_buy_max_price
            )
        )

    return csgo_items


def list_to_df(csgo_items):
    rows_dict = defaultdict(list)
    index = []
    for item in csgo_items:
        [rows_dict[k].append(v) for k, v in item.to_dict().items()]
        index.append(item.id)

    table = pd.DataFrame(data=rows_dict, index=index)
    pd.set_option('display.expand_frame_repr', False)

    return table
