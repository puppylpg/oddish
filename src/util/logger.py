import logging
import os
import sys

from src.config.definitions import NORMAL_LOGGER, SUGGESTION_LOGGER

formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")


def get_logger(name, log_file, level=logging.DEBUG, format=True):
    """To setup as many loggers as you want"""

    # output to both console and file
    console_handler = logging.StreamHandler(sys.stdout)
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
if not os.path.exists(os.path.dirname(NORMAL_LOGGER)):
    os.mkdir(os.path.dirname(NORMAL_LOGGER))
if not os.path.exists(os.path.dirname(SUGGESTION_LOGGER)):
    os.mkdir(os.path.dirname(SUGGESTION_LOGGER))

log = get_logger('normal', os.path.abspath(NORMAL_LOGGER))
suggestion_log = get_logger('suggestion', os.path.abspath(SUGGESTION_LOGGER), format=False)
