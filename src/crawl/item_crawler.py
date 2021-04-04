import re
import math
import time
import asyncio
import aiohttp
import traceback
from aiohttp_socks import ProxyConnector
from datetime import datetime

from src.config.definitions import config
from src.config.urls import steam_price_history_url, goods_section_root_url, goods_root_url, goods_section_page_url
from src.data.item import Item
from src.util.requester import async_get_json_dict, get_headers, get_json_dict
from src.util.category import final_categories
from src.util.logger import log
from src.util.cache import exist
from src.util import timer

async def async_crawl_item_history_price(index, item, session):
    history_prices = []

    steam_price_url = steam_price_history_url(item)
    log.info('prepare to GET steam history price {} for ({}): {}'.format(index, item.name, steam_price_url))

    steam_history_prices = await async_get_json_dict(steam_price_url, config.STEAM_COOKIE, session, proxy=True)

    # key existence check
    if (steam_history_prices is not None) and ('prices' in steam_history_prices):
        days = key_existence_check(item, history_prices, steam_history_prices)

        log.info('got steam history price {} for {}({} pieces of price history): {}'.format(index, item.name, len(history_prices), steam_price_url))

def key_existence_check(item:Item, history_prices, steam_history_prices):
    raw_price_history = steam_history_prices['prices']
    days = 0
    try:
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
    except Exception as e:
        log.error(traceback.format_exc())
        log.error('raw_price_history: {}'.format(raw_price_history))
        log.error('steam_history_prices: {}'.format(steam_history_prices))

    # set history price if exist
    if len(history_prices) != 0:
        item.set_history_prices(history_prices, days)
    return days

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
    return ['weapon_knife_survival_bowie', 'weapon_knife_butterfly', 'weapon_knife_falchion', 'weapon_knife_flip', 'weapon_knife_gut', 'weapon_knife_tactical', 'weapon_knife_m9_bayonet', 'weapon_bayonet', 'weapon_knife_karambit', 'weapon_knife_push', 'weapon_knife_stiletto', 'weapon_knife_ursus', 'weapon_knife_gypsy_jackknife', 'weapon_knife_widowmaker', 'weapon_knife_css', 'weapon_knife_cord', 'weapon_knife_canis', 'weapon_knife_outdoor', 'weapon_knife_skeleton', 'weapon_hkp2000', 'weapon_usp_silencer', 'weapon_glock', 'weapon_p250', 'weapon_fiveseven', 'weapon_cz75a', 'weapon_tec9', 'weapon_revolver', 'weapon_deagle', 'weapon_elite', 'weapon_galilar', 'weapon_scar20', 'weapon_awp', 'weapon_ak47', 'weapon_famas', 'weapon_m4a1', 'weapon_m4a1_silencer', 'weapon_sg556', 'weapon_ssg08', 'weapon_aug', 'weapon_g3sg1', 'weapon_p90', 'weapon_mac10', 'weapon_ump45', 'weapon_mp7', 'weapon_bizon', 'weapon_mp9', 'weapon_mp5sd', 'weapon_sawedoff', 'weapon_xm1014', 'weapon_nova', 'weapon_mag7', 'weapon_m249', 'weapon_negev', 'weapon_bloodhound_gloves', 'weapon_driver_gloves', 'weapon_hand_wraps', 'weapon_moto_gloves', 'weapon_specialist_gloves', 'weapon_sport_gloves', 'weapon_hydra_gloves', 'weapon_brokenfang_gloves', 'sticker_broken_fang', 'sticker_recoil', 'warhammer_sticker', 'alyx_sticker_capsule', 'halo_capsule', 'shattered_web', 'cs20_capsule', '2019_StarLadder_Berlin_Major', 'crate_sticker_pack_chicken_capsule_lootlist', 'crate_sticker_pack_feral_predators_capsule_lootlist', 'sticker_tournament15', 'skill_groups_capsule', 'sticker_tournament14', 'sticker_tournament13', 'sticker_tournament12', 'sticker_tournament11', 'sticker_tournament10', 'sticker_tournament9', 'sticker_tournament8', 'sticker_tournament7', 'sticker_tournament6', 'sticker_tournament5', 'sticker_tournament4', 'sticker_tournament3', 'crate_sticker_pack_comm2018_01_capsule_lootlist', 'crate_sticker_pack01', 'crate_sticker_pack02', 'crate_sticker_pack_enfu_capsule_lootlist', 'crate_sticker_pack_illuminate_capsule_01_lootlist', 'crate_sticker_pack_illuminate_capsule_02_lootlist', 'crate_sticker_pack_community01', 'crate_sticker_pack_bestiary_capsule_lootlist', 'crate_sticker_pack_slid3_capsule_lootlist', 'crate_sticker_pack_sugarface_capsule_lootlist', 'crate_sticker_pack_pinups_capsule_lootlist', 'crate_sticker_pack_team_roles_capsule_lootlist', 'sticker_other', 'csgo_type_tool', 'csgo_type_spray', 'csgo_type_collectible', 'csgo_type_ticket', 'csgo_tool_gifttag', 'csgo_type_musickit', 'csgo_type_weaponcase', 'csgo_tool_weaponcase_keytag', 'type_customplayer', 'csgo_tool_patch']

async def crawl_goods_by_price_section(category=None):
    root_url = goods_section_root_url(category)
    log.info('GET: {}'.format(root_url))

    root_json = get_json_dict(root_url, config.BUFF_COOKIE)
    category_items = []

    tasks = []
    timeout = aiohttp.ClientTimeout(total=30 * 60)
    if config.PROXY:
        # use socks
        connector = ProxyConnector.from_url(config.PROXY, limit=5)
    else:
        connector = aiohttp.TCPConnector(limit=5)

    if 'data' not in root_json:
        log.error('Error happens:')
        log.error(root_json)
        if 'error' in root_json:
            log.error('Error field: ' + root_json['error'])
        log.error('Please paste correct buff cookie to config, current cookie：' + str(config.BUFF_COOKIE))
        return None

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
    async with aiohttp.ClientSession(cookies=config.STEAM_COOKIE, headers=get_headers(), connector=connector,timeout=timeout) as session:
        # get each page
        for page_num in range(1, total_page + 1):
            log.info('Page {} / {}'.format(page_num, total_page))
            page_url = goods_section_page_url(
                category, page_num,
                page_size=max_page_size if use_max_page_size else default_page_size
            )
            page_json = get_json_dict(page_url, config.BUFF_COOKIE)
            if (page_json is not None) and ('data' in page_json) and ('items' in page_json['data']):
                # items on this page
                items_json = page_json['data']['items']
                for item in items_json:
                    # get item
                    csgo_item = collect_item(item)
                    if csgo_item is not None:
                        category_items.append(csgo_item)
                        try:
                            tasks.append(async_crawl_item_history_price(len(category_items), category_items[-1], session))
                        except Exception as e:
                            log.error(traceback.format_exc())

                stamp = time.time()
                try:
                    await asyncio.gather(*tasks)
                except Exception as e:
                    log.error(traceback.format_exc())
                tasks = []
                if not exist(page_url):
                    await timer.async_sleep_awhile(0, time.time() - stamp)
            else:
                log.warn("No specific data for page {}. Skip this page.".format(page_url))
    return category_items


def crawl():
    log.info("Force crawling? {}".format(config.FORCE_CRAWL))
    csgo_items = []

    raw_categories = csgo_all_categories()

    categories = final_categories(raw_categories)

    # crawl by categories and price section
    if len(raw_categories) != len(categories):
        total_category = len(categories)
        for index, category in enumerate(categories, start=1):
            t = asyncio.run(crawl_goods_by_price_section(category))
            if t is None:
                break
            else:
                csgo_items.extend(t)
            log.info('GET category {}/{} for ({}).'.format(index, total_category, category))
    else:
        # crawl by price section without category
        csgo_items.extend(asyncio.run(crawl_goods_by_price_section(None)) or [])

    return csgo_items
