import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget,QTableWidgetItem, QWidget, QAbstractScrollArea
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from managers import users_class_manager
from mainwindow import Ui_MainWindow
from resources import resource_rc

#Base = declarative_base()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        # Connect to SQLite database
        self.engine = create_engine(f"sqlite:///database/crm.db")
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        ###########################################


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Icon_onlywidget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn2.setChecked(True)
        self.adjust_to_screen_size()
        self.showMaximized()
        self.users_table_widget = users_class_manager.User_Manager(
            self.ui.users_tableWidget,
            self.session)
        self.users_table_widget.load_data()
        

        # Execute SQL query to fetch data from the "users" table
        # query = "SELECT ID, Login, Password FROM Users"
        # self.cursor.execute(query)
        # data = self.cursor.fetchall()

        # Populate data into the QTableWidget
        # for row_number, row_data in enumerate(data):
        #     self.ui.tableWidget.insertRow(row_number)
        #     for column_number, column_data in enumerate(row_data):
        #         item = QTableWidgetItem(str(column_data))
        #         self.ui.tableWidget.setItem(row_number, column_number, item)

    def adjust_to_screen_size(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        self.resize(screen_rect.width(), screen_rect.height())
   # def on_search_btn_toggled(self):

    def on_search_input_changed(self, text):
        print(f"Search input changed: {text}")
    #Buttons actions
    def on_add_user_pressed(self):
        self.users_table_widget.add_new_row()

    def on_save_user_pressed(self):
        self.users_table_widget.save_data()
    def on_delete_user_pressed(self):
        self.users_table_widget.delete_data()
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
        #self.users_table_widget.ui = self.ui
        self.users_table_widget.set_row_height(1)
        # self.users_table_widget.set_column_width(0,35)
        self.users_table_widget.set_column_width(200)


    # def on_search_btn_toggled(self):
    #     self.ui.users_tableWidget.search_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("./src/style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

