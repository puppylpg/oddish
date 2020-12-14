import sys, functools
import datetime
from http.cookies import SimpleCookie

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView

import src.ui.res_rc
from src.config.definitions import config
from src.ui.oddish_base import Ui_MainWindow
from src.util.requester import get_json_dict_raw
from src.crawl import item_crawler
from src.util import suggestion
from src.util.logger import gui_out, log

class crawler(QThread):
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        start = datetime.datetime.now()
        log.info("Start Time: {}".format(start))

        table = item_crawler.crawl()

        if (table is not None) and (not table.empty):
            suggestion.suggest(table)
        else:
            log.error('No correct csgo items remain. Please check if conditions are to strict.')

        end = datetime.datetime.now()
        log.info("END: {}. TIME USED: {}.".format(end, end - start))
        self._signal.emit()

class proxy_checker(QThread):
    _signal =pyqtSignal(bool)
    def __init__(self, proxy):
        super().__init__()
        self.proxy = proxy
    def run(self):
        config.PROXY = self.proxy
        flag = True
        if get_json_dict_raw("https://steamcommunity.com/market/", {}, True):
            self._signal.emit(True)
        else:
            self._signal.emit(False)


class browserc(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(browserc, self).__init__(parent)
        self.setWindowTitle("Cookies")
     
        layout = QtWidgets.QGridLayout()
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def get_cookie(self, url, demand, textbox):
        url = QtCore.QUrl(url)
        self.browser.load(url)
        def check_cookie(cookie):
            if cookie.domain() != url.host():
                return 
            for k in demand:
                if k == cookie.name() and demand[k] == "":
                    demand[k] = str(cookie.value(), 'utf-8')
                    break
            for k in demand:
                if demand[k] == "":
                    return
            textbox.setPlainText(SimpleCookie(demand).output(header = '', sep=';'))
            self.hide()

        self.browser.page().profile().cookieStore().cookieAdded.connect(check_cookie)
        self.showMaximized()

class oddish(Ui_MainWindow):
    steam_cookie = { 'sessionid': "" , 'steamLoginSecure': ""}
    buff_cookie = { 'session': "" }
    def __init__(self, Dialog):
        super().setupUi(Dialog)
        self.proxyEditor.setPlainText(config.PROXY)
        self.steamCookie.setPlainText(SimpleCookie(config.STEAM_COOKIE).output(header = '', sep=';'))
        self.buffCookie.setPlainText(SimpleCookie(config.BUFF_COOKIE).output(header = '', sep=';'))

        gui_out.text_signal.connect(self.log_output)
        Dialog.closeEvent = self.on_quit
        self.proxyVaild.setIcon(QtGui.QIcon(":icon/attention.png"))
        self.getSteam.clicked.connect(self.get_steam)
        self.getBuff.clicked.connect(self.get_buff)
        self.crawlStart.clicked.connect(self.crawl_start)
        self.proxyEditor.textChanged.connect(
            functools.partial(self.proxyVaild.setIcon, QtGui.QIcon(":icon/attention.png")))
        self.proxyVaild.clicked.connect(self.check_proxy)
        self.browser = browserc()
    def get_proxy(self):
        if self.useProxy.isChecked():
            return self.proxyEditor.toPlainText()
        else:
            return ""

    def proxy_change_icon(self, f):
        if f:
            self.proxyVaild.setIcon(QtGui.QIcon(":icon/yes.png"))
        else:
            self.proxyVaild.setIcon(QtGui.QIcon(":icon/no.png"))
        self.proxyVaild.setEnabled(True)

    def check_proxy(self):
        self.proxyVaild.setEnabled(False)
        self.proxy_check_t = proxy_checker(self.get_proxy())
        self.proxy_check_t._signal.connect(self.proxy_change_icon)
        self.proxy_check_t.start()

    def get_steam(self):
        self.steam_cookie = { 'sessionid': "" , 'steamLoginSecure': ""}
        self.browser.get_cookie('https://steamcommunity.com', self.steam_cookie, self.steamCookie)
    def get_buff(self):
        self.buff_cookie = { 'session': "" }
        self.browser.get_cookie('https://buff.163.com', self.buff_cookie, self.buffCookie)

    def crawl_start(self):
        self.crawlStart.setEnabled(False)
        self.crawl_t = crawler()
        self.crawl_t._signal.connect(functools.partial(self.crawlStart.setEnabled, True))
        self.crawl_t.start()
    def log_output(self, text):
        self.logger.moveCursor(QtGui.QTextCursor.End)
        self.logger.insertPlainText(text)

    def on_quit(self, event):
        reply = QMessageBox.question(QtWidgets.QMainWindow(), '信息', '保存配置吗？', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            config.save()
