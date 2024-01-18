from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView

import models.products


class Products_Manager(QTableWidget):

    def __init__(self, products_table_widget, session):
        super(Products_Manager, self).__init__()
        self.products_table_widget = products_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.products_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.products_table_widget.setSortingEnabled(True)
        self.products_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)



    def load_data(self):
        self.products_table_widget.setRowCount(0)
        products = self.database_session.query(models.products.Products).all()

        index = 0
        for product in products:
            self.products_table_widget.insertRow(index)

            for col, value in enumerate([str(product.ID), str(product.Name), str(product.Price), str(product.SerialNumber)]):
                item = QTableWidgetItem(value)
                if col in {0,3}: #Columns: "ID" and "Status"
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.products_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.products_table_widget.verticalHeader().setSectionsClickable(True)
        self.products_table_widget.verticalHeader().setFixedWidth(50)
        self.products_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.products_table_widget.verticalHeader().setMinimumSectionSize(50)