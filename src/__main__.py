import datetime

from src.crawl import item_crawler
from src.util import suggestion
from src.util.logger import log

if __name__ == '__main__':

    # start
    start = datetime.datetime.now()
    log.info("Start Time: {}".format(start))

    table = item_crawler.crawl()

    if table is not None:
        # suggestion
        suggestion.suggest(table)
    else:
        log.error('No correct csgo items remain. Please check if conditions are to strict.')

    # end
    end = datetime.datetime.now()
    log.info("END: {}. TIME USED: {}.".format(end, end - start))