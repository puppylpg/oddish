import os
import re

from src.config.definitions import OUTPUT_FILE_NAME, FORCE_CRAWL, CRAWL_MIN_PRICE_ITEM, CRAWL_MAX_PRICE_ITEM
from src.config.urls import BUFF_ROOT, BUFF_GOODS
from src.crawl import history_price_crawler
from src.data.item import Item
from src.util import requester, persist_util, http_util


def collect_item(item):
    buff_id = item['id']
    name = item['name']
    min_price = item['sell_min_price']
    sell_num = item['sell_num']
    steam_url = item['steam_market_url']
    steam_predict_price = item['goods_info']['steam_price_cny']
    buy_max_price = item['buy_max_price']

    if float(min_price) <= CRAWL_MIN_PRICE_ITEM or float(steam_predict_price) <= CRAWL_MIN_PRICE_ITEM \
            or float(min_price) >= CRAWL_MAX_PRICE_ITEM or float(steam_predict_price) >= CRAWL_MAX_PRICE_ITEM:
        print("{} price too low or too high. Drop it!".format(name))
        return None
    else:
        print("Finish parsing {}.".format(name))
        return Item(buff_id, name, min_price, sell_num, steam_url, steam_predict_price, buy_max_price)


def collect_single_category(category):
    csgo_category_item = []

    category_url = BUFF_GOODS + 'game=csgo&page_num=1&category=%s' % category
    print("GET({}): {}".format(category, category_url))
    category_json = requester.get_json_dict(category_url)

    # return if request timeout
    if category_json is None:
        print('Timeout for category {}. SKIP'.format(category))
        return csgo_category_item

    total_page = category_json['data']['total_page']
    total_count = category_json['data']['total_count']

    for page_num in range(1, total_page + 1):
        url = BUFF_GOODS + 'game=csgo&page_num={}&category={}'.format(page_num, category)
        page_items = requester.get_json_dict(url)

        # return if request timeout
        if page_items is None:
            print('Timeout for page {} of {}. SKIP'.format(page_num, category))
            continue

        current_count = page_items['data']['page_size']
        print(
            "GET({} page {}/{}, item {}/{}): {}".format(category, page_num, total_page, current_count, total_count, url)
        )

        items = page_items['data']['items']
        for item in items:
            csgo_item = collect_item(item)
            if csgo_item is not None:
                csgo_category_item.append(csgo_item)

    print("Finish parsing {}.".format(category))
    return csgo_category_item


def collect_all_categories(categories):
    csgo_items = []

    # for category in [categories.pop()]:
    for category in categories:
        csgo_items.extend(collect_single_category(category))

    print("Finish parsing All csgo items.")
    return csgo_items


def crawl_website():
    prefix = '<div class="h1z1-selType type_csgo" id="j_h1z1-selType">'
    suffix = '</ul> </div> </div> <div class="criteria">'
    # to match all csgo skin categories
    category_regex = re.compile(r'<li value="(.+?)"', re.DOTALL)

    # entry page
    root_url = BUFF_ROOT + 'market/?game=csgo#tab=selling&page_num=1'

    print("GET: " + root_url)
    root_html = http_util.open_url(root_url)

    remove_prefix = root_html.split(prefix, 1)[1]
    core_html = remove_prefix.split(suffix, 1)[0]

    # all categories
    categories = category_regex.findall(core_html)
    print("All categories: ")
    # All categories:
    # weapon_knife_survival_bowie, weapon_knife_butterfly, weapon_knife_falchion, weapon_knife_flip, weapon_knife_gut,
    # weapon_knife_tactical, weapon_knife_m9_bayonet, weapon_bayonet, weapon_knife_karambit, weapon_knife_push,
    # weapon_knife_stiletto, weapon_knife_ursus, weapon_knife_gypsy_jackknife, weapon_knife_widowmaker,
    # weapon_knife_css, weapon_knife_cord, weapon_knife_canis, weapon_knife_outdoor, weapon_knife_skeleton,
    # weapon_hkp2000, weapon_usp_silencer, weapon_glock, weapon_p250, weapon_fiveseven, weapon_cz75a, weapon_tec9,
    # weapon_revolver, weapon_deagle, weapon_elite, weapon_galilar, weapon_scar20, weapon_awp, weapon_ak47,
    # weapon_famas, weapon_m4a1, weapon_m4a1_silencer, weapon_sg556, weapon_ssg08, weapon_aug, weapon_g3sg1,
    # weapon_p90, weapon_mac10, weapon_ump45, weapon_mp7, weapon_bizon, weapon_mp9, weapon_mp5sd, weapon_sawedoff,
    # weapon_xm1014, weapon_nova, weapon_mag7, weapon_m249, weapon_negev,
    # weapon_bloodhound_gloves, weapon_driver_gloves, weapon_hand_wraps, weapon_moto_gloves, weapon_specialist_gloves,
    # weapon_sport_gloves, weapon_hydra_gloves,
    # csgo_type_tool, csgo_type_spray, csgo_type_collectible, csgo_type_ticket, csgo_tool_gifttag, csgo_type_musickit,
    # csgo_type_weaponcase, csgo_tool_weaponcase_keytag, type_customplayer
    print(*categories, sep=", ")

    csgo_items = collect_all_categories(categories)

    # crawl price for all items
    history_price_crawler.crawl_history_price(csgo_items)

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
