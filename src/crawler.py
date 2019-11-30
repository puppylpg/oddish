import os
import re

from src.config.definitions import OUTPUT_FILE_NAME, FORCE_CRAWL
from src.data.item import Item
from src.util import requester, persist_util, http_util, converter


def crawl_website():
    prefix = '<div class="h1z1-selType type_csgo" id="j_h1z1-selType">'
    suffix = '</ul> </div> </div> <div class="criteria">'
    category_regex = re.compile(r'<li value="(.+?)"', re.DOTALL)

    root_url = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=1'

    print("GET: " + root_url)
    root_html = http_util.open_url(root_url)

    remove_prefix = root_html.split(prefix, 1)[1]
    core_html = remove_prefix.split(suffix, 1)[0]

    categories = category_regex.findall(core_html)
    print("All categories: ")
    print(*categories, sep=", ")

    csgo_items = []

    # TODO
    for category in categories:
    # for category in [categories.pop()]:
        category_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&category=%s' % category
        print("GET({}): {}".format(category, category_url))
        category_json = requester.get_json(category_url)

        total_page = category_json['data']['total_page']
        total_count = category_json['data']['total_count']
        current_page_item_count = category_json['data']['page_size']

        # TODO
        for page_num in range(1, total_page + 1):
        # for page_num in range(1, 2):
            if page_num != 1:
                url = 'https://buff.163.com/api/market/goods?game=csgo&page_num={}&category={}'\
                    .format(page_num, category)
                json_data = requester.get_json(url)
                current_count = json_data['data']['page_size']
            else:
                # already requested
                url = category_url
                json_data = category_json
                current_count = current_page_item_count
            print(
                "GET({} page {}/{}, item {}/{}): {}".format(category, page_num, total_page, current_count, total_count, url)
            )

            items = json_data['data']['items']
            for item in items:
                buff_id = item['id']
                name = item['name']
                min_price = item['sell_min_price']
                sell_num = item['sell_num']
                steam_url = item['steam_market_url']
                steam_predict_price = item['goods_info']['steam_price_cny']
                buy_max_price = item['buy_max_price']

                csgo_items.append(
                    Item(buff_id, name, min_price, sell_num, steam_url, steam_predict_price, buy_max_price))
                print("Finish parsing {}.".format(name))

    # persist data
    table = persist_util.tabulate(csgo_items)

    return table


def load_local():
    return persist_util.load()


def crawl():
    print("Force crawling? {}".format(FORCE_CRAWL))
    if (not FORCE_CRAWL) and os.path.exists(OUTPUT_FILE_NAME):
        print('{} exists, load data from local!'.format(OUTPUT_FILE_NAME))
        table = load_local()
    else:
        print('Crawl data from website!')
        table = crawl_website()

    return table
