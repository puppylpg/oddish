import os
from collections import defaultdict

import pandas as pd

from src.config.definitions import OUTPUT_FILE_NAME, OUTPUT_PATH, OUTPUT_FILE_NAME_DAY, GRANULARITY_HOUR


def tabulate(csgo_items):
    rows_dict = defaultdict(list)
    index = []
    for item in csgo_items:
        [rows_dict[k].append(v) for k, v in item.to_dict().items()]
        index.append(item.id)

    table = pd.DataFrame(data=rows_dict, index=index)
    pd.set_option('display.expand_frame_repr', False)
    table_info(table)

    # mkdir if not exist
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    # save to file
    table.to_csv(OUTPUT_FILE_NAME, encoding='utf-8')
    # when saving file hourly, save a file daily too
    if GRANULARITY_HOUR:
        table.to_csv(OUTPUT_FILE_NAME_DAY, encoding='utf-8', mode='w')


def load():
    table = pd.read_csv(OUTPUT_FILE_NAME, encoding='utf-8')
    table_info(table)
    return table


def table_info(table):
    print(table)
    print(table.describe())
