import logging
import os
import sys
from src.config.definitions import config

if not config.CONSOLE:
    from PyQt5 import QtGui
    from PyQt5.QtCore import QObject, pyqtSignal
    from src.config.definitions import config

formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

if not config.CONSOLE:
    class gui_stream(QObject):
        text_signal = pyqtSignal(str)
        enabled = True

        def __init__(self):
            super().__init__()
        def write(self, text):
            if self.enabled:
                self.text_signal.emit(text)
        def flush(self):
            pass
    out = gui_stream()
else:
    out = sys.stdout

def get_logger(name, log_file, level = logging.DEBUG, format=True):
    """To setup as many loggers as you want"""

    # output to both console and file
    console_handler = logging.StreamHandler(out)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')

    if format:
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# mkdir if not exist
if not os.path.exists(os.path.dirname(config.NORMAL_LOGGER)):
    os.mkdir(os.path.dirname(config.NORMAL_LOGGER))
if not os.path.exists(os.path.dirname(config.SUGGESTION_LOGGER)):
    os.mkdir(os.path.dirname(config.SUGGESTION_LOGGER))

log = get_logger('normal', os.path.abspath(config.NORMAL_LOGGER))
suggestion_log = get_logger('suggestion', os.path.abspath(config.SUGGESTION_LOGGER), format=False)
