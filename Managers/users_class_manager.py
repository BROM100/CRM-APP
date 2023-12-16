from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget,QMessageBox, QLineEdit, QDialog, QVBoxLayout, QLabel, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel,QItemSelectionModel, QItemSelection
from PyQt6.QtGui import QIcon
# from sqlalchemy.ext.declarative import declarative_base
import models.users


class UserAddDialog(QDialog):
    def __init__(self):
        super(UserAddDialog, self).__init__()

        self.login_label = QLabel("Login:")
        self.login_edit = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()

        self.first_name_label = QLabel("First Name")
        self.first_name_edit = QLineEdit()

        self.last_name_label = QLabel("Last Name")
        self.last_name_edit = QLineEdit()

        self.email_label = QLabel("Email")
        self.email_edit = QLineEdit()

        self.type_label = QLabel("Type")
        self.type_edit = QLineEdit()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_edit)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_edit)
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_edit)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_edit)
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_edit)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)


        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.layout)

class User_Manager(QTableWidget):

    def __init__(self, users_table_widget, session):
        super(User_Manager, self).__init__()
        self.users_table_widget = users_table_widget
        self.database_session = session

        #Multiselection feature to QtableWidget
        self.users_table_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        #Column Sorting feature to QtableWidget
        self.users_table_widget.setSortingEnabled(True)
        self.users_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    def clear_selection(self):
        # Clear the selection in the QTableWidget
        self.users_table_widget.selectionModel().clearSelection()

    def count_standard_users(self):
        return len([1 for row in range(self.users_table_widget.rowCount())
                    if self.users_table_widget.item(row, 6).text().lower() == 'standard'])

    def count_admin_users(self):
        return len([1 for row in range(self.users_table_widget.rowCount())
                    if self.users_table_widget.item(row, 6).text().lower() == 'admin'])
    def add_new_row(self):
        print("Signal emitted: add_new_row")
        # Create an instance of the dialog for adding a new user
        dialog = UserAddDialog()

        # Show the dialog and wait for the user's input
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # If the user clicked OK, retrieve the entered data
            login = dialog.login_edit.text()
            password = dialog.password_edit.text()
            firstname = dialog.first_name_edit.text()
            lastname = dialog.last_name_edit.text()
            email = dialog.email_edit.text()
            type = dialog.type_edit.text()
            #Check if the login and password are not empty
            if login and password and len(password)>= 8:

                # Generate a new user ID
                new_user_id = self.generate_new_user_id()

                # Add the new row to the table
                row_position = self.users_table_widget.rowCount()
                self.users_table_widget.insertRow(row_position)

                # Set the new items for the added row
                self.users_table_widget.setItem(row_position, 0, QTableWidgetItem(str(new_user_id)))
                self.users_table_widget.setItem(row_position, 1, QTableWidgetItem(login))
                self.users_table_widget.setItem(row_position, 2, QTableWidgetItem(password))
                self.users_table_widget.setItem(row_position, 3, QTableWidgetItem(firstname))
                self.users_table_widget.setItem(row_position, 4, QTableWidgetItem(lastname))
                self.users_table_widget.setItem(row_position, 5, QTableWidgetItem(email))
                self.users_table_widget.setItem(row_position, 6, QTableWidgetItem(type))
                # Update the database with the new user
                new_user = models.users.Users(ID=new_user_id, Login=login, Password=password, First_Name=firstname, Last_Name=lastname, Email=email, Type=type)
                self.database_session.add(new_user)
                self.database_session.commit()
            else:
                QMessageBox.information(self, "Error", "Login and password (8 characters long) cannot be empty.")
                self.add_new_row()
    def generate_new_user_id(self):

        existing_user_ids = [int(self.users_table_widget.item(row, 0).text()) for row in
                             range(self.users_table_widget.rowCount())]
        if existing_user_ids:
            new_user_id = max(existing_user_ids) + 1
        else:
            new_user_id = 1

        return new_user_id

    def save_data(self):

        try:
            rows = self.users_table_widget.rowCount()
            if rows == 0:
                return


            for row in range(rows):
                user_id = int(self.users_table_widget.item(row, 0).text())
                login = self.users_table_widget.item(row, 1).text()
                password = self.users_table_widget.item(row, 2).text()
                first_name = self.users_table_widget.item(row, 3).text()
                last_name = self.users_table_widget.item(row, 4).text()
                email = self.users_table_widget.item(row, 5).text()
                type = self.users_table_widget.item(row, 6).text()
                # Update or insert the user data into the database
                user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()
                if user:
                    user.Login = login
                    user.Password = password
                    user.First_Name = first_name
                    user.Last_Name = last_name
                    user.Email = email
                    user.Type = type
                else:
                    new_user = models.users.Users(ID=user_id, Login=login, Password=password, First_Name=first_name, Last_Name=last_name, Email=email,Type=type)
                    self.database_session.add(new_user)

            self.database_session.commit()
            QMessageBox.information(self, "Save", "Data saved successfully.")
        except Exception as e:
            print(f"Error in save_data: {e}")

    def delete_data(self):
        selected_rows = self.users_table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete selected rows?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        for selected_row in selected_rows:
            user_id = int(self.users_table_widget.item(selected_row.row(), 0).text())
            user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()
            if user:
                self.database_session.delete(user)

        self.database_session.commit()
        self.load_data()  # Reload data after deletion
        QMessageBox.information(self, "Delete", "Data deleted successfully.")


    def set_row_height(self, h):
        for row in range(self.users_table_widget.rowCount()):
            self.users_table_widget.setRowHeight(row, h)
    def set_column_width(self, width):

        self.users_table_widget.setColumnWidth(0, 35)
        for c in range(1,self.users_table_widget.columnCount()):
            self.users_table_widget.setColumnWidth(c, width)

    def load_data(self):
        self.users_table_widget.setRowCount(0)
        users = self.database_session.query(models.users.Users).all()

        index = 0
        for user in users:
            self.users_table_widget.insertRow(index)

            for col, value in enumerate([str(user.ID), str(user.Login), str(user.Password), str(user.First_Name),
                                         str(user.Last_Name), str(user.Email), str(user.Type)]):
                item = QTableWidgetItem(value)
                self.users_table_widget.setItem(index, col, item)
            index += 1

        # Set the vertical header to show checkboxes
        self.users_table_widget.verticalHeader().setSectionsClickable(True)
        self.users_table_widget.verticalHeader().setFixedWidth(30)
        self.users_table_widget.verticalHeader().setDefaultSectionSize(50)
        self.users_table_widget.verticalHeader().setMinimumSectionSize(50)


