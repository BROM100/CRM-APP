from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QMessageBox, QAbstractItemView, QHeaderView, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
import models.contacts

class UserAddDialog(QDialog):
    def __init__(self):
        super(UserAddDialog, self).__init__()


        self.first_name_label = QLabel("First Name")
        self.first_name_edit = QLineEdit()

        self.last_name_label = QLabel("Last Name")
        self.last_name_edit = QLineEdit()

        self.email_label = QLabel("Email")
        self.email_edit = QLineEdit()

        self.phone_label = QLabel("Phone")
        self.phone_edit = QLineEdit()

        self.gender_label = QLabel("Gender")
        self.gender_edit = QLineEdit()

        self.do_not_call_label = QLabel("Do Not Call")
        self.do_not_call_edit = QLineEdit()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_edit)
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_edit)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_edit)
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.gender_edit)
        self.layout.addWidget(self.do_not_call_label)
        self.layout.addWidget(self.do_not_call_edit)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)


        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.layout)
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
    def clear_selection(self):
        # Clear the selection in the QTableWidget
        self.contacts_table_widget.selectionModel().clearSelection()
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

                if col == 0: #Column: "ID"
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.contacts_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.contacts_table_widget.verticalHeader().setSectionsClickable(True)
        self.contacts_table_widget.verticalHeader().setFixedWidth(30)
        self.contacts_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.contacts_table_widget.verticalHeader().setMinimumSectionSize(50)
        
    def save_data(self):

        try:
            rows = self.contacts_table_widget.rowCount()
            if rows == 0:
                return

            for row in range(rows):
                contact_id = int(self.contacts_table_widget.item(row, 0).text())
                firstname = self.contacts_table_widget.item(row, 1).text()
                lastname = self.contacts_table_widget.item(row, 2).text()
                email = self.contacts_table_widget.item(row, 3).text()
                phone = self.contacts_table_widget.item(row, 4).text()
                gender = self.contacts_table_widget.item(row, 5).text()
                do_not_call = self.contacts_table_widget.item(row, 6).text()
                # Update or insert the contact data into the database
                contact = self.database_session.query(models.contacts.Contacts).filter_by(ID=contact_id).first()
                print(contact)
                if contact:
                    contact.First_name = firstname
                    contact.Last_name = lastname
                    contact.Email = email
                    contact.Phone = phone
                    contact.Gender = gender
                    contact.Do_not_call = do_not_call
                else:
                    new_contact = models.contacts.Contacts(ID=contact_id, First_name=firstname, Last_name=lastname, Email=email, Phone=phone, Gender=gender, Do_not_call=do_not_call)
                    self.database_session.add(new_contact)

            self.database_session.commit()
            QMessageBox.information(self, "Save", "Data saved successfully.")
        except Exception as e:
            print(f"Error in save_data: {e}")

    def delete_data(self):
        selected_rows = self.contacts_table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete selected rows?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        deleted = 0
        for selected_row in selected_rows:
            contact_id = int(self.contacts_table_widget.item(selected_row.row(), 0).text())

            query = text("""
                SELECT COUNT(*) 
                FROM customers 
                WHERE contact_id = :contact_id
            """)
            result = self.database_session.execute(query, {"contact_id": contact_id}).scalar()

            if result > 0:
                QMessageBox.warning(self, "Delete", "Cannot delete contact with associated customer.")
                continue

            # If no associated customer, proceed with deletion
            contact = self.database_session.query(models.contacts.Contacts).filter_by(ID=contact_id).first()
            if contact:
                self.database_session.delete(contact)
                deleted += 1
        if deleted > 0:
            self.database_session.commit()
            QMessageBox.information(self, "Delete", "Data deleted successfully.")

        self.load_data()  # Reload data after deletion

    def add_new_row(self):
        print("Signal emitted: add_new_row")
        # Create an instance of the dialog for adding a new contact
        dialog = UserAddDialog()

        # Show the dialog and wait for the contact's input
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # If the contact clicked OK, retrieve the entered data
            
            firstname = dialog.first_name_edit.text()
            lastname = dialog.last_name_edit.text()
            email = dialog.email_edit.text()
            phone = dialog.phone_edit.text()
            gender = dialog.gender_edit.text()
            do_not_call = dialog.do_not_call_edit.text()
            
            


            new_contact_id = self.generate_new_contact_id()

            # Add the new row to the table
            row_position = self.contacts_table_widget.rowCount()
            self.contacts_table_widget.insertRow(row_position)

            # Set the new items for the added row
            self.contacts_table_widget.setItem(row_position, 0, QTableWidgetItem(str(new_contact_id)))
            self.contacts_table_widget.setItem(row_position, 1, QTableWidgetItem(firstname))
            self.contacts_table_widget.setItem(row_position, 2, QTableWidgetItem(lastname))
            self.contacts_table_widget.setItem(row_position, 3, QTableWidgetItem(email))
            self.contacts_table_widget.setItem(row_position, 4, QTableWidgetItem(phone))
            self.contacts_table_widget.setItem(row_position, 5, QTableWidgetItem(gender))
            self.contacts_table_widget.setItem(row_position, 6, QTableWidgetItem(do_not_call))
            # Update the database with the new contact
            new_contact = models.contacts.Contacts(ID=new_contact_id, First_name=firstname, Last_name=lastname, Email=email, Phone=phone, Gender=gender, Do_not_call=do_not_call )
            self.database_session.add(new_contact)
            self.database_session.commit()

            self.add_new_row()
    def generate_new_contact_id(self):

        existing_contact_id = [int(self.contacts_table_widget.item(row, 0).text()) for row in
                             range(self.contacts_table_widget.rowCount())]
        if existing_contact_id:
            new_contact_id = max(existing_contact_id) + 1
        else:
            new_contact_id = 1

        return new_contact_id
