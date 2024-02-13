import sys
from resources import resource_rc
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
from datetime import date
import calendar
from matplotlib.colors import LogNorm
import matplotlib.dates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from collections import defaultdict

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
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(ColumnChartCanvas, self).__init__(fig)
        self.setParent(parent)
        self.figure.subplots_adjust(left=0.2)

    def plot_data(self, top_products):
        product_names = [str(product[0]) for product in top_products]
        revenues = [float(product[1]) for product in top_products]

        self.axes.bar(product_names, revenues)
        self.axes.set_ylabel('Revenue')
        self.axes.set_title('Top Selling Products and Revenue')
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.7)
        self.draw()

class BarChartCustomers(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(BarChartCustomers, self).__init__(fig)
        self.setParent(parent)
        self.figure.subplots_adjust(left=0.2)

    def plot_data(self, top_customers, common_color='green'):
        customer_names = [str(customer[0]) for customer in top_customers]
        revenues = [float(customer[1]) for customer in top_customers]

        bars = self.axes.bar(range(len(customer_names)), revenues, color=common_color)
        self.rotate_labels_vertical(bars, customer_names)
        self.axes.set_ylabel('Revenue')
        self.axes.set_title('Top Customers and Revenue')
        self.adjust_layout()
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.7)
        self.draw()

    def adjust_layout(self):
        self.figure.subplots_adjust(right=0.85)

    def rotate_labels_vertical(self, bars, labels):
        for bar, label in zip(bars, labels):
            bar.set_label(label)
            height = bar.get_height()
            self.axes.text(bar.get_x() + bar.get_width() / 2, height / 2, label,
                           ha='center', va='center', rotation='vertical')

class YearlyRevenueChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(YearlyRevenueChartCanvas, self).__init__(fig)
        self.setParent(parent)
        self.figure.subplots_adjust(left=0.2, right=0.95, top=0.9, bottom=0.2)

    def plot_data(self, yearly_revenue):
        years = [str(item[0]) for item in yearly_revenue]
        revenues = [item[1] for item in yearly_revenue]

        self.axes.plot(years, revenues, marker='o', linestyle='-')
        self.axes.set_xlabel('Year')
        self.axes.set_ylabel('Total Revenue')
        self.axes.set_title('Yearly Revenue Summary')
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.7)

        # Set ticks and labels, then rotate the x-axis labels vertically
        self.axes.set_xticks(range(len(years)))
        self.axes.set_xticklabels(years, rotation='vertical')

        self.draw()

class StackedBarChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(StackedBarChartCanvas, self).__init__(fig)
        self.setParent(parent)
        self.figure.subplots_adjust(bottom=0.2)


    def plot_data(self, lead_data):
        lead_statuses = lead_data['statuses']
        lead_sources = lead_data['sources']

        num_statuses = len(lead_statuses)
        num_sources = len(lead_sources)

        # Create a matrix to store data for each combination of status and source
        data_matrix = np.zeros((num_statuses, num_sources), dtype=int)

        # Populate the matrix with the counts for each combination
        for i, status in enumerate(lead_statuses):
            for j, source in enumerate(lead_sources):
                count = lead_data['data'][(status, source)]
                data_matrix[i, j] = count

        # Plot the stacked bar chart
        bars = self.axes.bar(range(num_statuses), data_matrix[:, 0], label=lead_sources[0])

        for i in range(1, num_sources):
            bars = self.axes.bar(range(num_statuses), data_matrix[:, i],
                                 bottom=np.sum(data_matrix[:, :i], axis=1),
                                 label=lead_sources[i])

        self.axes.set_xlabel('Lead Status')
        self.axes.set_ylabel('Count')
        self.axes.set_title('Lead Status vs. Lead Source')
        self.axes.set_xticks(range(num_statuses))
        self.axes.set_xticklabels(lead_statuses)
        self.axes.legend()
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.7)
        self.draw()

class HeatmapChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(HeatmapChartCanvas, self).__init__(fig)
        self.setParent(parent)
        self.figure.subplots_adjust(left= 0.2)

    def plot_data(self, monthly_revenue):

        years = sorted(list(monthly_revenue.keys()))
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        months = sorted(list(monthly_revenue[years[0]].keys()), key=lambda x: month_order.index(x))

        # Create a matrix to store data for each month
        revenue_matrix = [[monthly_revenue[year][month] for year in years] for month in months]

        cmap = cm.get_cmap('Blues')
        im = self.axes.imshow(revenue_matrix, cmap=cmap, vmin=0, vmax=np.max(revenue_matrix))

        self.axes.set_xticks(range(len(years)))
        self.axes.set_xticklabels(years, rotation='vertical')

        self.axes.set_yticks(range(len(months)))
        self.axes.set_yticklabels(months, rotation='horizontal')

        self.axes.set_xlabel('Year')
        self.axes.set_ylabel('Month')
        self.axes.set_title('Monthly Revenue Heatmap')

        self.figure.colorbar(im)
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
        self.setWindowTitle("CRM")
        self.chart1_layout = QVBoxLayout(self.ui.chart1_widget)
        self.chart2_layout = QVBoxLayout(self.ui.chart2_widget)
        self.chart3_layout = QVBoxLayout(self.ui.chart3_widget)
        self.chart4_layout = QVBoxLayout(self.ui.chart4_widget)
        self.chart5_layout = QVBoxLayout(self.ui.chart5_widget)
        self.chart6_layout = QVBoxLayout(self.ui.chart6_widget)

        # self.ui.chart1_widget.setFixedSize(500, 450)
        # self.ui.chart2_widget.setFixedSize(550, 450)
        # self.ui.chart3_widget.setFixedSize(550, 450)
        # self.ui.chart4_widget.setFixedSize(680, 580)
        # self.ui.chart5_widget.setFixedSize(680, 580)
        # self.ui.chart6_widget.setFixedSize(680, 590)

        self.ui.Icon_onlywidget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn2.setChecked(True)

        self.adjust_to_screen_size()
        #self.showFullScreen()
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
        screen_rect = screen.availableGeometry()  # Use availableGeometry() instead of geometry() to exclude taskbars
        taskbar_height = screen.geometry().height() - screen_rect.height()  # Calculate taskbar height
        self.resize(screen_rect.width(), screen_rect.height() - taskbar_height)


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
        try:
            # Fetch yearly revenue data
            yearly_revenue = self.orders_table_wiget.calculate_yearly_revenue()

            # Clear the layout of chart4_widget
            self.clear_layout(self.ui.chart4_widget.layout())

            # Create a new chart canvas for yearly revenue and add it to chart4_widget
            chart_widget = QWidget(self.ui.chart4_widget)
            yearly_revenue_canvas = YearlyRevenueChartCanvas(chart_widget, width=8, height=6, dpi=100)
            self.ui.chart4_widget.layout().addWidget(yearly_revenue_canvas)

            # Plot data on the yearly revenue chart
            yearly_revenue_canvas.plot_data(yearly_revenue)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        try:
            # Calculate lead data for stacked bar chart
            lead_data = self.leads_table_widget.calculate_lead_status_source_data()

            # Clear the layout of chart5_widget
            self.clear_layout(self.ui.chart5_widget.layout())

            # Create the stacked bar chart canvas and add it to chart5_widget
            chart_widget = QWidget(self.ui.chart5_widget)
            stacked_bar_chart_canvas = StackedBarChartCanvas(chart_widget, width=8, height=6, dpi=100)
            self.ui.chart5_widget.layout().addWidget(stacked_bar_chart_canvas)

            # Plot data on the stacked bar chart
            stacked_bar_chart_canvas.plot_data(lead_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        try:
            # Fetch monthly revenue data
            monthly_revenue = self.orders_table_wiget.calculate_monthly_revenue()

            # Clear the layout of chart6_widget
            self.clear_layout(self.ui.chart6_widget.layout())

            # Create a new heatmap canvas for monthly revenue and add it to chart6_widget
            chart_widget = QWidget(self.ui.chart6_widget)
            heatmap_canvas = HeatmapChartCanvas(chart_widget, width=8, height=6, dpi=100)
            self.ui.chart6_widget.layout().addWidget(heatmap_canvas)

            # Plot data on the heatmap
            heatmap_canvas.plot_data(monthly_revenue)

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

