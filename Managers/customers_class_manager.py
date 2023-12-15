from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget,QMessageBox, QLineEdit, QDialog, QVBoxLayout, QLabel, QWidget, QAbstractItemView
from PyQt6.QtCore import Qt, QSortFilterProxyModel,QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon
# from sqlalchemy.ext.declarative import declarative_base
import models.customers

class Customer_Manager(QTableWidget):

    def __init__(self, customers_table_widget, session):
        super(Customer_Manager, self).__init__()
        self.customers_table_widget = customers_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.customers_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.customers_table_widget.setSortingEnabled(True)
        
        
        
    def load_data(self):
        self.customers_table_widget.setRowCount(0)
        customers = self.database_session.query(models.customers.Customers).all()

        index = 0
        for customer in customers:
            self.customers_table_widget.insertRow(index)

            for col, value in enumerate([str(customer.ID), str(customer.Name), str(customer.Address), str(customer.Domain),
                                         str(customer.IBAN), str(customer.Contact_ID), str(customer.Orders_count), str(customer.Lead_ID), str(customer.Department)]):
                item = QTableWidgetItem(value)
                self.customers_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.customers_table_widget.verticalHeader().setSectionsClickable(True)
        self.customers_table_widget.verticalHeader().setFixedWidth(30)
        self.customers_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.customers_table_widget.verticalHeader().setMinimumSectionSize(50)