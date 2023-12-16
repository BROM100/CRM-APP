from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget, QMessageBox, QLineEdit, QDialog, QVBoxLayout, \
    QLabel, QWidget, QAbstractItemView, QHeaderView, QCheckBox
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon
# from sqlalchemy.ext.declarative import declarative_base
import models.contacts


class Contacts_Manager(QTableWidget):

    def __init__(self, contacts_table_widget, session):
        super(Contacts_Manager, self).__init__()
        self.contacts_table_widget = contacts_table_widget
        self.database_session = session

        # Multiselection feature to QtableWidget
        self.contacts_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        # Column Sorting feature to QtableWidget
        self.contacts_table_widget.setSortingEnabled(True)
        self.contacts_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_data(self):
        self.contacts_table_widget.setRowCount(0)
        contacts = self.database_session.query(models.contacts.Contacts).all()

        index = 0
        for contact in contacts:
            self.contacts_table_widget.insertRow(index)

            for col, value in enumerate(
                    [str(contact.ID), str(contact.First_name), str(contact.Last_name), str(contact.Email),
                     str(contact.Phone), str(contact.Gender), str(contact.Do_not_call)]):
                item = QTableWidgetItem(value)
                self.contacts_table_widget.setItem(index, col, item)

                if col == 6:  # Column "Do_not_call"
                    checkbox = QCheckBox()
                    checkbox.setChecked(bool(contact.Do_not_call))
                    self.contacts_table_widget.setCellWidget(index, col, checkbox)
                if col == 0: #Column: "ID"
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            index += 1

        # Set the vertical header to show checkboxes
        self.contacts_table_widget.verticalHeader().setSectionsClickable(True)
        self.contacts_table_widget.verticalHeader().setFixedWidth(30)
        self.contacts_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.contacts_table_widget.verticalHeader().setMinimumSectionSize(50)