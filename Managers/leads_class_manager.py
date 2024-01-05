from PyQt6.QtWidgets import (QPushButton, QTableWidgetItem, QTableWidget,QMessageBox, QLineEdit, QDialog, QVBoxLayout, QLabel, QWidget, QAbstractItemView,
                             QHeaderView, QInputDialog)
from PyQt6.QtCore import Qt, QSortFilterProxyModel,QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon
# from sqlalchemy.ext.declarative import declarative_base
import models.leads


class Leads_Manager(QTableWidget):

    def __init__(self, leads_table_widget, session):
        super(Leads_Manager, self).__init__()
        self.leads_table_widget = leads_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.leads_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.leads_table_widget.setSortingEnabled(True)
        self.leads_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.leads_table_widget.itemDoubleClicked.connect(

            self.setupDoubleClickEditing

        )
    def clear_selection(self):
        # Clear the selection in the QTableWidget
        self.leads_table_widget.selectionModel().clearSelection()
    def load_data(self):
        self.leads_table_widget.setRowCount(0)
        leads = self.database_session.query(models.leads.Leads).all()

        index = 0
        for lead in leads:
            self.leads_table_widget.insertRow(index)

            for col, value in enumerate([str(lead.ID), str(lead.Name), str(lead.Email), str(lead.StockSector),
                                         str(lead.Phone), str(lead.Source), str(lead.Status)]):
                item = QTableWidgetItem(value)
                if col in {0,6}: #Columns: "ID" and "Status"
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.leads_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.leads_table_widget.verticalHeader().setSectionsClickable(True)
        self.leads_table_widget.verticalHeader().setFixedWidth(50)
        self.leads_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.leads_table_widget.verticalHeader().setMinimumSectionSize(50)

    def editStatus(self, item):
        # Get the current value in the cell
        current_value = item.text()

        # Create a list of options for the picklist
        options = ['New', 'On hold', 'In progress', 'Closed']

        # Show a popup with a picklist for the user to choose a new value
        new_value, ok = QInputDialog.getItem(
            self,
            "Edit Status",
            "Choose a new status:",
            options,
            current=0,  # Set the default option to the current value
            editable=False  # Make the picklist read-only
        )

        # If the user selected a new value, update the cell
        if ok and new_value and new_value != current_value:
            item.setText(new_value)
            row = item.row()
            lead_id = int(self.leads_table_widget.item(row, 0).text())
            self.updateDatabaseStatus(lead_id, new_value)
    def setupDoubleClickEditing(self, item):

        if item.column() == 6:
            self.editStatus(item)


    def updateDatabaseStatus(self, lead_id, new_status):
        lead = self.database_session.query(models.leads.Leads).filter_by(ID=lead_id).first()
        lead.Status = new_status
        self.database_session.commit()