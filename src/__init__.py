import sys
from PyQt5 import QtWidgets
from src.ui.oddish import oddish

# if __name__ == '__main__':
if True:
    if sys.version_info[:2] == (3, 7):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = oddish(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
