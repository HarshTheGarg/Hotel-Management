"""
File to store all the queries to be run
"""

import global_
# File to use global variables

import mysql.connector as sql
# To handle sql errors

import datetime
# To calculate price


def eventErrorHandler(event):
    """
    To remove error in the IDE for not using argument passed by the bind function
    :param event: event passed by bind function
    :rtype: None
    """
    str(event) * 2


def addCustomer(name: str, aadhaar: str, mobile: str, roomId: str, inDate: str) -> tuple:
    """
    Add a customer to customers table
    :param name: Customer's name
    :param aadhaar: Customer's aadhaar number
    :param mobile: Customer's mobile number
    :param roomId: Customer's Room Id
    :param inDate: Check-in date of customer for allCustomers table
    :return: (0, error message) or (1, customerId)
    :rtype: tuple
    """
    try:
        # Checking if room is vacant
        comm = "select qty, tax from {} where roomId='{}'".format(global_.tbRooms, roomId)
        global_.cur.execute(comm)
        res = global_.cur.fetchone()

        qtyOfRooms: int = res[0]

        roomTax: float = res[1]

        # If rooms is unavailable or room doesn't exist
        if qtyOfRooms == 0 or qtyOfRooms is None:

            return 0, "Room not Available"
            # Error, Message to be displayed

        # If room is available
        else:

            # Fetching all customerIds to create next id
            comm = "select * from " + global_.tbAllCustomers
            global_.cur.execute(comm)
            res = global_.cur.fetchall()  # Tuple

            # Creating next Customer Id
            # If no customers exist, tuple will be empty
            if not res:
                customerIdNumber = 1
            else:

                # Last id, integer part
                customerIdNumber = int(res[-1][0][1:]) + 1

            # Making sure customerId looks good
            if customerIdNumber < 10:
                customerIdNumber = "0" + str(customerIdNumber)

            # Make customer id of the format C01, C02...
            customerId = "C" + str(customerIdNumber)

            # Add Customer to the customers table
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
            addAllCustomers(customerId, name, aadhaar, mobile, roomId, inDate, roomTax)

            # (No Error, CustomerId to be displayed)
            return 1, customerId

    # If some error occurs
    except sql.Error as e:
        eventErrorHandler(e)
        return 0, "Some Error Occurred"


def searchCustomer(customerId: str, caller: str = "notFind") -> int:
    """
    Check if customer exists using customerId
    :param customerId: Id of the customer to be found
    :param caller: To check if function is called by the find method,
    since find in admin mode checks in allCustomerTable
    :return: 1 -> customer found, 0 -> customer not found
    :rtype: int
    """
    # Fetching all the customerIds to compare from respective tables
    if global_.accessLevel == "Admin" and caller == "find":
        comm = "select CustomerId from " + global_.tbAllCustomers
    else:
        comm = "select CustomerId from " + global_.tbCustomers

    global_.cur.execute(comm)
    customerRes = global_.cur.fetchall()

    # Checking all customerIds in a loop
    for resCustomerId in customerRes:

        if resCustomerId[0] == customerId:

            return 1
            # customerId found

    return 0
    # customerId Not Found


def selectCustomer(customerId: str, caller: str = "notFind") -> tuple:
    """
    Return the customer's details
    :param customerId: Id of the customer to be found
    :param caller: To check if function is called by the find method,
    since find in admin mode checks in allCustomerTable
    :rtype: tuple
    :return: tuple of customer's name, aadhaar, and mobile number
    """
    # Select all the details of the customer using customerId
    if global_.accessLevel == "Admin" and caller == "find":
        # Finding the data in admin mode

        comm = f"select * from {global_.tbAllCustomers} where customerId='{customerId}'"
    else:
        comm = f"select * from {global_.tbCustomers} where customerId='{customerId}'"

    global_.cur.execute(comm)
    customer = global_.cur.fetchone()  # customer -> tuple -> (customerId, name, aadhaar, mobile)

    name = customer[1]
    aadhaar = customer[2]
    mobile = customer[3]
    return name, aadhaar, mobile


def updateCustomer(customerId: str, name: str, aadhaar: str, mobile: str) -> None:
    """
    Update customer details in customers table
    :param customerId: Id of customer whose details have to be updated
    :param name: New customer name
    :param aadhaar: New Aadhaar number
    :param mobile: New Mobile number
    :rtype: None
    """
    details = {"CustomerName": name, "Aadhaar": aadhaar, "Mobile": mobile}
    # Dictionary of all the details

    # Updating all details using a loop
    for detail in details:
        comm = f"update {global_.tbCustomers} set {detail}='{details[detail]}'" \
               f" where customerId='{customerId}'"
        global_.cur.execute(comm)

        global_.conn.commit()
        # Committing the changes made

    updateAllCustomers(customerId, name, aadhaar, mobile)
    # To update in allCustomers Table also


def removeCustomer(customerId: str, outDate: datetime.date) -> tuple:
    """
    Remove customer from customers table
    :param customerId: Id of the customer to be removed
    :param outDate: To set the check-out date in allCustomers table
    :return: (roomId, checkInDate, checkOutDate, roomRate, price, roomTax)
    :rtype: tuple
    """
    # Get customer's roomId to add qty to rooms table
    comm = f"select RoomId from {global_.tbCustomers} where CustomerId='{customerId}'"
    global_.cur.execute(comm)

    customerRoom = global_.cur.fetchone()[0]

    comm = f"delete from {global_.tbCustomers} where CustomerId='{customerId}'"
    global_.cur.execute(comm)
    # Remove the customer from the customers table

    global_.conn.commit()
    # Committing the changes made

    comm = "update {} set Qty=Qty+1 where roomId='{}'".format(global_.tbRooms, customerRoom)
    global_.cur.execute(comm)
    # Updating Quantity of Room

    global_.conn.commit()
    # Committing the changes made

    checkOutAllCustomersTable(customerId, outDate)
    # Check out the customer from allCustomers table

    comm = "select * from {} where customerId='{}'".format(global_.tbAllCustomers, customerId)
    global_.cur.execute(comm)
    res = global_.cur.fetchone()
    # Getting the customer's details for the invoice

    price_ = price(customerId, outDate)
    # Generating the price of the stay without the tax

    return res[4], res[5], res[6], res[8], price_, res[9]
    # (roomId, checkInDate, checkOutDate, roomRate, price, roomTax)
    # Returning info to generate invoice


def showCustomers() -> tuple:
    """
    Retrieve data of all the customers
    :return: Customer's data
    :rtype: tuple
    """
    res = None
    # If there is no customer

    if global_.accessLevel == "User":
        # If logged in as user, retrieve data only of current customers
        # Selecting all the the customers
        comm = "select * from " + global_.tbCustomers
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    elif global_.accessLevel == "Admin":
        # Else, in admin mode, retrieve Data of all customers
        # Selecting all the the customers
        comm = "select * from " + global_.tbAllCustomers
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    # Returning tuple of customer's information
    return res


def addAllCustomers(
        customerId: str, name: str, aadhaar: str, mobile: str, roomId: str, inDate: str, tax: float
) -> None:
    """
    Add the customer's details in the allCustomers table
    :param customerId: Customer's Id
    :param name: Customer's Name
    :param aadhaar: Customer's Aadhaar Number
    :param mobile: Customer's Mobile Number
    :param roomId: Customer's Room's Id
    :param inDate: Check-in date of customer
    :param tax: Room Tax
    :rtype: None
    """
    # Get rate of the room
    comm = "select rate from {} where roomId='{}'".format(global_.tbRooms, roomId)
    global_.cur.execute(comm)
    rate = global_.cur.fetchone()[0]

    # To add customer to allCustomer table
    comm = "insert into {} values(" \
           "'{}', '{}', '{}', '{}', '{}', '{}', NULL, 'y', {}, {}" \
           ")" \
        .format(global_.tbAllCustomers, customerId, name, aadhaar, mobile, roomId, inDate, int(rate), float(tax))

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
    days_ = outDate - inDate
    return rate*days_


# Function to add a room to database
def addRoom(roomId, ac, qty, rate, tax):
    # Converting Yes/No to a single character
    if ac.casefold() == "Yes".casefold():
        ac = "y"
    elif ac.casefold() == "No".casefold():
        ac = "n"

    # Function to add the room to database
    def sendComm():
        comm1 = "insert into {tableName} values(" \
                "'{}', '{}', {}, {}, {}" \
                ")".format(roomId, ac, qty, rate, tax, tableName=global_.tbRooms)
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
    tax = res[4]
    return qty, rate, tax


# Function to update qty and rate of room
def updateRoom(roomId, qty, rate, tax):
    # Updating the room quantity
    comm = "update {} set qty={} where roomId='{}'".format(global_.tbRooms, qty, roomId)
    global_.cur.execute(comm)

    # Updating the room rate
    comm = "update {} set rate={} where roomId='{}'".format(global_.tbRooms, rate, roomId)
    global_.cur.execute(comm)

    # Updating the room tax
    comm = "update {} set tax={} where roomId='{}'".format(global_.tbRooms, tax, roomId)
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
