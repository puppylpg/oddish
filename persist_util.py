from collections import defaultdict

import pandas as pd

from definitions import FILE_NAME


def tabulate(csgo_items):
    rows_dict = defaultdict(list)
    for item in csgo_items:
        [rows_dict[k].append(v) for k, v in item.to_dict().items()]

    table = pd.DataFrame(data=rows_dict)
    pd.set_option('display.expand_frame_repr', False)
    print(table)
    table.to_csv(FILE_NAME)
