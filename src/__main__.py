import datetime

from src.crawl import item_crawler
from src.util import suggestion

if __name__ == '__main__':

    # start
    start = datetime.datetime.now()
    print("Start Time: {}".format(start))

    table = item_crawler.crawl()

    # suggestion
    suggestion.suggest(table)

    # end
    end = datetime.datetime.now()
    print("END: {}. TIME USED: {}.".format(end, end - start))