from fnmatch import fnmatch

from src.config.definitions import CATEGORY_BLACK_LIST, CATEGORY_WHITE_LIST
from src.util.logger import log


def final_categories(categories):
    """白名单优先于黑名单"""

    log.info('Blacklist categories({}): {}'.format(len(CATEGORY_BLACK_LIST), CATEGORY_BLACK_LIST))
    log.info('Whitelist categories({}): {}'.format(len(CATEGORY_WHITE_LIST), CATEGORY_WHITE_LIST))

    if len(CATEGORY_WHITE_LIST) != 0:
        final = [item for item in categories if any(fnmatch(item, pattern) for pattern in CATEGORY_WHITE_LIST)]
    else:
        final = [item for item in categories if not any(fnmatch(item, pattern) for pattern in CATEGORY_BLACK_LIST)]

    log.info('Final categories({}): {}'.format(len(final), final))
    return final
