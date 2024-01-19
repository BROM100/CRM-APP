from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QPushButton, QTableWidgetItem, QTableWidget, QMessageBox, QLineEdit, QDialog, QVBoxLayout,
                             QLabel, QAbstractItemView,
                             QHeaderView, QInputDialog)
from collections import defaultdict
# from sqlalchemy.ext.declarative import declarative_base
import models.leads


class LeadAddDialog(QDialog):
    def __init__(self):
        super(LeadAddDialog, self).__init__()

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_edit = QLineEdit()

        self.stock_sector_label = QLabel("Stock Sector")
        self.stock_sector_edit = QLineEdit()

        self.phone_label = QLabel("Phone")
        self.phone_edit = QLineEdit()

        self.source_label = QLabel("Source")
        self.source_edit = QLineEdit()

        self.status_label = QLabel("Status")
        self.status_edit = QLineEdit()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(self.stock_sector_label)
        self.layout.addWidget(self.stock_sector_edit)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_edit)
        self.layout.addWidget(self.source_label)
        self.layout.addWidget(self.source_edit)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_edit)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)


        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.layout)

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
    
    def delete_data(self):
        selected_rows = self.leads_table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete selected rows?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        for selected_row in selected_rows:
            lead_id = int(self.leads_table_widget.item(selected_row.row(), 0).text())
            lead = self.database_session.query(models.leads.Leads).filter_by(ID=lead_id).first()
            if lead:
                self.database_session.delete(lead)

        self.database_session.commit()
        self.load_data()  # Reload data after deletion
        QMessageBox.information(self, "Delete", "Data deleted successfully.")
        
    def save_data(self):

        try:
            rows = self.leads_table_widget.rowCount()
            if rows == 0:
                return


            for row in range(rows):
                lead_id = int(self.leads_table_widget.item(row, 0).text())
                name = self.leads_table_widget.item(row, 1).text()
                email = self.leads_table_widget.item(row, 2).text()
                stocksector = self.leads_table_widget.item(row, 3).text()
                phone = self.leads_table_widget.item(row, 4).text()
                source = self.leads_table_widget.item(row, 5).text()
                status = self.leads_table_widget.item(row, 6).text()
                # Update or insert the lead data into the database
                lead = self.database_session.query(models.leads.Leads).filter_by(ID=lead_id).first()
                if lead:
                    lead.Name = name
                    lead.Email = email
                    lead.StockSector = stocksector
                    lead.Phone = phone
                    lead.Source = source
                    lead.Status = status
                else:
                    new_lead = models.leads.Leads(ID=lead_id, Name=name, Email=email, StockSector=stocksector, Phone=phone, Source=source,Status=status)
                    self.database_session.add(new_lead)

            self.database_session.commit()
            QMessageBox.information(self, "Save", "Data saved successfully.")
        except Exception as e:
            print(f"Error in save_data: {e}")

    def add_new_row(self):

        dialog = LeadAddDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:

            name = dialog.name_edit.text()
            email = dialog.email_edit.text()
            stocksector = dialog.stock_sector_edit.text()
            phone = dialog.phone_edit.text()
            source = dialog.source_edit.text()
            status = dialog.status_edit.text()

            if (name != '') and (email != ''):

                # Generate a new user ID
                new_lead_id = self.generate_new_lead_id()

                # Add the new row to the table
                row_position = self.leads_table_widget.rowCount()
                self.leads_table_widget.insertRow(row_position)

                # Set the new items for the added row
                self.leads_table_widget.setItem(row_position, 0, QTableWidgetItem(str(new_lead_id)))
                self.leads_table_widget.setItem(row_position, 1, QTableWidgetItem(name))
                self.leads_table_widget.setItem(row_position, 2, QTableWidgetItem(email))
                self.leads_table_widget.setItem(row_position, 3, QTableWidgetItem(stocksector))
                self.leads_table_widget.setItem(row_position, 4, QTableWidgetItem(phone))
                self.leads_table_widget.setItem(row_position, 5, QTableWidgetItem(source))
                self.leads_table_widget.setItem(row_position, 6, QTableWidgetItem(status))
                # Update the database with the new user
                new_lead = models.leads.Leads(ID=new_lead_id, Name= name, Email=email, StockSector=stocksector, Phone=phone, Source=source, Status=status)
                self.database_session.add(new_lead)
                self.database_session.commit()
            else:
                QMessageBox.information(self, "Error", "Name and Email can not be empty")
                self.add_new_row()
    def generate_new_lead_id(self):

        existing_lead_ids = [int(self.leads_table_widget.item(row, 0).text()) for row in
                             range(self.leads_table_widget.rowCount())]
        if existing_lead_ids:
            new_lead_id = max(existing_lead_ids) + 1
        else:
            new_lead_id = 1

        return new_lead_id
    def editStatus(self, item):
        # Get the current value in the cell
        current_value = item.text()

        # Create a list of options for the picklist
        options = ['New', 'On hold', 'In progress', 'Closed']

        # Show a popup with a picklist for the lead to choose a new value
        new_value, ok = QInputDialog.getItem(
            self,
            "Edit Status",
            "Choose a new status:",
            options,
            current=0,  # Set the default option to the current value
            editable=False  # Make the picklist read-only
        )

        # If the lead selected a new value, update the cell
        if ok and new_value and new_value != current_value:
            status='status'
            item.setText(new_value)
            row = item.row()
            lead_id = int(self.leads_table_widget.item(row, 0).text())
            self.updateDatabaseStatus(status,lead_id, new_value)

    def editSource(self, item):
        # Get the current value in the cell
        current_value = item.text()

        # Create a list of options for the picklist
        options = ['Events', 'Social media', 'Direct traffic', 'Paid ads', 'Email marketing']

        # Show a popup with a picklist for the lead to choose a new value
        new_value, ok = QInputDialog.getItem(
            self,
            "Edit Source",
            "Choose a new source:",
            options,
            current=0,  # Set the default option to the current value
            editable=False  # Make the picklist read-only
        )

        # If the lead selected a new value, update the cell
        if ok and new_value and new_value != current_value:
            source = 'source'
            item.setText(new_value)
            row = item.row()
            lead_id = int(self.leads_table_widget.item(row, 0).text())
            self.updateDatabaseStatus(source, lead_id, new_value)
    def setupDoubleClickEditing(self, item):

        if item.column() == 6:
            self.editStatus(item)
        elif item.column() == 5:
            self.editSource(item)
    def updateDatabaseStatus(self, field, lead_id, value):
        lead = self.database_session.query(models.leads.Leads).filter_by(ID=lead_id).first()
        if field == 'status':
            lead.Status = value
            self.database_session.commit()
        elif field == 'source':
            lead.Source = value
            self.database_session.commit()

    def calculate_lead_status_source_data(self):
        lead_statuses = ['New', 'On hold', 'In progress', 'Closed']
        lead_sources = ['Events', 'Social media', 'Direct traffic', 'Paid ads', 'Email marketing']

        data = defaultdict(int)

        leads = self.database_session.query(models.leads.Leads).all()

        for lead in leads:
            status = lead.Status
            source = lead.Source
            data[(status, source)] += 1

        lead_data = {
            'statuses': lead_statuses,
            'sources': lead_sources,
            'data': data
        }

        return lead_data