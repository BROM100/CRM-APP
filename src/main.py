import sys
from resources import resource_rc
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mainwindow import Ui_MainWindow
from managers import users_class_manager, customers_class_manager, contacts_class_manager, leads_class_manager, \
    products_class_manager, orders_class_manager


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
class ColumnChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(ColumnChartCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_data(self, top_products):
        product_names = [str(product[0]) for product in top_products]
        revenues = [float(product[1]) for product in top_products]

        self.axes.bar(product_names, revenues)
        self.axes.set_ylabel('Revenue')
        self.axes.set_title('Top Selling Products and Revenue')
        self.draw()

class BarChartCustomers(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(BarChartCustomers, self).__init__(fig)
        self.setParent(parent)

    def plot_data(self, top_customers, common_color='green'):
        customer_names = [str(customer[0]) for customer in top_customers]
        revenues = [float(customer[1]) for customer in top_customers]

        bars = self.axes.bar(range(len(customer_names)), revenues, color=common_color)
        self.rotate_labels_vertical(bars, customer_names)
        self.axes.set_ylabel('Revenue')
        self.axes.set_title('Top Customers and Revenue')
        self.adjust_layout()
        self.draw()

    def adjust_layout(self):
        self.figure.subplots_adjust(right=0.85)

    def rotate_labels_vertical(self, bars, labels):
        for bar, label in zip(bars, labels):
            bar.set_label(label)
            height = bar.get_height()
            self.axes.text(bar.get_x() + bar.get_width() / 2, height / 2, label,
                           ha='center', va='center', rotation='vertical')


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
        self.chart2_layout = QVBoxLayout(self.ui.chart2_widget)
        self.chart3_layout = QVBoxLayout(self.ui.chart3_widget)
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

        self.leads_table_widget = leads_class_manager.Leads_Manager(
            self.ui.leads_tableWidget,
            self.session)
        self.leads_table_widget.load_data()

        self.contacts_table_widget = contacts_class_manager.Contacts_Manager(
            self.ui.contacts_tableWidget,
            self.session)
        self.contacts_table_widget.load_data()

        self.customers_table_widget = customers_class_manager.Customer_Manager(
            self.ui.customers_tableWidget,
            self.session)
        self.customers_table_widget.load_data()

        self.products_table_wiget = products_class_manager.Products_Manager(
            self.ui.products_tableWidget,
            self.session)
        self.products_table_wiget.load_data()

        self.orders_table_wiget = orders_class_manager.Orders_Manager(
            self.ui.orders_tableWidget,
            self.session)
        self.orders_table_wiget.load_data()

        self.clicked.connect(self.users_table_widget.clear_selection)
        self.clicked.connect(self.customers_table_widget.clear_selection)
        self.clicked.connect(self.contacts_table_widget.clear_selection)
        self.clicked.connect(self.leads_table_widget.clear_selection)
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
    """users_tableWidget CRUD buttons"""
    def on_add_user_pressed(self):
        self.users_table_widget.add_new_row()
    def on_save_user_pressed(self):
        self.users_table_widget.save_data()
    def on_delete_user_pressed(self):
        self.users_table_widget.delete_data()


    """customers_tableWidget CRUD buttons"""
    def on_add_customer_pressed(self):
        self.customers_table_widget.add_new_row()
    def on_save_customer_pressed(self):
        self.customers_table_widget.save_data()
    def on_delete_customer_pressed(self):
        self.customers_table_widget.delete_data()

    """contacts_tableWidget CRUD buttons"""

    def on_add_contact_pressed(self):
        self.contacts_table_widget.add_new_row()

    def on_save_contact_pressed(self):
        self.contacts_table_widget.save_data()

    def on_delete_contact_pressed(self):
        self.contacts_table_widget.delete_data()

    """leads_tableWidget CRUD buttons"""
    def on_add_lead_pressed(self):
        self.leads_table_widget.add_new_row()

    def on_save_lead_pressed(self):
        self.leads_table_widget.save_data()

    def on_delete_lead_pressed(self):
        self.leads_table_widget.delete_data()


    def on_home_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashboard_btn1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        try:


            # Fetch top selling products and their revenue
            top_products = self.orders_table_wiget.get_top_selling_products()

            self.clear_layout(self.ui.chart2_widget.layout())  # Clear chart2_widget layout

            # Create the column chart canvas and add it to chart2_widget
            chart_widget = QWidget(self.ui.chart2_widget)
            column_chart_canvas = ColumnChartCanvas(chart_widget, width=5, height=4, dpi=100)
            self.ui.chart2_widget.layout().addWidget(column_chart_canvas)

            # Plot data on the column chart
            column_chart_canvas.plot_data(top_products)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        try:


            user_data = {
                'standard': self.users_table_widget.count_standard_users(),
                'admin': self.users_table_widget.count_admin_users()
            }

            self.clear_layout(self.chart1_layout)

            chart_widget = QWidget(self.ui.chart1_widget)
            pie_chart_canvas = PieChartCanvas(chart_widget, width=5, height=4, dpi=100)
            self.chart1_layout.addWidget(pie_chart_canvas)


            pie_chart_canvas.plot_data(user_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        try:
            # Fetch top customers and their revenue
            top_customers = self.orders_table_wiget.get_top_customers()

            # Clear the layout of chart3_widget
            self.clear_layout(self.ui.chart3_widget.layout())

            # Create the bar chart canvas and add it to chart3_widget
            chart_widget = QWidget(self.ui.chart3_widget)
            bar_chart_customers = BarChartCustomers(chart_widget, width=5, height=4, dpi=100)
            self.ui.chart3_widget.layout().addWidget(bar_chart_customers)

            # Plot data on the bar chart
            bar_chart_customers.plot_data(top_customers)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())

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



    #def on_search_btn_toggled(self):


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("./src/style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

