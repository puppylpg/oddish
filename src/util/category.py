from fnmatch import fnmatch

from src.config.definitions import config
from src.util.logger import log


def final_categories(categories):
    """白名单优先于黑名单"""

    log.info('Blacklist categories({}): {}'.format(len(config.CATEGORY_BLACK_LIST), config.CATEGORY_BLACK_LIST))
    log.info('Whitelist categories({}): {}'.format(len(config.CATEGORY_WHITE_LIST), config.CATEGORY_WHITE_LIST))

    if len(config.CATEGORY_WHITE_LIST) != 0:
        final = [item for item in categories if any(fnmatch(item, pattern) for pattern in config.CATEGORY_WHITE_LIST)]
    else:
        final = [item for item in categories if not any(fnmatch(item, pattern) for pattern in config.CATEGORY_BLACK_LIST)]

    log.info('Final categories({}): {}'.format(len(final), final))
    return final
