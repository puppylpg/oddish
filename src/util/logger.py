import logging
import os
import sys

from PyQt5 import QtGui
from src.config.definitions import config

formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

class gui_stream:
    def __init__(self, textbox):
        self.textbox = textbox
    def write(self, text):
        self.textbox.moveCursor(QtGui.QTextCursor.End)
        self.textbox.insertPlainText(text)
    def flush(self):
        pass
gui_out = gui_stream(None)

def get_logger(name, log_file, level = logging.DEBUG, format=True):
    """To setup as many loggers as you want"""

    # output to both console and file
    console_handler = logging.StreamHandler(gui_out)
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
