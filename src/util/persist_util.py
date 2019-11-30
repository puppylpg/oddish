import os

import pandas as pd

from src.config.definitions import OUTPUT_FILE_NAME, OUTPUT_PATH, OUTPUT_FILE_NAME_DAY, GRANULARITY_HOUR
from src.util import converter


def tabulate(csgo_items):

    table = converter.list_to_df(csgo_items)
    table_info(table)

    # mkdir if not exist
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    # save to file
    table.to_csv(OUTPUT_FILE_NAME, encoding='utf-8')
    # when saving file hourly, save a file daily too
    if GRANULARITY_HOUR:
        table.to_csv(OUTPUT_FILE_NAME_DAY, encoding='utf-8', mode='w')

    return table


def load():
    table = pd.read_csv(OUTPUT_FILE_NAME, encoding='utf-8')
    table_info(table)
    return table


def table_info(table):
    print(table)
    print(table.describe())
