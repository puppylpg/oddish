import datetime

from src import crawler
from src.util import suggestion

if __name__ == '__main__':

    # start
    start = datetime.datetime.now()
    print("Start Time: {}".format(start))

    csgo_items = crawler.crawl()

    # suggestion
    suggestion.suggest(csgo_items)

    # end
    end = datetime.datetime.now()
    print("END: {}. TIME USED: {}.".format(end, end - start))