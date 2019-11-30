import datetime

from src import crawler
from src.util import suggestion

if __name__ == '__main__':

    # start
    start = datetime.datetime.now()
    print("Start Time: {}".format(start))

    table = crawler.crawl()

    # suggestion
    suggestion.suggest(table)

    # end
    end = datetime.datetime.now()
    print("END: {}. TIME USED: {}.".format(end, end - start))