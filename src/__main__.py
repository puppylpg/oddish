import sys
import datetime

from src.crawl import item_crawler
from src.util import suggestion
from src.util.logger import log

if __name__ == '__main__':

    if sys.version_info[:2] == (3, 7):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # start
    start = datetime.datetime.now()
    log.info("Start Time: {}".format(start))

    table = item_crawler.crawl()

    # table may be empty if no data is received due to timeout
    if (table is not None) and (not table.empty):
        # suggestion
        suggestion.suggest(table)
    else:
        log.error('No correct csgo items remain. Please check if conditions are to strict.')

    # end
    end = datetime.datetime.now()
    log.info("END: {}. TIME USED: {}.".format(end, end - start))
