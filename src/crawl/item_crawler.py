import re
import urllib.request

from src.config.definitions import config
from src.config.urls import goods_section_root_url, goods_root_url, goods_section_page_url
from src.crawl import history_price_crawler
from src.data.item import Item
from src.util import persist
from src.util.requester import get_json_dict
from src.util.category import final_categories
from src.util.logger import log
from src.util import timer


def collect_item(item):
    buff_id = item['id']
    name = item['name']
    min_price = item['sell_min_price']
    sell_num = item['sell_num']
    steam_url = item['steam_market_url']
    steam_predict_price = item['goods_info']['steam_price_cny']
    buy_max_price = item['buy_max_price']

    # restrict price of a item
    if float(min_price) < config.CRAWL_MIN_PRICE_ITEM:
        log.info("{} price is lower than {}. Drop it!".format(name, config.CRAWL_MIN_PRICE_ITEM))
        return None
    if float(min_price) > config.CRAWL_MAX_PRICE_ITEM:
        log.info("{} price is higher than {}. Drop it!".format(name, config.CRAWL_MAX_PRICE_ITEM))
        return None

    log.info("Finish parsing {}.".format(name))
    return Item(buff_id, name, min_price, sell_num, steam_url, steam_predict_price, buy_max_price)


def csgo_all_categories():
    prefix = '<div class="h1z1-selType type_csgo" id="j_h1z1-selType">'
    suffix = '</ul> </div> </div> <div class="criteria">'
    # to match all csgo skin categories
    category_regex = re.compile(r'<li value="(.+?)"', re.DOTALL)

    # entry page
    root_url = goods_root_url()

    log.info("GET: " + root_url)
    root_html = urllib.request.urlopen(root_url).read().decode('utf-8')

    remove_prefix = root_html.split(prefix, 1)[1]
    core_html = remove_prefix.split(suffix, 1)[0]

    # all categories
    categories = category_regex.findall(core_html)
    log.info("All categories({}): {}".format(len(categories), categories))
    return categories


def enrich_item_with_price_history(csgo_items):
    # crawl price for all items
    history_price_crawler.crawl_history_price(csgo_items)
    return csgo_items


def crawl_website():
    csgo_items = []

    raw_categories = csgo_all_categories()

    categories = final_categories(raw_categories)

    # crawl by categories and price section
    if len(raw_categories) != len(categories):
        total_category = len(categories)
        for index, category in enumerate(categories, start=1):
            csgo_items.extend(crawl_goods_by_price_section(category))
            log.info('GET category {}/{} for ({}).'.format(index, total_category, category))
    else:
        # crawl by price section without category
        csgo_items.extend(crawl_goods_by_price_section(None))

    enrich_item_with_price_history(csgo_items)
    return persist.tabulate(csgo_items)


def crawl_goods_by_price_section(category=None):
    root_url = goods_section_root_url(category)
    log.info('GET: {}'.format(root_url))

    root_json = get_json_dict(root_url, config.BUFF_COOKIE)
    
    category_items = []

    if root_json is not None:
        if 'data' not in root_json:
            log.error('Error happens:')
            log.error(root_json)
            if 'error' in root_json:
                log.error('Error field: ' + root_json['error'])
            log.error('Please paste correct buff cookie to config, current cookie：' + str(config.BUFF_COOKIE))
            return []

        if ('total_page' not in root_json['data']) or ('total_count' not in root_json['data']):
            log.error("No specific page and count info for root page. Please check buff data structure.")

        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']
        log.info('Totally {} items of {} pages to crawl.'.format(total_count, total_page))
        # get each page
        for page_num in range(1, total_page + 1):
            log.info('Page {} / {}'.format(page_num, total_page))
            page_url = goods_section_page_url(category, page_num)
            page_json = get_json_dict(page_url, config.BUFF_COOKIE)
            if (page_json is not None) and ('data' in page_json) and ('items' in page_json['data']):
                # items on this page
                items_json = page_json['data']['items']
                for item in items_json:
                    # get item
                    csgo_item = collect_item(item)
                    if csgo_item is not None:
                        category_items.append(csgo_item)
            else:
                log.warn("No specific data for page {}. Skip this page.".format(page_url))

    return category_items


def crawl():
    log.info("Force crawling? {}".format(config.FORCE_CRAWL))

    return crawl_website()
