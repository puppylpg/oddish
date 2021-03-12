import sys, json, pathlib
import argparse
from src.config.definitions import config

praser = argparse.ArgumentParser('oddish')
praser.add_argument('--output', '-o', 
    help = "Place the output json into <file>", type = pathlib.Path, metavar = 'output.json')
praser.add_argument('--console', 
    help = "Disable Graphical User Interface", action='store_true', default = False)
args = praser.parse_args()
if config.CONSOLE or args.console:
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

    if args.output is not None:
        database = [x.to_dict() for x in table]
        with open(args.output, "w", encoding='utf-8') as f:
            f.write(json.dumps(database))
    
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
