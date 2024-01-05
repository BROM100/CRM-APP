from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QPushButton, QTableWidgetItem, QTableWidget, QMessageBox, QLineEdit, QDialog, QVBoxLayout,
                             QLabel, QAbstractItemView, QHeaderView, QComboBox, QDialogButtonBox, QFormLayout,
                             QCheckBox)

import models.customers
from models.customers import Customers


class CreateCustomerDialog(QDialog):
    def __init__(self, generate_new_customer_id, existing_contacts, parent=None):
        super(CreateCustomerDialog, self).__init__(parent)
        self.generate_new_customer_id = generate_new_customer_id
        self.existing_contacts = existing_contacts
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.domain_edit = QLineEdit()
        self.iban_edit = QLineEdit()
        self.orders_count_edit = QLineEdit()
        self.lead_id_edit = QLineEdit()
        self.department_edit = QLineEdit()

        self.contact_id_combo = QComboBox()
        self.contact_id_combo.addItem("Choose Contact", None)  # Default option

        # Populate contact combo with existing contacts
        for contact in self.existing_contacts:
            contact_text = f"{contact.First_name} {contact.Last_name} (ID: {contact.ID})"
            self.contact_id_combo.addItem(contact_text, contact.ID)



        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_edit)
        layout.addWidget(QLabel("Domain:"))
        layout.addWidget(self.domain_edit)
        layout.addWidget(QLabel("IBAN:"))
        layout.addWidget(self.iban_edit)
        # layout.addWidget(QLabel("Orders Count:"))
        # layout.addWidget(self.orders_count_edit)
        # layout.addWidget(QLabel("Lead ID:"))
        # layout.addWidget(self.lead_id_edit)
        layout.addWidget(QLabel("Department:"))
        layout.addWidget(self.department_edit)
        layout.addWidget(QLabel("Contact ID:"))
        layout.addWidget(self.contact_id_combo)


        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Create Customer")

    def accept(self):
        try:
            new_customer = Customers(
                ID=self.generate_new_customer_id(),
                Name=self.name_edit.text(),
                Address=self.address_edit.text(),
                Domain=self.domain_edit.text(),
                IBAN=self.iban_edit.text(),
                #Orders_count=self.orders_count_edit.text(),
                #Lead_ID=int(self.lead_id_edit.text()),
                Department=self.department_edit.text(),
                Contact_ID=self.contact_id_combo.currentData()  # Get the ID of the selected contact
            )

            # Save the new customer to the database
            self.parent().database_session.add(new_customer)
            self.parent().database_session.commit()

            # Close the dialog
            super(CreateCustomerDialog, self).accept()
        except Exception as e:
            print(f"Error in accept: {e}")

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

    def clear_selection(self):
        # Clear the selection in the QTableWidget
        self.customers_table_widget.selectionModel().clearSelection()
    def load_data(self):
        self.customers_table_widget.setRowCount(0)
        customers = self.database_session.query(models.customers.Customers).all()

        index = 0
        for customer in customers:
            self.customers_table_widget.insertRow(index)
            lead = customer.lead.Name if customer.lead else ""
            contact_first_name = customer.contact.First_name if customer.contact else ""
            contact_last_name = customer.contact.Last_name if customer.contact else ""

            for col, value in enumerate(
                    [str(customer.ID), str(customer.Name), str(customer.Address), str(customer.Domain),
                     str(customer.IBAN), f"{contact_first_name} {contact_last_name}", str(customer.Orders_count),
                     f"{lead}", str(customer.Department)]):
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
    def save_data(self):

        try:
            rows = self.customers_table_widget.rowCount()
            if rows == 0:
                return


            for row in range(rows):
                customer_id = int(self.customers_table_widget.item(row, 0).text())
                name = self.customers_table_widget.item(row, 1).text()
                address = self.customers_table_widget.item(row, 2).text()
                domain = self.customers_table_widget.item(row, 3).text()
                iban = self.customers_table_widget.item(row, 4).text()
                #contact_id = self.customers_table_widget.item(row, 5).text()
                orders_count = self.customers_table_widget.item(row, 6).text()
                lead_id = self.customers_table_widget.item(row, 7).text()
                department = self.customers_table_widget.item(row, 8).text()
                # Update or insert the customer data into the database
                customer = self.database_session.query(models.customers.Customers).filter_by(ID=customer_id).first()
                if customer:
                    customer.Name = name
                    customer.Address = address
                    customer.Domain = domain
                    customer.IBAN = iban
                    #customer.Contact_ID = contact_id
                    customer.Orders_count = orders_count
                    customer.Lead_ID = lead_id
                    customer.Department = department
                else:
                    new_customer = models.customers.Customers(ID=customer_id, Name=name, Address=address,
                                                              Domain=domain, IBAN=iban, #Contact_ID=contact_id,
                                                              Orders_count=orders_count, Lead_ID=lead_id, Department=department )

                    self.database_session.add(new_customer)

            self.database_session.commit()
            QMessageBox.information(self, "Save", "Data saved successfully.")
        except Exception as e:
            print(f"Error in save_data: {e}")

    def delete_data(self):
        selected_rows = self.customers_table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete selected rows?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        for selected_row in selected_rows:
            customer_id = int(self.customers_table_widget.item(selected_row.row(), 0).text())
            customer = self.database_session.query(models.customers.Customers).filter_by(ID=customer_id).first()
            if customer:
                self.database_session.delete(customer)

        self.database_session.commit()
        self.load_data()  # Reload data after deletion
        QMessageBox.information(self, "Delete", "Data deleted successfully.")

    def generate_new_customer_id(self):
        existing_customers_ids = [
            int(self.customers_table_widget.item(row, 0).text())
            for row in range(self.customers_table_widget.rowCount())
        ]
        if existing_customers_ids:
            new_customer_id = max(existing_customers_ids) + 1
        else:
            new_customer_id = 1

        return new_customer_id

    def add_new_row(self):
        existing_contacts = self.database_session.query(models.contacts.Contacts).all()
        create_customer_dialog = CreateCustomerDialog(self.generate_new_customer_id, existing_contacts, self)
        result = create_customer_dialog.exec()

        # Handle the result if needed
        if result == QDialog.DialogCode.Accepted:
            # Reload data after creating a new customer
            self.load_data()


    def show_contact_details(self, item):
        if item.column() == 5:  # "Contact" column
            row = item.row()
            customer_id_item = self.customers_table_widget.item(row, 0)
            if customer_id_item is not None:
                customer_id_str = customer_id_item.text()
            else:
                print("Failed to retrieve customer ID item")
                return

            try:
                self.customer = (
                    self.database_session.query(models.customers.Customers)
                    .filter(models.customers.Customers.ID == customer_id_str)
                    .first()
                )

                if self.customer is None:
                    print(f"No customer found with ID: {customer_id_str}")
                    return

                contact = self.customer.contact

                if contact is None:
                    # If the customer doesn't have a contact, open the dialog to choose an existing contact
                    existing_contacts = self.database_session.query(models.contacts.Contacts).all()
                    dialog = ChooseContactDialog(self, existing_contacts)
                    result = dialog.exec()

                    if result == QDialog.DialogCode.Accepted:
                        selected_contact = dialog.get_selected_contact()
                        if selected_contact:
                            self.customer.contact = selected_contact
                            self.database_session.commit()
                        else:
                            # If no contact was selected, return to prevent further execution
                            return
                else:
                    # If the user clicks on a cell with a contact, proceed with the normal logic
                    # Open the dialog for editing contact details
                    dialog = EditContactDialog(self, contact)
                    result = dialog.exec()


                    if result == QDialog.DialogCode.Accepted:
                        # Save the changes to the database
                        self.database_session.commit()

            except Exception as e:
                print(f"Error querying customer: {e}")

        # Reload data after showing contact details
        self.load_data()
class EditContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super(EditContactDialog, self).__init__(parent)

        self.contact = contact

        layout = QVBoxLayout()

        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Male", "Female"])
        self.do_not_call_checkbox = QCheckBox("Do Not Call")

        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name_edit)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.last_name_edit)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(self.phone_edit)
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender_combo)
        layout.addWidget(self.do_not_call_checkbox)

        if self.contact:
            delete_button = QPushButton("Delete Contact")
            delete_button.clicked.connect(self.delete_contact)
            layout.addWidget(delete_button)
        else:
            choose_existing_button = QPushButton("Choose Existing Contact")
            choose_existing_button.clicked.connect(self.choose_existing_contact)
            layout.addWidget(choose_existing_button)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Edit Contact Details")

        if contact:
            self.first_name_edit.setText(contact.First_name)
            self.last_name_edit.setText(contact.Last_name)
            self.email_edit.setText(contact.Email)
            self.phone_edit.setText(contact.Phone)
            self.gender_combo.setCurrentText(contact.Gender)
            self.do_not_call_checkbox.setChecked(contact.Do_not_call)
    def delete_contact(self):
        # If there is no contact associated, close the dialog
        if not self.contact or not self.parent().customer:
            super(EditContactDialog, self).reject()
            return

        # Ask for confirmation before deleting the contact
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Icon.Question)
        confirm_dialog.setWindowTitle("Confirm Deletion")
        confirm_dialog.setText("Are you sure you want to delete this contact?")
        confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm_dialog.setDefaultButton(QMessageBox.StandardButton.No)

        # Execute the confirmation dialog
        result = confirm_dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            try:
                # Remove the current customer from the list of associated customers
                self.parent().customer.contact = None
                self.parent().database_session.commit()
                self.parent().show_contact_details(self.parent().customers_table_widget.currentItem())
                # Close the dialog
                super(EditContactDialog, self).accept()
                # Reload data after deleting the contact
                self.parent().load_data()



            except Exception as e:
                print(f"Error deleting contact: {e}")
                # Handle the error, show a message box, or log it as needed
        else:
            # User chose not to delete, do nothing
            pass
    def choose_existing_contact(self):
        # If there is no contact associated, open the dialog for choosing an existing contact
        if not self.contact:
            existing_contacts = self.parent().database_session.query(models.contacts.Contacts).all()
            dialog = ChooseContactDialog(self, existing_contacts)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                selected_contact = dialog.get_selected_contact()
                if selected_contact:
                    self.contact = selected_contact
                    self.first_name_edit.setText(self.contact.First_name)
                    self.last_name_edit.setText(self.contact.Last_name)
                    self.email_edit.setText(self.contact.Email)
                    self.phone_edit.setText(self.contact.Phone)
        else:
            # If the contact already exists, allow editing
            super(EditContactDialog, self).choose_existing_contact()

    def accept(self):
        # Save the edited contact details
        if self.contact:
            self.contact.First_name = self.first_name_edit.text()
            self.contact.Last_name = self.last_name_edit.text()
            self.contact.Email = self.email_edit.text()
            self.contact.Phone = self.phone_edit.text()
            self.contact.Gender = self.gender_combo.currentText()
            self.contact.DoNotCall = self.do_not_call_checkbox.isChecked()
        # Reload data after editing the contact
        self.parent().load_data()

        super(EditContactDialog, self).accept()



class ChooseContactDialog(QDialog):
    def __init__(self, parent=None, contacts=None):
        super(ChooseContactDialog, self).__init__(parent)

        self.contacts = contacts

        layout = QFormLayout()

        self.contact_combo = QComboBox()
        layout.addRow("Choose Contact:", self.contact_combo)

        for contact in contacts:
            # self.contact_combo.addItem(f"{contact.First_name} {contact.Last_name}", contact)
            contact_text = f"{contact.First_name} {contact.Last_name} (ID: {contact.ID})"
            self.contact_combo.addItem(contact_text, contact.ID)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Choose Existing Contact")

    def get_selected_contact(self):
        index = self.contact_combo.currentIndex()
        if index != -1:
            return self.contacts[index]
        else:
            return None

