import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget,QTableWidgetItem, QWidget, QAbstractScrollArea, QVBoxLayout, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from managers import users_class_manager, customers_class_manager
from mainwindow import Ui_MainWindow
from resources import resource_rc
from PyQt6.QtCore import Qt, pyqtSignal
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Base = declarative_base()
class PieChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PieChartCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_data(self, user_data):
        categories = ['Standard', 'Admin']
        values = [user_data['standard'], user_data['admin']]

        self.axes.pie(values, labels=categories, autopct='%1.1f%%', startangle=0)
        self.axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.axes.set_title('Users Types')
        self.draw()

class MainWindow(QMainWindow):
    clicked = pyqtSignal()
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
        self.chart1_layout = QVBoxLayout(self.ui.chart1_widget)

        self.ui.Icon_onlywidget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn2.setChecked(True)
        self.adjust_to_screen_size()
        self.showFullScreen()
        #self.showMaximized()
        self.users_table_widget = users_class_manager.User_Manager(
            self.ui.users_tableWidget,
            self.session)
        self.users_table_widget.load_data()

        self.customers_table_widget = customers_class_manager.Customer_Manager(
            self.ui.customers_tableWidget,
            self.session)
        self.customers_table_widget.load_data()

        self.clicked.connect(self.users_table_widget.clear_selection)
    def mousePressEvent(self, event):
        # Emit the clicked signal when the user clicks inside the main window
        self.clicked.emit()
        super().mousePressEvent(event)
    def adjust_to_screen_size(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        self.resize(screen_rect.width(), screen_rect.height())

    ###Buttons actions###
    def on_search_input_changed(self, text):
        print(f"Search input changed: {text}")

    # def on_search_btn_toggled(self):
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
        try:
            self.ui.stackedWidget.setCurrentIndex(2)

            # Pobierz dane o użytkownikach z User_Manager
            user_data = {
                'standard': self.users_table_widget.count_standard_users(),
                'admin': self.users_table_widget.count_admin_users()
            }
            print(user_data)
            # Dodaj wykres kolumnowy do widgetu chart1_widget
            chart_widget = QWidget(self.ui.chart1_widget)
            pie_chart_canvas = PieChartCanvas(chart_widget, width=5, height=4, dpi=100)
            self.chart1_layout.addWidget(pie_chart_canvas)

            # Przekaz dane do wykresu
            pie_chart_canvas.plot_data(user_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


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

