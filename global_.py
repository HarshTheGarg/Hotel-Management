"""
File to store global variables used in all the files
"""

import tkinter as tk
import mysql.connector as sql
# To specify datatype


accessLevel: str
# User Access

username: str
# Sign In Username

password: str
# Sign In Password

statusBar: tk.Label
# Status Bar

conn: sql.connection.MySQLConnection
# MySQL Connection

cur: sql.connection.MySQLCursor
# MySQL Cursor

tbRooms: str
# Rooms Table name

tbCustomers: str
# Customers Table name

tbAllCustomers: str
# All Customers Table name

condition: int
# Condition Checker
# 1: Ok, 0: Not Ok


def updateStatus(text: str) -> None:
    """
    Update the status bar
    :param text: Text to be displayed on the status bar
    """
    statusBar.configure(text=text)
