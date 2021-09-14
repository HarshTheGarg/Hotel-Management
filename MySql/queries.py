"""
File to store all the queries to be run
"""

import global_  # File to use global variables

import mysql.connector as sql  # To handle sql errors

import datetime  # To calculate price


def eventErrorHandler(event):
    """
    Remove error in the IDE for not using argument passed by the bind function
    :param event: event passed by bind function
    :rtype: None
    """
    str(event) * 2


def addCustomer(name: str, aadhaar: str, mobile: str, roomId: str, inDate: str) -> tuple[int, str]:
    """
    Add a customer to customers table
    :param name: Customer's name
    :param aadhaar: Customer's aadhaar number
    :param mobile: Customer's mobile number
    :param roomId: Customer's Room Id
    :param inDate: Check-in date of customer for allCustomers table
    :return: (0, error message) or (1, customerId)
    :rtype: tuple[int, str]
    """
    try:
        # Check if room is vacant
        comm = f"select qty, tax " \
               f"from {global_.tbRooms}" \
               f" where roomId='{roomId}'"
        global_.cur.execute(comm)
        res: tuple = global_.cur.fetchone()

        if res is None:
            # If room doesn't exist

            return 0, "Room not Available"
            # Error, Message to be displayed

        elif res[0] == 0:
            # res[0] : Quantity of room
            # If rooms is unavailable

            return 0, "Room not Vacant"
            # Error, Message to be displayed

        else:
            # If room is available

            roomTax: float = res[1]

            # Fetch all customerIds to create next id
            comm = f"select * from {global_.tbAllCustomers}"
            global_.cur.execute(comm)
            res: tuple = global_.cur.fetchall()

            # Create next Customer Id
            if not res:
                # If no customers exist, tuple will be empty
                customerIdNumber = 1

            else:
                # Last id, integer part
                customerIdNumber = int(res[-1][0][1:]) + 1

            # Make sure customerId looks good
            if customerIdNumber < 10:
                customerIdNumber = "0" + str(customerIdNumber)

            customerId = "C" + str(customerIdNumber)
            # Make customer id of the format C01, C02...

            comm = f"insert into {global_.tbCustomers} values(" \
                   f"'{customerId}', " \
                   f"'{name}', " \
                   f"'{aadhaar}', " \
                   f"'{mobile}', " \
                   f"'{roomId}'" \
                   ")"
            global_.cur.execute(comm)
            # Add Customer to the customers table

            global_.conn.commit()
            # Commit the changes made

            comm = f"update {global_.tbRooms} " \
                   f"set qty=qty-1 " \
                   f"where roomId='{roomId}'"
            global_.cur.execute(comm)
            # Reduce the qty of room from rooms table

            global_.conn.commit()
            # Commit the changes made

            addAllCustomers(customerId, name, aadhaar, mobile, roomId, inDate, roomTax)
            # Add the details to allCustomers Table

            return 1, customerId
            # (No Error, CustomerId to be displayed)

    except sql.Error as e:
        # If some error occurs

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
    # Fetch all the customerIds to compare from respective tables
    if global_.accessLevel == "Admin" and caller == "find":
        # If user in in admin mode and finding the customer(Not updating or checking out in either mode)
        comm = f"select CustomerId from {global_.tbAllCustomers}"
    else:
        comm = f"select CustomerId from {global_.tbCustomers}"

    global_.cur.execute(comm)
    customerRes: tuple[str] = global_.cur.fetchall()

    for resCustomerId in customerRes:
        # Check all customerIds in a loop

        if resCustomerId[0] == customerId:

            return 1
            # customerId found

    return 0
    # customerId Not Found


def selectCustomer(customerId: str, caller: str = "notFind") -> tuple[str, str, str]:
    """
    Return the customer's details
    :param customerId: Id of the customer to be found
    :param caller: To check if function is called by the find method,
    since find in admin mode checks in allCustomerTable
    :rtype: tuple[str, str, str]
    :return: tuple of customer's name, aadhaar, and mobile number
    """
    # Select all the details of the customer using customerId
    if global_.accessLevel == "Admin" and caller == "find":
        # Find the data in admin mode (Not updating or checking out in either mode)
        comm = f"select * from {global_.tbAllCustomers} " \
               f"where customerId='{customerId}'"
    else:
        comm = f"select * from {global_.tbCustomers} " \
               f"where customerId='{customerId}'"

    global_.cur.execute(comm)
    customer: tuple = global_.cur.fetchone()

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
    details = {
        "CustomerName": name,
        "Aadhaar": aadhaar,
        "Mobile": mobile
    }
    # Dictionary of all the details

    # Update all details using a loop
    for detail in details:
        comm = f"update {global_.tbCustomers} " \
               f"set {detail}='{details[detail]}' " \
               f"where customerId='{customerId}'"
        global_.cur.execute(comm)

        global_.conn.commit()
        # Commit the changes made

    updateAllCustomers(customerId, name, aadhaar, mobile)
    # Update in allCustomers Table also


def removeCustomer(
        customerId: str, outDate: datetime.date
) -> tuple[str, datetime.date, datetime.date, int, int, float]:
    """
    Remove customer from customers table
    :param customerId: Id of the customer to be removed
    :param outDate: To set the check-out date in allCustomers table
    :return: (roomId, checkInDate, checkOutDate, roomRate, price, roomTax)
    :rtype: tuple[str, datetime.date, datetime.date, int, int, float]
    """
    comm = f"select RoomId from {global_.tbCustomers} " \
           f"where CustomerId='{customerId}'"
    global_.cur.execute(comm)
    customerRoom = global_.cur.fetchone()[0]
    # Get customer's roomId to add qty to rooms table

    comm = f"update {global_.tbRooms} " \
           f"set Qty=Qty+1 " \
           f"where roomId='{customerRoom}'"
    global_.cur.execute(comm)
    # Update Quantity of Room
    global_.conn.commit()
    # Commit the changes made

    comm = f"delete from {global_.tbCustomers} " \
           f"where CustomerId='{customerId}'"
    global_.cur.execute(comm)
    # Remove the customer from the customers table
    global_.conn.commit()
    # Commit the changes made

    checkOutAllCustomersTable(customerId, str(outDate))
    # Check out the customer from allCustomers table

    comm = f"select * from {global_.tbAllCustomers} " \
           f"where customerId='{customerId}'"
    global_.cur.execute(comm)
    res: tuple = global_.cur.fetchone()
    # Get the customer's details for the invoice

    price = calcPrice(customerId, outDate)
    # Generate the price of the stay without the tax

    return res[4], res[5], res[6], res[8], price, res[9]
    # (roomId, checkInDate, checkOutDate, roomRate, price, roomTax)
    # Return info to generate invoice


def showCustomers() -> tuple[tuple]:
    """
    Retrieve data of all the customers
    :return: Customer's data
    :rtype: tuple
    """
    res: tuple = ()

    if global_.accessLevel == "User":
        # If logged in as user, retrieve data only of current customers
        # Select all the the checked-in customers
        comm = f"select * from {global_.tbCustomers}"
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    elif global_.accessLevel == "Admin":
        # Else, in admin mode, retrieve Data of all customers
        # Select all the the customers
        comm = f"select * from {global_.tbAllCustomers}"
        global_.cur.execute(comm)
        res = global_.cur.fetchall()

    return res


def addAllCustomers(
        customerId: str, name: str, aadhaar: str, mobile: str,
        roomId: str, inDate: str, tax: float) -> None:
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
    comm = f"select rate from {global_.tbRooms} " \
           f"where roomId='{roomId}'"
    global_.cur.execute(comm)
    rate = global_.cur.fetchone()[0]
    # Get rate of the room

    comm = f"insert into {global_.tbAllCustomers} values(" \
           f"'{customerId}', " \
           f"'{name}', " \
           f"'{aadhaar}', " \
           f"'{mobile}'," \
           f" '{roomId}', " \
           f"'{inDate}'," \
           f" NULL, " \
           f"'y', " \
           f"{int(rate)}, " \
           f"{float(tax)}" \
           ")"
    global_.cur.execute(comm)
    # Add customer to allCustomer table
    global_.conn.commit()
    # Commit the changes made


def updateAllCustomers(customerId: str, name: str, aadhaar: str, mobile: str) -> None:
    """
    Update the customer's details in the allCustomers table
    :param customerId: Id of the customer whose details are to be updated
    :param name: Customer's new Name
    :param aadhaar: Customer's new Aadhaar Number
    :param mobile: Customer's new Mobile Number
    :rtype: None
    """
    details = {
        "CustomerName": name,
        "Aadhaar": aadhaar,
        "Mobile": mobile
    }
    # Dictionary of all the new details

    # Update all details using a loop
    for detail in details:
        comm = f"update {global_.tbAllCustomers}" \
               f" set {detail}='{details[detail]}' " \
               f"where customerId='{customerId}'"
        global_.cur.execute(comm)
        global_.conn.commit()
        # Commit the changes made


def checkOutAllCustomersTable(customerId: str, outDate: str) -> None:
    """
    Check-Out the customer from the allCustomers table
    :param customerId: Id of customer to be checked-out
    :param outDate: Date when customer checks out
    :rtype: None
    """
    comm = f"update {global_.tbAllCustomers} " \
           f"set checkOutDate='{outDate}' " \
           f"where customerId='{customerId}'"
    global_.cur.execute(comm)
    # Update the checkOut date

    comm = f"update {global_.tbAllCustomers} " \
           f"set checkedIn='n' " \
           f"where customerId='{customerId}'"
    global_.cur.execute(comm)
    # Update the checkedIn value
    global_.conn.commit()
    # Commit the changes made


def calcPrice(customerId: str, outDate: datetime.date) -> int:
    """
    Calculate the price without the tax to be paid by the customer
    :param customerId: Customer Id to fetch the rate of room and check-in date from allCustomers table
    :param outDate: To calculate the number of days
    :rtype: int
    :return: Number of days times rate of room
    """
    comm = f"select rate from {global_.tbAllCustomers} " \
           f"where customerId='{customerId}'"
    global_.cur.execute(comm)
    rate: int = global_.cur.fetchone()[0]
    # Get the rate of the room

    comm = f"select checkInDate from {global_.tbAllCustomers} " \
           f"where customerId='{customerId}'"
    global_.cur.execute(comm)
    inDate = global_.cur.fetchone()[0]
    # Get the checkInDate

    noOfDays = (outDate - inDate).days
    # .days() to get as int
    # No of days

    return rate*noOfDays


def addRoom(roomId: str, ac: str, qty: int, rate: int, tax: float) -> int:
    """
    Add room to rooms table
    :param roomId: Unique room id depending on the type of room
    :param ac: y or n, AC room or not
    :param qty: Quantity of rooms vacant
    :param rate: Rate of the room
    :param tax: Tax to be paid for the room
    :return: 1 (No error) or 0 (Room already exists)
    :rtype: int
    """
    # Convert Yes/No to a single character
    if ac.casefold() == "Yes".casefold():
        ac = "y"
    elif ac.casefold() == "No".casefold():
        ac = "n"

    def sendComm() -> None:
        """
        Add room to the table
        :rtype: None
        """
        comm1 = f"insert into {global_.tbRooms} values(" \
                f"'{roomId}', " \
                f"'{ac}', " \
                f"{qty}, " \
                f"{rate}, " \
                f"{tax}" \
                ")"
        global_.cur.execute(comm1)
        global_.conn.commit()
        # Commit the changes made

    comm = f"select * from {global_.tbRooms}"
    global_.cur.execute(comm)
    res: tuple = global_.cur.fetchall()
    # Check if room already exists

    if len(res) == 0:
        # If no room exists, res will be empty

        sendComm()
        # Create the room

        return 1

    else:
        # Check if required room exists
        for room in res:
            if room[0] == roomId:
                # Room Exists

                return 0

        sendComm()
        # Create the room

        return 1


def searchRoom(roomId: str) -> int:
    """
    Check if room exists to be able to update it
    :param roomId: To check if room with this id exists
    :return: 1(Room exists) or 0 (Room doesn't exist)
    :rtype: int
    """
    comm = f"select RoomId from {global_.tbRooms}"
    global_.cur.execute(comm)
    # Select all the roomIds

    res: tuple[tuple[str]] = global_.cur.fetchall()

    for existingId in res:
        if existingId[0] == roomId:
            return 1

    return 0


def selectRoom(roomId: str) -> tuple[int, int, float]:
    """
    Fetch info about a particular room
    :param roomId: Id of Room of which details are to be displayed
    :return: (Quantity of vacant rooms, room rate, room tax)
    :rtype: tuple[int, int, float]
    """
    comm = "select * from {} where roomId='{}'".format(global_.tbRooms, roomId)
    global_.cur.execute(comm)
    res: tuple = global_.cur.fetchone()
    # Select all the info of the room

    qty: int = res[2]
    rate: int = res[3]
    tax: float = res[4]
    return qty, rate, tax


def updateRoom(roomId: str, qty: int, rate: int, tax: float) -> None:
    """
    Update the room details
    :param roomId: Id of room whose details are to be updated
    :param qty: New Quantity of room
    :param rate: New Rate of room
    :param tax: New Tax of room
    :rtype: None
    """
    comm = f"update {global_.tbRooms} set qty={qty} where roomId='{roomId}'"
    global_.cur.execute(comm)
    # Update the room quantity

    comm = f"update {global_.tbRooms} set rate={rate} where roomId='{roomId}'"
    global_.cur.execute(comm)
    # Update the room rate

    comm = f"update {global_.tbRooms} set tax={tax} where roomId='{roomId}'"
    global_.cur.execute(comm)
    # Update the room tax

    global_.conn.commit()
    # Commit the changes made


def showRooms() -> tuple[tuple]:
    """
    Return the details of all the rooms
    :rtype: tuple[tuple]
    """
    comm = f"select * from {global_.tbRooms}"
    global_.cur.execute(comm)
    res: tuple[tuple] = global_.cur.fetchall()
    # Select all the rooms

    return res


def retrieveAllData() -> tuple[tuple]:
    """
    Return all the customer's data to form csv file
    :rtype: tuple[tuple]
    :return:
    """
    comm = f"select * from {global_.tbAllCustomers}"
    global_.cur.execute(comm)
    allCustomers: tuple[tuple] = global_.cur.fetchall()
    # Select all the customers from the allCustomers table

    return allCustomers


def endConn() -> None:
    """
    Close the MySQL connection before exiting
    :rtype: None
    """
    global_.cur.close()
    # Close the cursor

    global_.conn.close()
    # Close the connection
