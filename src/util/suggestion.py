from src.config.definitions import MIN_PRICE_THRESHOLD, TOP_N, MAX_GAP_PERCENTAGE
from src.util import converter

buff_to_steam_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}

steam_to_buff_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}


def suggest(table):
    print('buff买steam卖：')
    for info, column in buff_to_steam_suggestions.items():
        # buff往steam卖，steam - buff越大越好，所以最大的在前
        sort_by_column(table, info, column, ascending=False)

    print('steam买buff卖：')
    for info, column in steam_to_buff_suggestions.items():
        # steam往buff卖，steam - buff越小越好，最好是负的，所以最小的在前
        sort_by_column(table, info, column, ascending=True)


def sort_by_column(table, suggestion, column, ascending=True):
    print(suggestion)
    # filter
    higher_price = table[table['price'] >= MIN_PRICE_THRESHOLD]
    print("After threshold(price >= {}) filtered: \n{}".format(MIN_PRICE_THRESHOLD, higher_price.describe()))

    higher_price = higher_price[higher_price['gap_percent'] <= MAX_GAP_PERCENTAGE]
    print("After threshold(gap_percent <= {}) filtered: \n{}".format(MAX_GAP_PERCENTAGE, higher_price.describe()))

    if ascending:
        top = higher_price.nsmallest(TOP_N, column)
        # top = higher_price.sort_values(by=column, ascending=ascending).head(TOP_N)
    else:
        top = higher_price.nlargest(TOP_N, column)

    for item in converter.df_to_list(top):
        print(item.detail())
