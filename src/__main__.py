import sys
from PyQt5 import QtWidgets
from src.ui.oddish import oddish

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = oddish(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
