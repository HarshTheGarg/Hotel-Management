"""
Creating the database and required tables(if they don't exist) and using them
"""

import MySql.mysqlConn  # Establish the connection with MySQL

import global_  # Import the variables file


def createDbAndTables() -> None:
    """
    Create the required database and tables
    :rtype: None
    """
    MySql.mysqlConn.estConnect()
    # Establish the connection with MySQL server

    # If Connection was successful
    if global_.condition == 1:

        global_.cur = global_.conn.cursor()
        # Create the MySQL cursor

        global_.updateStatus("Connecting to Database")
        # Update the status bar

        # Create database if it doesn't exist
        dbname = "HotelMan"
        comm = "Show databases"
        global_.cur.execute(comm)
        databases: tuple = global_.cur.fetchall()
        # See all available databases and compare if required database exists

        try:

            # flag == True -> database exists
            # flag == False -> database doesn't exist
            flag = False

            for database in databases:
                # If database exists
                if database[0].casefold() == dbname.casefold():
                    flag = True
                    break

            # If database doesn't exist
            if not flag:
                comm = "create database " + dbname
                global_.cur.execute(comm)
                # Create the database

            comm = "use " + dbname
            global_.cur.execute(comm)
            # Use the database

        # If any error in creating/using the database
        except MySql.mysqlConn.sql.Error as e:
            print(e)

            global_.condition = 0

            global_.updateStatus("Error using the database")
            # Update the status bar

        # Create required tables
        if global_.condition == 1:

            global_.tbRooms = "rooms"
            global_.tbCustomers = "customers"
            global_.tbAllCustomers = "allCustomers"

            # Create Rooms Table
            try:
                comm = f"create table {global_.tbRooms} (" \
                       "RoomId varchar(2) Primary key," \
                       "AC varchar(1)," \
                       "Qty int(2), " \
                       "Rate int(5)," \
                       "Tax decimal(4,2)" \
                       ")"
                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass

            # Create Customers Table
            try:
                comm = f"create table {global_.tbCustomers} (" \
                       "CustomerId varchar(3) Primary key, " \
                       "CustomerName varchar(30)," \
                       "Aadhaar varchar(15), " \
                       "Mobile varchar(10)," \
                       "RoomId varchar(2)" \
                       ")"
                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass

            # Create All Customers Table
            try:
                comm = f"create table {global_.tbAllCustomers} (" \
                       "CustomerId varchar(3) Primary key, " \
                       "CustomerName varchar(30)," \
                       "Aadhaar varchar(15), " \
                       "Mobile varchar(10)," \
                       "RoomId varchar(2)," \
                       "checkInDate date," \
                       "checkOutDate date," \
                       "checkedIn char," \
                       "rate int(5)," \
                       "tax decimal(4, 2)" \
                       ")"
                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass
