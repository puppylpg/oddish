import os

import pandas as pd

from src.config.definitions import DATABASE_FILE, DATABASE_PATH, DATABASE_FILE_DAY, GRANULARITY_HOUR
from src.util import converter
from src.util.logger import log


def tabulate(csgo_items):

    if len(csgo_items) != 0:
        # persist data
        table = converter.list_to_df(csgo_items)
        table_info(table)

        # mkdir if not exist
        if not os.path.exists(DATABASE_PATH):
            os.makedirs(DATABASE_PATH)
        # save to file
        table.to_csv(DATABASE_FILE, encoding='utf-8')
        # when saving file hourly, save a file daily too
        if GRANULARITY_HOUR:
            table.to_csv(DATABASE_FILE_DAY, encoding='utf-8', mode='w')

        return table
    else:
        return None


def load():
    table = pd.read_csv(DATABASE_FILE, encoding='utf-8')
    table_info(table)
    return table


def table_info(table):
    log.info(table)
    log.info(table.describe())
