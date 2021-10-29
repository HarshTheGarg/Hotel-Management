"""
Initiating the connection with MySQL
"""

import mysql.connector as sql  # To connect to MySQL database
# pip install mysql-connector-python

import global_  # Importing the variables file


def estConnect() -> None:
    """
    Establish the connection with the MySQL server
    :rtype: None
    """

    # Getting the ip address of the server
    with open("info.txt") as infoFile:
        infoFile.readline()
        infoFile.readline()
        add = infoFile.readline()

    try:
        global_.conn = sql.connect(host=add, user=global_.username, password=global_.password)
        # Connect to the MySQL server

        # Check If Connection Was Successful
        if global_.conn.is_connected():

            global_.condition = 1
            # Update the Condition variable

            global_.updateStatus("Connection Successful")
            # Update the status bar

    # If there is Error in connecting to the database
    except sql.Error:

        global_.condition = 0
        # Update the Condition variable

        global_.updateStatus("Connection Failed. Try Again")
        # Update the status bar
