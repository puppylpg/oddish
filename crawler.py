import datetime
import re

import http_util
import requester
import suggestion
import persist_util
from item import Item

if __name__ == '__main__':

    # start
    start = datetime.datetime.now()
    print("Start Time: {}".format(start))

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

        # TODO
        for i in range(1, total_page + 1):
        # for i in range(1, 2):
            if i != 1:
                url = 'https://buff.163.com/api/market/goods?game=csgo&page_num={}&category={}'.format(i, category)
                json_data = requester.get_json(url)
            else:
                # already requested
                url = category_url
                json_data = category_json
            print("GET({} page {} of {}): {}".format(category, i, total_page, url))

            items = category_json['data']['items']
            for item in items:
                name = item['name']
                min_price = item['sell_min_price']
                sell_num = item['sell_num']
                steam_url = item['steam_market_url']
                steam_predict_price = item['goods_info']['steam_price_cny']
                buy_max_price = item['buy_max_price']

                csgo_items.append(Item(name, min_price, sell_num, steam_url, steam_predict_price, buy_max_price))
                print("Finish parsing {}.".format(name))

    # persist data
    persist_util.tabulate(csgo_items)
    # suggestion
    suggestion.suggest(csgo_items)

    # end
    end = datetime.datetime.now()
    print("END: {}. TIME USED: {}.".format(end, end - start))