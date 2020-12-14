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


# def csgo_all_categories():
#     prefix = '<div class="h1z1-selType type_csgo" id="j_h1z1-selType">'
#     suffix = '</ul> </div> </div> <div class="criteria">'
#     # to match all csgo skin categories
#     category_regex = re.compile(r'<li value="(.+?)"', re.DOTALL)

#     # entry page
#     root_url = goods_root_url()

#     log.info("GET: " + root_url)
#     root_html = urllib.request.urlopen(root_url).read().decode('utf-8')

#     remove_prefix = root_html.split(prefix, 1)[1]
#     core_html = remove_prefix.split(suffix, 1)[0]

#     # all categories
#     categories = category_regex.findall(core_html)
#     log.info("All categories({}): {}".format(len(categories), categories))
#     print(categories)
#     return categories

def csgo_all_categories():
    return ['weapon_knife_survival_bowie', 'weapon_knife_butterfly', 'weapon_knife_falchion', 'weapon_knife_flip', 'weapon_knife_gut', 'weapon_knife_tactical', 'weapon_knife_m9_bayonet', 'weapon_bayonet', 'weapon_knife_karambit', 'weapon_knife_push', 'weapon_knife_stiletto', 'weapon_knife_ursus', 'weapon_knife_gypsy_jackknife', 'weapon_knife_widowmaker', 'weapon_knife_css', 'weapon_knife_cord', 'weapon_knife_canis', 'weapon_knife_outdoor', 'weapon_knife_skeleton', 'weapon_hkp2000', 'weapon_usp_silencer', 'weapon_glock', 'weapon_p250', 'weapon_fiveseven', 'weapon_cz75a', 'weapon_tec9', 'weapon_revolver', 'weapon_deagle', 'weapon_elite', 'weapon_galilar', 'weapon_scar20', 'weapon_awp', 'weapon_ak47', 'weapon_famas', 'weapon_m4a1', 'weapon_m4a1_silencer', 'weapon_sg556', 'weapon_ssg08', 'weapon_aug', 'weapon_g3sg1', 'weapon_p90', 'weapon_mac10', 'weapon_ump45', 'weapon_mp7', 'weapon_bizon', 'weapon_mp9', 'weapon_mp5sd', 'weapon_sawedoff', 'weapon_xm1014', 'weapon_nova', 'weapon_mag7', 'weapon_m249', 'weapon_negev', 'weapon_bloodhound_gloves', 'weapon_driver_gloves', 'weapon_hand_wraps', 'weapon_moto_gloves', 'weapon_specialist_gloves', 'weapon_sport_gloves', 'weapon_hydra_gloves', 'weapon_brokenfang_gloves', 'sticker_broken_fang', 'sticker_recoil', 'warhammer_sticker', 'alyx_sticker_capsule', 'halo_capsule', 'shattered_web', 'cs20_capsule', '2019_StarLadder_Berlin_Major', 'crate_sticker_pack_chicken_capsule_lootlist', 'crate_sticker_pack_feral_predators_capsule_lootlist', 'sticker_tournament15', 'skill_groups_capsule', 'sticker_tournament14', 'sticker_tournament13', 'sticker_tournament12', 'sticker_tournament11', 'sticker_tournament10', 'sticker_tournament9', 'sticker_tournament8', 'sticker_tournament7', 'sticker_tournament6', 'sticker_tournament5', 'sticker_tournament4', 'sticker_tournament3', 'crate_sticker_pack_comm2018_01_capsule_lootlist', 'crate_sticker_pack01', 'crate_sticker_pack02', 'crate_sticker_pack_enfu_capsule_lootlist', 'crate_sticker_pack_illuminate_capsule_01_lootlist', 'crate_sticker_pack_illuminate_capsule_02_lootlist', 'crate_sticker_pack_community01', 'crate_sticker_pack_bestiary_capsule_lootlist', 'crate_sticker_pack_slid3_capsule_lootlist', 'crate_sticker_pack_sugarface_capsule_lootlist', 'crate_sticker_pack_pinups_capsule_lootlist', 'crate_sticker_pack_team_roles_capsule_lootlist', 'sticker_other', 'csgo_type_tool', 'csgo_type_spray', 'csgo_type_collectible', 'csgo_type_ticket', 'csgo_tool_gifttag', 'csgo_type_musickit', 'csgo_type_weaponcase', 'csgo_tool_weaponcase_keytag', 'type_customplayer', 'csgo_tool_patch']

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
