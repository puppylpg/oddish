import sys
from src.config.definitions import config

if config.CONSOLE:
    import datetime

    from src.crawl import item_crawler
    from src.util import suggestion
    from src.util.logger import log

    start = datetime.datetime.now()
    log.info("Start Time: {}".format(start))

    table = item_crawler.crawl()

    if (table is not None) and len(table) > 0:
        suggestion.suggest(table)
    else:
        log.error('No correct csgo items remain. Please check if conditions are to strict.')

    end = datetime.datetime.now()
    log.info("END: {}. TIME USED: {}.".format(end, end - start))
else:
    from PyQt5 import QtWidgets
    from src.ui.oddish import oddish

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = oddish(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
