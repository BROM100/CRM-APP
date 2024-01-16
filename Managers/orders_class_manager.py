from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget,QMessageBox, QLineEdit, QDialog, QVBoxLayout, QLabel, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel,QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon

import models.orders
from models.orders import Orders


class Orders_Manager(QTableWidget):

    def __init__(self, orders_table_widget, session):
        super(Orders_Manager, self).__init__()
        self.orders_table_widget = orders_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.orders_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.orders_table_widget.setSortingEnabled(True)
        self.orders_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def load_data(self):
        self.orders_table_widget.setRowCount(0)
        orders = self.database_session.query(models.orders.Orders).all()

        index = 0
        for order in orders:
            self.orders_table_widget.insertRow(index)
            customer = order.customer.Name if order.customer else ""
            product = order.product.Name if order.product else ""
            user = order.user.First_Name if order.user else ""

            for col, value in enumerate(
                    [str(order.ID), f"{customer}", f"{product}", str(order.Date),
                     f"{user}",str(order.Amount),str(order.Discount),str(order.Total)]):
                item = QTableWidgetItem(value)

                if col in {0,7}:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.orders_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.orders_table_widget.verticalHeader().setSectionsClickable(True)
        self.orders_table_widget.verticalHeader().setFixedWidth(30)
        self.orders_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.orders_table_widget.verticalHeader().setMinimumSectionSize(50)