import sqlite3
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream
import sqlite3
import resource_rc


from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Connect to SQLite database
        self.connection = sqlite3.connect("./database/crm.db")
        self.cursor = self.connection.cursor()


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Icon_onlywidget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn2.setChecked(True)

    def loaddata(self):
        # Clear existing items in the table
        self.ui.tableWidget.setRowCount(0)

        # Execute SQL query to fetch data from the "users" table
        query = "SELECT ID, Login, Password FROM Users"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Populate data into the QTableWidget
        for row_number, row_data in enumerate(data):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                self.ui.tableWidget.setItem(row_number, column_number, item)

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
        self.loaddata()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

