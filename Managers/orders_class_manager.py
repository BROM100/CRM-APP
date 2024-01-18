from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView)
from sqlalchemy import desc, func

import models.orders
from models.customers import Customers
from models.orders import Orders
from models.products import Products


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

    def calculate_total_price(self, order, product_price):
        amount = order.Amount
        discount_percentage = order.Discount / 100  # Assuming Discount is already a percentage
        discount_amount = amount * discount_percentage

        total_price = amount * product_price - discount_amount
        return total_price
    def load_data(self):
        self.orders_table_widget.setRowCount(0)
        orders = self.database_session.query(models.orders.Orders).all()

        index = 0
        for order in orders:
            self.orders_table_widget.insertRow(index)
            customer = order.customer.Name if order.customer else ""
            product = order.product.Name if order.product else ""
            user = order.user.First_Name if order.user else ""
            product_price = order.product.Price if order.product else 0
            total_price = self.calculate_total_price(order, product_price)


            for col, value in enumerate(
                    [str(order.ID), f"{customer}", f"{product}", str(order.Date),
                     f"{user}",str(order.Amount),f"{order.Discount}%",str(total_price)]):
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

    def get_top_selling_products(self, n=5):
        # Fetch the top n selling products and their revenue
        query = self.database_session.query(
            Products.Name,
            func.sum(Orders.Amount * Products.Price - (Orders.Discount / 100 * Orders.Amount)).label('revenue')
        ).join(Products).group_by(Products.Name).order_by(desc('revenue')).limit(n)

        top_products = query.all()
        return top_products

    def get_top_customers(self, n=5):
        # Fetch the top n customers and their total revenue
        query = self.database_session.query(
            Customers.Name,
            func.sum(Orders.Amount * Products.Price - (Orders.Discount / 100 * Orders.Amount)).label('revenue')
        ).join(Products).join(Customers).group_by(Customers.Name).order_by(desc('revenue')).limit(n)

        top_customers = query.all()
        return top_customers