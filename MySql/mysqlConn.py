"""
Initiating the connection with MySQL
"""

# To connect to MySQL database
# pip install mysql-connector-python
import mysql.connector as sql

# Importing the variables file
import global_


# To establish the connection with MySQL server on 100.70.197.206 (My IP address) and store the status and
# connection status in the vars.status and vars.condition
def estConnect():
    try:

        # Connecting to the MySQL server
        global_.conn = sql.connect(host="100.70.197.206", user=global_.username, password=global_.password)

        # Checking If Connection Was Successful
        if global_.conn.is_connected():

            # Update the Condition variable
            global_.condition = 1
            global_.updateStatus("Connection Successful")

    # To be run if there is Error in connecting to the database
    except sql.Error as e:
        # Print the Error
        print(e)

        # Update the Condition variable
        global_.condition = 0

        global_.updateStatus("Connection Failed. Try Again")
