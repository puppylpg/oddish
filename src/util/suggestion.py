import heapq
from src.config.definitions import config
from src.util.logger import suggestion_log

standard = {
    '单位价钱收益': 'gap_percent',
    '差价': 'gap'
}


def suggest(table):
    suggestion_log.info('Buff买Steam卖：\n')
    for info, column in standard.items():
        # buff往steam卖，steam - buff越大越好，所以最大的在前
        sort_by_column(table, info, column, ascending=False)

    suggestion_log.info('Steam买Buff卖：\n')
    for info, column in standard.items():
        # steam往buff卖，steam - buff越小越好，最好是负的，所以最小的在前
        sort_by_column(table, info, column, ascending=True)


def sort_by_column(table, suggestion, column, ascending=True):
    filtered_table = filter_table(table)

    if ascending:
        top = heapq.nsmallest(config.TOP_N, table, key = lambda s: getattr(s, column))
    else:
        top = heapq.nlargest(config.TOP_N, table, key = lambda s: getattr(s, column))

    suggestion_log.info(suggestion + '降序：')
    for item in top:
        suggestion_log.info(item.detail())
    suggestion_log.info('\n')


def filter_table(table):
    return [x for x in table if getattr(x, 'history_sold') >= config.MIN_SOLD_THRESHOLD]
