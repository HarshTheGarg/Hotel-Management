"""
File to store all the queries to be run
"""

# File to use global variables
import global_

# To handle sql errors
import mysql.connector as sql


# Function to add a customer to database
def addCustomer(name, aadhaar, mobile, roomId, inDate):
    try:
        # Checking if room is vacant
        comm = "select qty from {} where roomId='{}'".format(global_.tbRooms, roomId)
        global_.cur.execute(comm)

        # qty -> Number of rooms, tuple
        qty = global_.cur.fetchone()

        # If qty of rooms is zero
        if qty == (0,) or qty is None:

            # Error, Message to be displayed
            return 0, "Room not Available"

        # If qty is not zero
        else:

            # Fetching all the customerId
            comm = "select * from " + global_.tbAllCustomers
            global_.cur.execute(comm)
            res = global_.cur.fetchall()  # Tuple

            # Creating next Customer Id
            # If no customers exist, tuple will be empty
            if not res:
                customerIdNumber = 1
            else:

                # Last id
                customerIdNumber = int(res[-1][0][1:]) + 1

            # Making sure customerId looks good
            if customerIdNumber < 10:
                customerIdNumber = "0" + str(customerIdNumber)

            # To make customer id of the format C01, C02...
            customerId = "C" + str(customerIdNumber)

            # To add Customer to the customers table
            comm = "insert into {} values(" \
                   "'{}', '{}', '{}', '{}', '{}', '{}'" \
                   ")".format(global_.tbCustomers, customerId, name, aadhaar, mobile, roomId, inDate)
            global_.cur.execute(comm)

            # Committing the changes made
            global_.conn.commit()

            # To reduce the qty of room from rooms table
            comm = "update {} set qty=qty-1 where roomId='{}'".format(global_.tbRooms, roomId)
            global_.cur.execute(comm)

            # Committing the changes made
            global_.conn.commit()

            # Add the details to allCustomers Table
            addAllCustomers(customerId, name, aadhaar, mobile, roomId, inDate)

            # No Error, CustomerId to be displayed
            return 1, customerId

    # If some error occurs
    except sql.Error as e:
        print(e)
        return 0, "Some Error Occurred"


# To check if customer exists using customerId
def searchCustomer(customerId, caller="notFind"):
    # Fetching all the customerIds to compare
    if global_.accessLevel == "Admin" and caller == "find":
        comm = "select CustomerId from " + global_.tbAllCustomers
    else:
        comm = "select CustomerId from " + global_.tbCustomers

    global_.cur.execute(comm)
    customerRes = global_.cur.fetchall()

    # Checking all customerIds in a loop
    for i in customerRes:  # i -> tuple of tuple

        # Strip to remove the leading and trailing "(", ")", ","
        if str(i).strip("'(),") == customerId:
            # customerId found
            return 1

    # customerId Not Found
    return 0


# To display details about a specific customer
def selectCustomer(customerId, caller="notFind"):
    # Select all the details of the customer using customerId
    if global_.accessLevel == "Admin" and caller == "find":
        comm = "select * from {} where customerId='{}'".format(global_.tbAllCustomers, customerId)
        print("Using Admin")
    else:
        comm = "select * from {} where customerId='{}'".format(global_.tbCustomers, customerId)

    global_.cur.execute(comm)
    customer = global_.cur.fetchone()  # customer -> tuple -> (customerId, name, aadhaar, mobile)

    name = customer[1]
    aadhaar = customer[2]
    mobile = customer[3]
    return name, aadhaar, mobile


# To update customer details
def updateCustomer(customerId, name, aadhaar, mobile):
    # Dictionary of all the new details
    details = {"CustomerName": name, "Aadhaar": aadhaar, "Mobile": mobile}

    # Updating all details using a loop
    for i in details:
        comm = "update {} set {}='{}' where customerId='{}'".format(global_.tbCustomers, i, details[i], customerId)
        global_.cur.execute(comm)

        global_.conn.commit()

        # To update in allCustomers Table also
        updateAllCustomers(customerId, name, aadhaar, mobile)


# To remove customer
def removeCustomer(customerId, outDate):
    # Get customer's roomId to add qty to rooms table
    comm = "select RoomId from {} where CustomerId='{}'".format(global_.tbCustomers, customerId)
    global_.cur.execute(comm)

    # To save the RoomId in customerRoom
    # Strip to remove trailing and leading "(", ")", ","
    customerRoom = str(global_.cur.fetchone()).strip("(),'")

    # Remove the customer from the database
    comm = "delete from {} where CustomerId='{}'".format(global_.tbCustomers, customerId)
    global_.cur.execute(comm)

    # Committing the changes made
    global_.conn.commit()

    # Updating Quantity of Room
    comm = "update {} set Qty=Qty+1 where roomId='{}'".format(global_.tbRooms, customerRoom)
    global_.cur.execute(comm)

    # Committing the changes made
    global_.conn.commit()

    checkOutAllCustomersTable(customerId, outDate)

    comm = "select * from {} where customerId='{}'".format(global_.tbAllCustomers, customerId)
    global_.cur.execute(comm)
    res = global_.cur.fetchone()

    price_ = price(customerId, outDate)

    # Returning info to generate invoice
    return res[4], res[5], res[6], res[8], price_


# To show all the checked in customers
def showCustomers():

    res = None

    if global_.accessLevel == "User":

        # Selecting all the the customers
        comm = "select * from " + global_.tbCustomers
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    elif global_.accessLevel == "Admin":

        # Selecting all the the customers
        comm = "select * from " + global_.tbAllCustomers
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    # Returning tuple of customer's information
    return res


# To add customer to allCustomers table
def addAllCustomers(customerId, name, aadhaar, mobile, roomId, inDate):

    # Get rate of the room
    comm = "select rate from {} where roomId='{}'".format(global_.tbRooms, roomId)
    global_.cur.execute(comm)
    rate = global_.cur.fetchone()[0]

    # To add customer to allCustomer table
    comm = "insert into {} values(" \
           "'{}', '{}', '{}', '{}', '{}', '{}', NULL, 'y', '{}'" \
           ")" \
        .format(global_.tbAllCustomers, customerId, name, aadhaar, mobile, roomId, inDate, rate)

    global_.cur.execute(comm)

    # Committing the changes made
    global_.conn.commit()


# To update status in allCustomers Table
def updateAllCustomers(customerId, name, aadhaar, mobile):
    # Dictionary of all the new details
    details = {"CustomerName": name, "Aadhaar": aadhaar, "Mobile": mobile}

    # Updating all details using a loop
    for i in details:
        comm = "update {} set {}='{}' where customerId='{}'".format(global_.tbAllCustomers, i, details[i], customerId)
        global_.cur.execute(comm)

        # Committing the changes made
        global_.conn.commit()


# To check out customer from allCustomers Table
def checkOutAllCustomersTable(customerId, outDate):
    # Updating the checkOut date
    comm = "update {} set checkOutDate='{}' where customerId='{}'" \
        .format(global_.tbAllCustomers, outDate, customerId)

    global_.cur.execute(comm)

    # Updating the checkedIn value
    comm = "update {} set checkedIn='n' where customerId='{}'" \
        .format(global_.tbAllCustomers, customerId)

    global_.cur.execute(comm)

    # Committing the changes made
    global_.conn.commit()


# Calculate the price to be paid
def price(customerId, outDate):

    # Getting the rate of the room
    comm = "select rate from {} where customerId='{}'".format(global_.tbAllCustomers, customerId)
    global_.cur.execute(comm)
    rate = global_.cur.fetchone()[0]

    # Getting the checkInDate
    comm = "select checkInDate from {} where customerId='{}'".format(global_.tbAllCustomers, customerId)
    global_.cur.execute(comm)
    inDate = global_.cur.fetchone()[0]

    # No of days
    days = (outDate - inDate).days
    return rate*days


# Function to add a room to database
def addRoom(roomId, ac, qty, rate):
    # Converting Yes/No to a single character
    if ac.casefold() == "Yes".casefold():
        ac = "y"
    elif ac.casefold() == "No".casefold():
        ac = "n"

    # Function to add the room to database
    def sendComm():
        comm1 = "insert into {tableName} values(" \
                "'{}', '{}', '{}', '{}'" \
                ")".format(roomId, ac, qty, rate, tableName=global_.tbRooms)
        global_.cur.execute(comm1)

        # Committing the changes made
        global_.conn.commit()

    # Checking if room already exists
    comm = "select * from " + global_.tbRooms
    global_.cur.execute(comm)
    res = global_.cur.fetchall()

    # If no room exists, res will be empty
    if len(res) == 0:

        # Creating the room
        sendComm()

        # No error
        return 1

    else:

        # Checking if required room exists
        for i in res:
            if i[0] == roomId:
                # Room Exists
                return 0

        # Creating the room
        sendComm()

        # No error
        return 1


# To check if room exists using roomId
def searchRoom(roomId):
    # selecting the roomId
    comm = "select RoomId from " + global_.tbRooms
    global_.cur.execute(comm)

    # Tuple of Tuple of RoomId
    res = global_.cur.fetchall()

    for i in res:
        if str(i).strip("'(),") == roomId:
            # Room exists
            return 1

    # Room doesn't exist
    return 0


# Function to display a specific room
def selectRoom(roomId):
    # Selecting all the info of the room
    comm = "select * from {} where roomId='{}'".format(global_.tbRooms, roomId)
    global_.cur.execute(comm)
    res = global_.cur.fetchone()  # Tuple

    qty = res[2]
    rate = res[3]
    return qty, rate


# Function to update qty and rate of room
def updateRoom(roomId, qty, rate):
    # Updating the room quantity
    comm = "update {} set qty={} where roomId='{}'".format(global_.tbRooms, qty, roomId)
    global_.cur.execute(comm)

    # Updating the room rate
    comm = "update {} set rate={} where roomId='{}'".format(global_.tbRooms, rate, roomId)
    global_.cur.execute(comm)

    # Committing the changes made
    global_.conn.commit()


# Function to display all the rooms
def showRooms():
    # Selecting all the rooms
    comm = "select * from " + global_.tbRooms
    global_.cur.execute(comm)
    res = global_.cur.fetchall()  # Tuple
    return res


# To form CSV
def retrieveAllData():
    comm = f"select * from {global_.tbAllCustomers}"
    global_.cur.execute(comm)

    allCustomers = global_.cur.fetchall()

    return allCustomers


# To close the cursor and connection before sign out
def endConn():
    global_.cur.close()
    global_.conn.close()
