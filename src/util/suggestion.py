from src.config.definitions import TOP_N, MIN_SOLD_THRESHOLD
from src.util import converter
from src.util.logger import suggestion_log

buff_to_steam_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}

steam_to_buff_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}


def suggest(table):
    suggestion_log.info('buff买steam卖：\n')
    for info, column in buff_to_steam_suggestions.items():
        # buff往steam卖，steam - buff越大越好，所以最大的在前
        sort_by_column(table, info, column, ascending=False)

    suggestion_log.info('steam买buff卖：\n')
    for info, column in steam_to_buff_suggestions.items():
        # steam往buff卖，steam - buff越小越好，最好是负的，所以最小的在前
        sort_by_column(table, info, column, ascending=True)


def sort_by_column(table, suggestion, column, ascending=True):
    suggestion_log.info(suggestion + "\n")

    # filter
    filtered_table = filter_table(table)

    if ascending:
        top = filtered_table.nsmallest(TOP_N, column)
        # top = higher_price.sort_values(by=column, ascending=ascending).head(TOP_N)
    else:
        top = filtered_table.nlargest(TOP_N, column)

    suggestion_log.info('收益降序：')
    for item in converter.df_to_list(top):
        suggestion_log.info(item.detail())
    suggestion_log.info('\n')


def filter_table(table):

    # due to steam average history price is used!
    # table = table[table['gap_percent'] <= MAX_GAP_PERCENTAGE]
    # suggestion_log.info("After threshold(gap_percent <= {}) filtered: \n{}".format(MAX_GAP_PERCENTAGE, table.describe()))

    table = table[table['history_sold'] >= MIN_SOLD_THRESHOLD]
    suggestion_log.info("After threshold(history_sold >= {}) filtered: \n{}\n".format(MIN_SOLD_THRESHOLD, table.describe()))

    return table
