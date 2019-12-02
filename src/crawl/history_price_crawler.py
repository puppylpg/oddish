from src.config.definitions import DOLLAR_TO_CNY
from src.config.urls import BUFF_HISTORY_PRICE, BUFF_HISTORY_PRICE_CNY
from src.util import requester
from src.util.logger import log


def steam_price_history_url(item_id):
    """7 days history prices"""
    return BUFF_HISTORY_PRICE + 'game=csgo&goods_id={}&currency=&days=7'.format(item_id)


def buff_price_history_url(item_id):
    return BUFF_HISTORY_PRICE_CNY + 'game=csgo&goods_id={}&currency=CNY&days=7'.format(item_id)


def crawl_item_history_price(index, item, total_price_number):
    history_prices = []

    item_id = item.id
    steam_price_url = steam_price_history_url(item_id)
    log.info('GET steam history price {}/{} for ({}): {}'.format(index, total_price_number, item.name, steam_price_url))
    steam_history_prices = requester.get_json_dict(steam_price_url)

    if steam_history_prices is not None:
        days = steam_history_prices['data']['days']
        raw_price_history = steam_history_prices['data']['price_history']
        for pair in raw_price_history:
            if len(pair) == 2:
                history_prices.append(float(pair[1]) * DOLLAR_TO_CNY)

        # set history price if exist
        if len(history_prices) != 0:
            item.set_history_prices(history_prices, days)

        log.info('totally {} pieces of price history in {} days for {}\n'.format(len(history_prices), days, item.name))


def crawl_history_price(csgo_items):
    total_price_number = len(csgo_items)
    log.info('Total {} items to get history price.'.format(total_price_number))

    for index, item in enumerate(csgo_items, start=1):
        crawl_item_history_price(index, item, total_price_number)
