import sqlite3
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QTableWidget
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream
import sqlite3
import resource_rc
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base
# from sqlalchemy.ext.declarative import declarative_base
import models.users

class User_Manager(QTableWidget):

    def __init__(self, ui, session):
        # super(UsersTableWidget, self).__init__()
        self.ui = ui
        self.database_session = session
        # self.setVerticalHeaderLabels(list("ABCD"))
        self.ui.users_tableWidget.itemChanged.connect(self.save_changes)

    def save_changes(self, item):
        print("Save Changes Called")
        # This slot will be automatically called when any item in the QTableWidget changes
        row = item.row()
        col = item.column()

        user_id = int(self.ui.users_tableWidget.item(row, 0).text())
        login = self.ui.users_tableWidget.item(row, 1).text()
        password = self.ui.users_tableWidget.item(row, 2).text()

        # Query the database to get the user with the given ID
        user = self.database_session.query(models.users.Users).filter_by(ID=user_id).first()

        # Update the user's data
        if user:
            if col == 1:
                user.Login = login
            elif col == 2:
                user.Password = password

            try:
                print(self.database_session.query(models.users.Users).filter_by(ID=user_id).first().statement)

                # Commit the changes to the database
                self.database_session.commit()
            except Exception as e:
                print(f"Error committing changes: {e}")



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
            self.ui.users_tableWidget.setItem(index, 0, QTableWidgetItem(str(user.ID)))
            self.ui.users_tableWidget.setItem(index, 1, QTableWidgetItem(str(user.Login)))
            self.ui.users_tableWidget.setItem(index, 2, QTableWidgetItem(str(user.Password)))
            index = index + 1

