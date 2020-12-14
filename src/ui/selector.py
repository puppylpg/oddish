import math

from src.crawl.item_crawler import csgo_all_categories
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

class selector(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(selector, self).__init__(parent)
        self.setWindowTitle("Selector")

        grid_layout = QtWidgets.QGridLayout()
        scroll = QtWidgets.QScrollArea()
        scroll.setMinimumSize(1000, 640)

        categories = csgo_all_categories()
        rows = int(len(categories) / 2)
        for i in range(rows):
            for j in range(2):
                index = i * 2 + j
                hbox = QtWidgets.QHBoxLayout()
                checkbox = QtWidgets.QCheckBox(categories[index], self)
                checkbox.setFixedHeight(40)
                iconf = QtCore.QFileInfo(":/csgo/" + categories[index] + ".svg");
                if iconf.exists():
                    icon = QtSvg.QSvgWidget(":/csgo/" + categories[index] + ".svg")
                    icon.setFixedSize(icon.width() / 3, icon.height() / 3)
                    hbox.addWidget(icon)
                hbox.addWidget(checkbox)
                grid_layout.addLayout(hbox, i, j)

        w = QtWidgets.QWidget()
        w.setLayout(grid_layout)
        scroll.setWidget(w)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(scroll)
        self.setLayout(hbox)
