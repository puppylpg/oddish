import re
import math
import asyncio

# from tqdm import tqdm

from src.config.definitions import CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM, BUFF_COOKIE, FORCE_CRAWL, CRAWL_STEAM_ASYNC
from src.config.urls import goods_section_root_url, goods_root_url, goods_section_page_url
from src.crawl import history_price_crawler
from src.data.item import Item
from src.util import persist_util, http_util
from src.util.requester import get_json_dict, buff_cookies
from src.util.category_util import final_categories
from src.util.logger import log


def collect_item(item):
    buff_id = item['id']
    name = item['name']
    min_price = item['sell_min_price']
    sell_num = item['sell_num']
    steam_url = item['steam_market_url']
    steam_predict_price = item['goods_info']['steam_price_cny']
    buy_max_price = item['buy_max_price']

    # restrict price of a item
    if float(min_price) < CRAWL_MIN_PRICE_ITEM:
        log.info("{} price is lower than {}. Drop it!".format(name, CRAWL_MIN_PRICE_ITEM))
        return None
    if float(min_price) > CRAWL_MAX_PRICE_ITEM:
        log.info("{} price is higher than {}. Drop it!".format(name, CRAWL_MAX_PRICE_ITEM))
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
    root_html = http_util.open_url(root_url)

    remove_prefix = root_html.split(prefix, 1)[1]
    core_html = remove_prefix.split(suffix, 1)[0]

    # all categories
    categories = category_regex.findall(core_html)
    log.info("All categories({}): {}".format(len(categories), categories))
    return categories


def enrich_item_with_price_history(csgo_items, crawl_steam_async=True):
    # crawl price for all items
    if crawl_steam_async:
        asyncio.get_event_loop().run_until_complete(history_price_crawler.async_crawl_history_price(csgo_items))
    else:
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

    enrich_item_with_price_history(csgo_items, CRAWL_STEAM_ASYNC)
    return persist_util.tabulate(csgo_items)


def crawl_goods_by_price_section(category=None):
    root_url = goods_section_root_url(category)
    log.info('GET: {}'.format(root_url))

    root_json = get_json_dict(root_url, buff_cookies)

    category_items = []

    if root_json is not None:
        if 'data' not in root_json:
            log.error('Error happens:')
            log.error(root_json)
            if 'error' in root_json:
                log.error('Error field: ' + root_json['error'])
            log.error('Please paste correct buff cookie to config, current cookie：' + BUFF_COOKIE)
            exit(1)

        if ('total_page' not in root_json['data']) or ('total_count' not in root_json['data']):
            log.error("No specific page and count info for root page. Please check buff data structure.")

        total_page = root_json['data']['total_page']
        total_count = root_json['data']['total_count']

        # buff有个page_size参数，默认一页请求20个item，最多80
        # 尝试使用80，能将对buff的访问量减少为原来的1/4。暂时不作为可配置项，硬编码在代码里
        use_max_page_size = True
        max_page_size = 80
        default_page_size = 20

        # 使用80一页后，新的页码
        if use_max_page_size:
            total_page = math.ceil(total_count / max_page_size)

        log.info('Totally {} items of {} pages to crawl.'.format(total_count, total_page))
        # get each page
        for page_num in range(1, total_page + 1):
            log.info('Page {} / {}'.format(page_num, total_page))
            page_url = goods_section_page_url(
                category, page_num,
                page_size=max_page_size if use_max_page_size else default_page_size
            )
            page_json = get_json_dict(page_url, buff_cookies)
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
    log.info("Force crawling? {}".format(FORCE_CRAWL))

    return crawl_website()
