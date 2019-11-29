import os
import sys
from datetime import datetime

TIMESTAMP = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

DATE_HOUR = str(datetime.now().strftime('%Y-%m-%d-%H'))
OUTPUT_PATH = "output"
OUTPUT_NAME = "csgo_skins_" + DATE_HOUR

FILE_NAME = os.path.join(
    OUTPUT_PATH, OUTPUT_NAME + ".csv"
)
