import traceback
from datetime import datetime

from src.config.urls import steam_price_history_url
from src.util.requester import get_json_dict, steam_cookies
from src.util.logger import log


def crawl_item_history_price(index, item, total_price_number):
    history_prices = []

    steam_price_url = steam_price_history_url(item)
    log.info('GET steam history price {}/{} for ({}): {}'.format(index, total_price_number, item.name, steam_price_url))
    steam_history_prices = get_json_dict(steam_price_url, steam_cookies, True)

    if steam_history_prices is not None:
        raw_price_history = steam_history_prices['prices']
        if len(raw_price_history) > 0:
            days = min((datetime.today().date() - datetime.strptime(raw_price_history[0][0], '%b %d %Y %H: +0').date()).days, 7)
        else:
            days = 0
        for pair in reversed(raw_price_history):
            if len(pair) == 3:
                for i in range(0, int(pair[2])):
                    history_prices.append(float(pair[1]))
            if (datetime.today().date() - datetime.strptime(pair[0], '%b %d %Y %H: +0').date()).days > days:
                break

        # set history price if exist
        if len(history_prices) != 0:
            item.set_history_prices(history_prices, days)

        log.info('totally {} pieces of price history in {} days for {}\n'.format(len(history_prices), days, item.name))


def crawl_history_price(csgo_items):
    total_price_number = len(csgo_items)
    log.info('Total {} items to get history price.'.format(total_price_number))

    for index, item in enumerate(csgo_items, start=1):
        try:
            crawl_item_history_price(index, item, total_price_number)
        except Exception as e:
            log.error(traceback.format_exc())
