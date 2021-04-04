import math
import functools

from src.crawl.item_crawler import csgo_all_categories
from src.util.category import final_categories
from src.config.definitions import config
from src.util.logger import out

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

def switch(name):
    if name in config.CATEGORY_WHITE_LIST:
        config.CATEGORY_WHITE_LIST.remove(name)
    else:
        config.CATEGORY_WHITE_LIST.append(name)

class selector(QtWidgets.QWidget):
    def add_checkbox(self, grid_layout, i, j):
        categories = csgo_all_categories()
        index = i * 2 + j
        hbox = QtWidgets.QHBoxLayout()
        checkbox = QtWidgets.QCheckBox(categories[index], self)
        if categories[index] in self.cur_category:
            checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            checkbox.setCheckState(QtCore.Qt.Unchecked)
        checkbox.stateChanged.connect(functools.partial(switch, categories[index]))
        checkbox.setFixedHeight(40)
        iconf = QtCore.QFileInfo(":/csgo/" + categories[index] + ".svg");
        if iconf.exists():
            icon = QtSvg.QSvgWidget(":/csgo/" + categories[index] + ".svg")
            icon.setFixedSize(icon.width() / 3, icon.height() / 3)
            hbox.addWidget(icon)
        hbox.addWidget(checkbox)
        grid_layout.addLayout(hbox, i, j)

    def __init__(self, parent = None):
        super(selector, self).__init__(parent)
        self.setWindowTitle("类型限定")
        out.enabled = False
        categories = csgo_all_categories()
        self.cur_category = final_categories(categories)
        out.enabled = True
        config.CATEGORY_WHITE_LIST = self.cur_category  # when open this, black list is abandoned

        grid_layout = QtWidgets.QGridLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setMinimumSize(1000, 640)

        rows = int(len(categories) / 2)
        for i in range(rows):
            for j in range(2):
                self.add_checkbox(grid_layout, i, j)
        if len(categories) % 2 != 0:
            self.add_checkbox(grid_layout, rows, 0)

        w = QtWidgets.QWidget()
        w.setLayout(grid_layout)
        scroll.setWidget(w)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(scroll)
        self.setLayout(hbox)
