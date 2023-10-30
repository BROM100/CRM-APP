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

    def on_home_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashboard_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_dashboard_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_orders_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_orders_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_products_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_products_btn2_toggled(self, ):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_customers_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_customers_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_contacts_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_contacts_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def on_leads_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def on_leads_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

