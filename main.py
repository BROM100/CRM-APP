import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream

import resource_rc


from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Icon_onlywidget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn2.setChecked(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

