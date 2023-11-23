import sqlite3
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QTableWidget,QMessageBox,QHeaderView,QLineEdit, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream, QItemSelection,Qt
import sqlite3
import resource_rc
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base
# from sqlalchemy.ext.declarative import declarative_base
import models.users


class UserAddDialog(QDialog):
    def __init__(self):
        super(UserAddDialog, self).__init__()

        self.login_label = QLabel("Login:")
        self.login_edit = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_edit)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.layout)
class User_Manager(QTableWidget):

    def __init__(self, ui, session):
        super(User_Manager, self).__init__()
        self.ui = ui
        self.database_session = session
        # self.setVerticalHeaderLabels(list("ABCD"))
        # self.ui.users_tableWidget.itemChanged.connect(self.save_changes)

    def add_new_row(self):
        # Create an instance of the dialog for adding a new user
        dialog = UserAddDialog()

        # Show the dialog and wait for the user's input
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # If the user clicked OK, retrieve the entered data
            login = dialog.login_edit.text()
            password = dialog.password_edit.text()

            # Generate a new user ID (you may adjust this logic as needed)
            new_user_id = self.generate_new_user_id()

            # Add the new row to the table
            row_position = self.ui.users_tableWidget.rowCount()
            self.ui.users_tableWidget.insertRow(row_position)

            # Set the new items for the added row
            self.ui.users_tableWidget.setItem(row_position, 0, QTableWidgetItem(str(new_user_id)))
            self.ui.users_tableWidget.setItem(row_position, 1, QTableWidgetItem(login))
            self.ui.users_tableWidget.setItem(row_position, 2, QTableWidgetItem(password))

            # Update the database with the new user
            new_user = models.users.Users(ID=new_user_id, Login=login, Password=password)
            self.database_session.add(new_user)
            self.database_session.commit()

    def generate_new_user_id(self):
        # You need to implement a logic to generate a new user ID
        # This could involve querying the database for the maximum ID and incrementing it
        # Here is a simple example assuming IDs are integers
        existing_user_ids = [int(self.ui.users_tableWidget.item(row, 0).text()) for row in
                             range(self.ui.users_tableWidget.rowCount())]
        if existing_user_ids:
            new_user_id = max(existing_user_ids) + 1
        else:
            new_user_id = 1

        return new_user_id

    def save_data(self):

        try:
            rows = self.ui.users_tableWidget.rowCount()
            if rows == 0:
                return

            # Assuming your User class has attributes ID, Login, Password
            for row in range(rows):
                user_id = int(self.ui.users_tableWidget.item(row, 0).text())
                login = self.ui.users_tableWidget.item(row, 1).text()
                password = self.ui.users_tableWidget.item(row, 2).text()

                # Update or insert the user data into the database
                user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()
                if user:
                    user.Login = login
                    user.Password = password
                else:
                    new_user = models.users.Users(ID=user_id, Login=login, Password=password)
                    self.database_session.add(new_user)

            self.database_session.commit()
            QMessageBox.information(self, "Save", "Data saved successfully.")
        except Exception as e:
            print(f"Error in save_data: {e}")

    def delete_data(self):
        selected_rows = self.ui.users_tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            return

        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete selected rows?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        for selected_row in selected_rows:
            user_id = int(self.ui.users_tableWidget.item(selected_row.row(), 0).text())
            user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()
            if user:
                self.database_session.delete(user)

        self.database_session.commit()
        self.load_data()  # Reload data after deletion
        QMessageBox.information(self, "Delete", "Data deleted successfully.")

    # def save_changes(self, item):
    #     print("Save Changes Called")
    #     # This slot will be automatically called when any item in the QTableWidget changes
    #     row = item.row()
    #     col = item.column()
    #
    #     user_id = int(self.ui.users_tableWidget.item(row, 0).text())
    #     login = self.ui.users_tableWidget.item(row, 1).text()
    #     password = self.ui.users_tableWidget.item(row, 2).text()
    #
    #     # Query the database to get the user with the given ID
    #     user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()
    #
    #     # Update the user's data
    #     if user:
    #         if col == 1:
    #             user.Login = login
    #         elif col == 2:
    #             user.Password = password
    #
    #         try:
    #             print(self.database_session.query(models.users.Users).filter_by(ID=user_id).first().statement)
    #
    #             # Commit the changes to the database
    #             self.database_session.commit()
    #         except Exception as e:
    #             print(f"Error committing changes: {e}")



    def set_column_width(self, width):
        # Set the width of each column to the specified value
        for column in range(self.ui.users_tableWidget.columnCount()):
            self.ui.users_tableWidget.setColumnWidth(column, width)

    def load_data(self):
        self.ui.users_tableWidget.setRowCount(0)
        users = self.database_session.query(models.users.Users).all()

        index = 0
        for user in users:
            self.ui.users_tableWidget.insertRow(index)

            # Set checkboxes in the vertical header
            item_id = QTableWidgetItem(str(user.ID))
            item_id.setFlags(item_id.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.users_tableWidget.setVerticalHeaderItem(index, item_id)

            # Set other items in the table
            self.ui.users_tableWidget.setItem(index, 0, QTableWidgetItem(str(user.ID)))
            self.ui.users_tableWidget.setItem(index, 1, QTableWidgetItem(str(user.Login)))
            self.ui.users_tableWidget.setItem(index, 2, QTableWidgetItem(str(user.Password)))

            # Add a checkbox to the vertical header
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.users_tableWidget.setVerticalHeaderItem(index, checkbox_item)

            index += 1

        # Set the vertical header to show checkboxes
        self.ui.users_tableWidget.verticalHeader().setSectionsClickable(True)
        self.ui.users_tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.ui.users_tableWidget.verticalHeader().setMinimumSectionSize(50)

