"""
Creating the database and required tables(if they don't exist) and using them
"""

# establishing connection
import MySql.mysqlConn

# Importing the variables file
import global_


# To create (and use) the required database
def createDbAndTables():

    # Establishes the connection with MySQL server and store the status and connection status
    # in the vars.status and vars.condition
    MySql.mysqlConn.estConnect()

    # If Connection was successful
    if global_.condition == 1:

        # Creating the MySQL cursor
        global_.cur = global_.conn.cursor()

        global_.updateStatus("Connecting to Database")

        # Creating database if it doesn't exist
        dbname = "HotelMan"

        # To see all available databases and compare if required database exists
        comm = "Show databases"
        global_.cur.execute(comm)

        # databases -> list of all the databases on the server
        databases = global_.cur.fetchall()

        try:

            # flag == True -> database exists
            # flag == False -> database doesn't exist
            flag = False

            for i in databases:
                # .casefold() for case insensitive checking
                # if database exists
                if i[0].casefold() == dbname.casefold():
                    flag = True
                    break

            # if flag == False, database doesn't exist
            if not flag:

                # Creating the database
                comm = "create database " + dbname
                global_.cur.execute(comm)

            # Using the database
            comm = "use " + dbname
            global_.cur.execute(comm)

        # If any error in creating/using the database
        except MySql.mysqlConn.sql.Error as e:

            # Printing the error
            print(e)
            global_.condition = 0

            global_.updateStatus("Error using the database")

            """# Exiting the Programme
            sys.exit()"""

        if global_.condition == 1:

            # Creating required tables
            global_.tbRooms = "rooms"
            global_.tbCustomers = "customers"
            global_.tbAllCustomers = "allCustomers"

            # Creating Rooms Table
            try:
                comm = "create table {} (" \
                       "RoomId varchar(2) Primary key," \
                       "AC varchar(1)," \
                       "Qty int(2), " \
                       "Rate int(5)," \
                       "Tax decimal(4,2)" \
                       ")"\
                    .format(global_.tbRooms)

                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass

            # Customers Table
            try:
                comm = "create table {} (" \
                       "CustomerId varchar(3) Primary key, " \
                       "CustomerName varchar(30)," \
                       "Aadhaar varchar(15), " \
                       "Mobile varchar(10)," \
                       "RoomId varchar(2)" \
                       ")"\
                    .format(global_.tbCustomers)

                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass

            # All Customers Table
            try:
                comm = "create table {} (" \
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
                       ")"\
                    .format(global_.tbAllCustomers)

                global_.cur.execute(comm)

            # If the table exists
            except MySql.mysqlConn.sql.Error:
                pass
