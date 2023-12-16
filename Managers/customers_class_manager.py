from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget,QMessageBox, QLineEdit, QDialog, QVBoxLayout, QLabel, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel,QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload
import models.customers
import uuid

class Customer_Manager(QTableWidget):

    def __init__(self, customers_table_widget, session):
        super(Customer_Manager, self).__init__()
        self.customers_table_widget = customers_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.customers_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.customers_table_widget.setSortingEnabled(True)
        self.customers_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.customers_table_widget.itemDoubleClicked.connect(
            self.show_contact_details
        )

        
    def load_data(self):
        self.customers_table_widget.setRowCount(0)
        customers = self.database_session.query(models.customers.Customers).all()

        index = 0
        for customer in customers:
            self.customers_table_widget.insertRow(index)

            contact_first_name = customer.contact.First_name if customer.contact else ""
            contact_last_name = customer.contact.Last_name if customer.contact else ""

            for col, value in enumerate(
                    [str(customer.ID), str(customer.Name), str(customer.Address), str(customer.Domain),
                     str(customer.IBAN), f"{contact_first_name} {contact_last_name}", str(customer.Orders_count),
                     str(customer.Lead_ID), str(customer.Department)]):
                item = QTableWidgetItem(value)

                if col in {0,5}: #Columns: "ID" and "Contact"
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.customers_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.customers_table_widget.verticalHeader().setSectionsClickable(True)
        self.customers_table_widget.verticalHeader().setFixedWidth(30)
        self.customers_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.customers_table_widget.verticalHeader().setMinimumSectionSize(50)

    def show_contact_details(self, item):

        if item.column() == 5:
            row = item.row()
            try:
                customer_id_item = self.customers_table_widget.item(row, 0)
                if customer_id_item is not None:
                    customer_id_str = customer_id_item.text()
                    print(f"Retrieved customer ID: {customer_id_str}")
                else:
                    print("Failed to retrieve customer ID item")
                    return
            except ValueError as e:
                print(f"Error retrieving customer ID: {e}")
                return

            try:
                customer = (
                    self.database_session.query(models.customers.Customers)
                    .filter(models.customers.Customers.ID == customer_id_str)
                    .options(
                        joinedload(models.customers.Customers.contact)
                    )
                    .first()
                )

                if customer is None:
                    print(f"No customer found with ID: {customer_id_str}")
                    return

                # Extract contact details
                contact_first_name = (
                    customer.contact.First_name if customer.contact else ""
                )
                contact_last_name = (
                    customer.contact.Last_name if customer.contact else ""
                )
                print(contact_first_name)

                # Open the dialog with contact details
                dialog = DetailsDialog(
                    f"{contact_first_name} {contact_last_name}",
                    customer.contact.Email if customer.contact else "",
                    customer.contact.Phone if customer.contact else "",
                )
                dialog.exec()

            except Exception as e:
                print(f"Error querying customer: {e}")
class DetailsDialog(QDialog):
    def __init__(self, name, email, phone):
        super(DetailsDialog, self).__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Name: {name}"))
        layout.addWidget(QLabel(f"Email: {email}"))
        layout.addWidget(QLabel(f"Phone: {phone}"))

        self.setLayout(layout)
        self.setWindowTitle("Contact Details")