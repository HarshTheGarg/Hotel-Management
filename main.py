"""
Hotel Management Project
Main python file
"""

import tkinter as tk  # tkinter for gui

from tkinter import messagebox  # pop up message box

from tkinter import ttk  # for scrollBar

import MySql.mysqlInit as sqlInit  # MySQL connection initialize

from MySql import queries  # Queries to be run

import global_  # Variables file

import generateInvoice  # To generate invoice

import sendSMS  # File to send SMS

import os  # To restart the file

from PIL import ImageTk, Image  # To use images

import random  # To generate OTP

import datetime  # To get current date

import generateCSV  # To generate CSV file

# global variables to use throughout the file
global frame1
global otpEntered

darkModeFlag = False
# Light mode by default

root = tk.Tk()
# Tkinter gui initialized

root.title("Hotel Man")
# Window Title

root.iconbitmap("./Assets/LogoBlack.ico")
# Window icon

root.geometry("500x350")
# Initial window size

root.resizable(False, False)
# Disable resizing of windows


def eventErrorHandler(event: tk.Event) -> None:
    """
    To remove error in the IDE for not using argument passed by the bind function
    :param event: event passed by bind function
    :rtype: None
    """
    str(event) * 2


def clearFrame(frame: tk.Frame) -> None:
    """
    Clear a frame before populating it
    :rtype: None
    :param frame: Tkinter Frame whose children are to be destroyed
    """

    for frame_content in frame.winfo_children():
        frame_content.destroy()


def intCheck(text: str) -> int:
    """
    Check if Mobile/Aadhaar entered is integer
    :param text: Value Entered by user
    :rtype: int
    :return: 1 (Correct input) or 0 (Incorrect input)
    """
    try:
        int(text)
        return 1
    except ValueError:
        return 0


def lenCheck(text: str, length: int) -> int:
    """
    Check if correct number of digits are entered for aadhaar and mobile number)
    :param text: Entered Value
    :param length: Expected Length
    :rtype: int
    :return: 1 (Correct input) or 0 (Incorrect input)
    """
    if len(text) == length:
        return 1
    else:
        return 0


def successMsgBox(title: str, message: str) -> None:
    """
    Success message pop-up box using tk.messagebox
    :param title: Title of Success Message
    :param message: Main Body
    :rtype: None
    """
    messagebox.showinfo(title, message)


def errorMsgBox(title: str = "Error", message: str = "Some Error Occurred") -> None:
    """
    Error message pop-up box using tk.messagebox
    :param title: Title of Success Message
    :param message: Main Body
    :rtype: None
    """
    messagebox.showerror(title, message)


def confirmMsgBox(title: str, message: str) -> str:
    """
    Pop-up Message Box to ask for confirmation
    :param title: Title of Success Message
    :param message: Content of the pop-up
    :rtype: str
    :return: user's answer
    """
    return messagebox.askquestion(title, message)


def genOTP() -> int:
    """
    Generate a 6 digit random otp
    :rtype: int
    :return: 6 digit random number
    """
    otp: int = random.randrange(100000, 999999)
    return otp


def getDate() -> datetime.date:
    """
    Current date
    :rtype: date
    :return: Current Date
    """
    return datetime.date.today()


def exitApplication() -> None:
    """
    End the connection with MySQL and exit the application
    :rtype: None
    """
    confirm: str = confirmMsgBox("Exit", "Are you sure you want to exit?")

    if confirm == "yes":
        global_.updateStatus("Bye!")
        # Updating the status bar

        queries.endConn()
        # Sign out of MySQL

        root.destroy()
        # Destroy the window


def checkIn() -> None:
    """
    Display the check-in options and check-in the customer
    :rtype: None
    """

    global_.updateStatus("Customers!! :-D")
    # Update the Status Bar

    root.title("Hotel Man - Check In")
    # Changing the title of the window

    clearFrame(frame1)
    # Clearing the right frame

    """ 
    Display the check-in options
    """

    # Customer Name Label
    customerNameLab = tk.Label(frame1, text="Name of Customer:")
    customerNameLab.grid(row=0, column=0, pady=30, padx=5, sticky=tk.E)

    # Customer Name Entry Box
    customerName = tk.Entry(frame1, width=30, justify=tk.CENTER)
    customerName.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=tk.W)
    customerName.focus_set()  # Auto focus on first entry box

    # Customer Aadhaar Label
    customerAadhaarLab = tk.Label(frame1, text="Customer's Aadhaar Number:")
    customerAadhaarLab.grid(row=0, column=2, pady=25, padx=5, sticky=tk.E)

    # Customer Aadhaar Entry Box
    customerAadhaar = tk.Entry(frame1, width=30, justify=tk.CENTER)
    customerAadhaar.grid(row=0, column=3, padx=(15, 0), pady=25, sticky=tk.W)

    # Customer Mobile Number Label
    customerMobileLab = tk.Label(frame1, text="Mobile Number:")
    customerMobileLab.grid(row=1, column=0, pady=25, padx=5, sticky=tk.E)

    # Customer Mobile Entry Box
    customerMobile = tk.Entry(frame1, width=30, justify=tk.CENTER)
    customerMobile.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=tk.W)

    # Customer Room Id Label
    customerRoomIdLab = tk.Label(frame1, text="Room Type: ")
    customerRoomIdLab.grid(row=1, column=2, pady=25, padx=5, sticky=tk.E)

    # Rooms Option Menu
    room = tk.StringVar()  # Tkinter string data type

    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]
    # All the options to be displayed

    room.set("Select")
    # Set default value to be displayed

    # To display the drop down menu
    customerRoomId = tk.OptionMenu(frame1, room, *roomNames)
    customerRoomId.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=tk.W)

    def addCustomer() -> None:
        """
        Validate the entries and add the customer
        :rtype: None
        """
        global otpEntered
        # To use the global variable

        # If room is not selected
        if room.get() == "Select":

            global_.updateStatus("Select a room")
            # Update the Status Bar

            errorMsgBox("Customer", "Please Select a room")
            # Display error message

        # If some room is selected
        else:
            roomId = ""

            if room.get() == "Normal (AC)":
                roomId = "NA"
            elif room.get() == "Normal (No AC)":
                roomId = "NN"
            elif room.get() == "Deluxe":
                roomId = "DA"
            elif room.get() == "Suite":
                roomId = "SA"

            aadhaarNumber = customerAadhaar.get().replace(" ", "")
            # Remove the spaces from the customer's aadhaar number

            mobileNumber = customerMobile.get().replace(" ", "")
            # Remove the spaces from the customer's mobile number

            # Validate Aadhaar Number
            if intCheck(aadhaarNumber) == 0 or lenCheck(aadhaarNumber, 12) == 0:

                # If wrong Aadhaar number entered
                global_.updateStatus("Aadhaar Number Doesn't Exists")
                # Update the Status Bar

                errorMsgBox("Wrong Input", "Please Input Correct Aadhaar number")
                # Display error message

            # Validate mobile number
            elif intCheck(mobileNumber) == 0 or lenCheck(mobileNumber, 10) == 0:

                # Wrong Mobile Entered
                global_.updateStatus("Mobile number Doesn't Exist")
                # Update the Status Bar

                errorMsgBox("Wrong Input", "Please Input Correct Mobile number")
                # Display the error message

            # If both the mobile, aadhaar number are correct
            else:

                otp = genOTP()
                # Generate the OTP

                sendSMS.sendOTP(otp, mobileNumber)
                # Send the otp to the customer

                global_.updateStatus("OTP Sent!")
                # Update the Status Bar

                def validateOtp() -> None:
                    """
                    Check whether the otp entered is correct and then add the customer to the database
                    with appropriate messages
                    :rtype: None
                    """

                    if str(otp) != otpEntered:
                        # Wrong otp

                        global_.updateStatus("Oops! Try Again")
                        # Update the Status Bar

                        errorMsgBox("OTP", "Wrong OTP Entered")
                        # Display the Error Message

                    else:
                        customerAdded = queries.addCustomer(
                            customerName.get().title(),
                            aadhaarNumber,
                            mobileNumber,
                            roomId,
                            str(getDate())
                        )
                        # Running the MySQL query

                        # Some error occurred
                        if customerAdded[0] == 0:

                            global_.updateStatus("Try Again...:-\\")
                            # Update the Status Bar

                            errorMsgBox("Customer Check In", customerAdded[1])
                            # Displaying the error

                        # No error
                        elif customerAdded[0] == 1:

                            global_.updateStatus("Customer Added! ^_^")
                            # Update the Status Bar

                            successMsgBox(
                                "Customer Check In",
                                "Customer Checked In\nCustomer Id is {}".format(customerAdded[1])
                            )
                            # Displaying the success message

                            checkIn()
                            # Running the function again to add another customer

                def showOTPScreen() -> None:
                    """
                    Show the screen to enter the otp
                    :rtype: None
                    """
                    otpScreen = tk.Toplevel()
                    # Tkinter new screen

                    otpScreen.title("One Time Password")
                    # Title for new screen

                    otpScreen.iconbitmap("./Assets/LogoBlack.ico")
                    # Sign in screen icon

                    # Frame for otp
                    otpFrame = tk.Frame(otpScreen, pady=5)
                    otpFrame.pack()

                    # Enter OTP Label
                    otpLabel = tk.Label(otpFrame, text="Enter OTP: ")
                    otpLabel.grid(row=0, column=0)

                    # OTP Entry Field
                    otpEntry = tk.Entry(otpFrame, justify=tk.CENTER)
                    otpEntry.grid(row=0, column=1)
                    otpEntry.focus_set()
                    otpEntry.configure(show="*")

                    def submit() -> None:
                        """
                        Destroy the pop-up and call the function to add the customer
                        :rtype: None
                        """
                        global otpEntered
                        # To use the value outside the function

                        otpEntered = otpEntry.get()

                        otpScreen.destroy()
                        # Destroying the otp screen

                        validateOtp()
                        # Validate the otp and add the customer

                    # Otp screen Submit Button
                    but = tk.Button(otpScreen, text="Submit", command=submit)
                    but.pack(pady=(10, 0))

                    # Key bind to submit on pressing return
                    def returnPressedInner(event: tk.Event) -> None:
                        """
                        Action to perform when return is pressed on the otp screen
                        :param event: Automatically passed by the bind function
                        :rtype: None
                        """
                        eventErrorHandler(event)
                        submit()

                    # Binding all elements of otp screen to call submit func when Return key is pressed
                    for otpScreen_children in otpScreen.winfo_children():
                        otpScreen_children.bind("<Return>", returnPressedInner)

                    otpScreen.configure(pady=50)
                    # Vertical Padding of the popup screen

                    otpScreen.geometry("500x230")
                    # Dimensions of the SignIn screen

                    otpScreen.focus_force()
                    # To automatically focus on the pop up screen

                    if darkModeFlag:
                        # Dark Mode

                        otpScreen.configure(bg="#333333")
                        otpScreen.iconbitmap("./Assets/LogoColor.ico")

                        otpFrame.configure(bg="#333333")

                        otpLabel.configure(bg="#333333", fg="#DADADA")
                        otpEntry.configure(bg="#5D5D5D", fg="#DADADA", relief=tk.FLAT, borderwidth=1)

                        but.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)

                showOTPScreen()
                # Show the pop-up screen to enter the otp

    # Check-in screen Submit Button
    submitCustomerDetails = tk.Button(frame1, text="Submit", width=15, command=addCustomer)
    submitCustomerDetails.grid(row=2, column=1, columnspan=2, pady=15)

    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when return is pressed on the check-in customer screen
        :param event: Automatically passed by the bind function
        :rtype: None
        """
        eventErrorHandler(event)
        addCustomer()

    # Key bind to submit on pressing return
    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerName.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerAadhaar.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerMobile.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        customerRoomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerRoomId.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=tk.FLAT, borderwidth=3)
        customerRoomId["menu"].config(bg="#555555", fg="#DADADA", bd=0)

        submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def updateCustomer() -> None:
    """
    Update the customer's information
    :rtype: None
    """
    global_.updateStatus("Filled Something Wrong?")
    # Update status bar

    root.title("Hotel Man - Update Customer details")
    # Changing the Title of the window

    clearFrame(frame1)
    # Clearing the frame

    # Select Customer Id Label
    customerIdLab = tk.Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=tk.E)

    # CustomerId entry Box
    customerId = tk.Entry(frame1, justify=tk.CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=tk.W)
    customerId.focus_set()  # Auto focus

    # To Fetch Customer's Details
    def searchCustomer() -> None:
        """
        Fetch the customer's details and update the database with the correct details
        :rtype: None
        """
        customerResult = queries.searchCustomer(str(customerId.get()))
        # Run the MySQL query to see if customerId exists

        if customerResult == 0:
            # Customer Not found

            global_.updateStatus("Couldn't Find Him/Her")
            # Update the status bar

            errorMsgBox("Customer", "Customer Not Found\nPlease Try Again")
            # Display the error

            updateCustomer()
            # Run the main update function again

        elif customerResult == 1:
            # Customer Found

            global_.updateStatus("Correct Your Mistakes")
            # Update the status bar

            name, aadhaar, mobile = queries.selectCustomer(customerId.get())
            # Get the customer's details to display

            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]
            # Add spaces in aadhaar number for better readability

            # Customer Name Label
            customerNameLab = tk.Label(frame1, text="Name of customer:")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=tk.E)

            # Customer Name Entry Box
            customerName = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerName.insert(tk.END, str(name))  # Inserting the already existing values
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=tk.W)
            customerName.focus_set()

            # Customer Aadhaar Label
            customerAadhaarLab = tk.Label(frame1, text="Customer's Aadhaar Number:")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=tk.E)

            # Customer Aadhaar Entry Box
            customerAadhaar = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerAadhaar.insert(tk.END, aadhaar)  # Inserting the already existing values
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=tk.W)

            # Customer Mobile Number Label
            customerMobileLab = tk.Label(frame1, text="Mobile Number: ")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=tk.E)

            # Customer Mobile Entry Box
            customerMobile = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerMobile.insert(tk.END, str(mobile))  # Inserting the already existing values
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=tk.W)

            def submitUpdateCustomer() -> None:
                """
                Send the query to the database
                :rtype: None
                """
                aadhaarNumber = customerAadhaar.get().replace(" ", "")
                # Remove spaces from aadhaar number entered

                mobileNumber = customerMobile.get().replace(" ", "")
                # Remove spaces from mobile number entered

                if intCheck(aadhaarNumber) == 0 or lenCheck(aadhaarNumber, 12) == 0:
                    # Check if the aadhaar number is of correct length and all integers

                    global_.updateStatus("Aadhaar Doesn't Exist")
                    # Update the status bar

                    errorMsgBox("Wrong Input", "Please Input Correct Aadhaar number")
                    # Display the error message

                elif intCheck(mobileNumber) == 0 or lenCheck(mobileNumber, 10) == 0:
                    # Check if the mobile number is of correct length and all integers

                    global_.updateStatus("Mobile Number Doesn't Exist")
                    # Update the status bar

                    errorMsgBox("Wrong Input", "Please Input Correct Mobile number")
                    # Display the error message

                else:
                    # If both the mobile, aadhaar number are correct

                    global_.updateStatus("Updating...")
                    # Update the status bar

                    queries.updateCustomer(customerId.get(), customerName.get(), aadhaarNumber, mobileNumber)
                    # Run the query

                    successMsgBox("Customer", "Record Updated Successfully")
                    # Display the success message

                    updateCustomer()
                    # Run the update function again

            # Update Customer Details Button
            submitCustomerDetails = tk.Button(frame1, text="Update", width=15, command=submitUpdateCustomer)
            submitCustomerDetails.grid(row=2, column=2, columnspan=2, sticky=tk.W)

            # Key bind to submit on pressing return
            def returnPressedInner(event: tk.Event) -> None:
                """
                Action to perform when return is pressed on the update customer's screen when details are displayed
                :param event: Automatically passed by the bind function
                :rtype: None
                """
                submitUpdateCustomer()
                eventErrorHandler(event)

            for frame1_children_inner in frame1.winfo_children():
                frame1_children_inner.bind("<Return>", returnPressedInner)

            if darkModeFlag:
                # Dark Mode

                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

                submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = tk.Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, columnspan=2, pady=25, sticky=tk.W)

    # Key bind to submit on pressing return
    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when return is pressed on the update screen when details are not displayed
        :param event: Automatically passed by the bind function
        :rtype: None
        """
        searchCustomer()
        eventErrorHandler(event)

    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def checkOut() -> None:
    """
    Remove a customer from the database and generate the invoice
    :rtype: None
    """
    global_.updateStatus("Someone Leaving?")
    # Update status bar

    root.title("Hotel Man - Check Out")
    # Change the Title of the window

    clearFrame(frame1)
    # Clear the frame

    # Select Customer Id Label
    customerIdLab = tk.Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=tk.E)

    # Customer Id Entry Box
    customerId = tk.Entry(frame1, justify=tk.CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=tk.W)
    customerId.focus_set()

    # search the customer in database
    def searchCustomer() -> None:
        """
        Search if customer exists in the database. If present display the details and ask to remove from database
        :rtype: None
        """
        customerResult = queries.searchCustomer(str(customerId.get()))
        # Run the MySQL query to see if customerId exists

        if customerResult == 0:
            # Customer Not found

            global_.updateStatus("Couldn't Find the Customer")
            # Update status bar

            errorMsgBox("Customer", "Customer Not Found\nPlease Try Again")
            # Display the error

            customerId.delete(0, tk.END)
            # Emptying the entry box

        elif customerResult == 1:
            # Customer Found

            global_.updateStatus("Sure this is the one?")
            # Update status bar

            name, aadhaar, mobile = queries.selectCustomer(customerId.get())
            # Get the customer's details to display

            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]
            # Add spaces in aadhaar number for better readability

            # Customer Name Label
            customerNameLab = tk.Label(frame1, text="Name of customer: ")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=tk.E)

            # Customer Name Entry Box
            customerName = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerName.insert(tk.END, str(name))  # Inserting the already existing values
            customerName.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=tk.W)

            # Customer Aadhaar Label
            customerAadhaarLab = tk.Label(frame1, text="Customer's Aadhaar Number: ")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=tk.E)

            # Customer Aadhaar Entry Box
            customerAadhaar = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerAadhaar.insert(tk.END, aadhaar)  # Inserting the already existing values
            customerAadhaar.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=tk.W)

            # Customer Mobile Number Label
            customerMobileLab = tk.Label(frame1, text="Mobile Number: ")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=tk.E)

            # Customer Mobile Entry Box
            customerMobile = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerMobile.insert(tk.END, str(mobile))  # Inserting the already existing values
            customerMobile.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=tk.W)

            def removeCustomer() -> None:
                """
                Send the query to remove the customer from the database and generate the invoice
                :rtype: None
                """
                global_.updateStatus("Removing...")
                # Update status bar

                cRoomId, cCheckInDate, cCheckOutDate, cRate, price, tax = \
                    queries.removeCustomer(str(customerId.get()), getDate())
                # Send the query to remove the customer

                roomType: str = ""

                # Retrieve room name using roomId
                if cRoomId == "DA":
                    roomType = "Deluxe"
                elif cRoomId == "NA":
                    roomType = "Normal (AC)"
                elif cRoomId == "NN":
                    roomType = "Normal (No AC)"
                elif cRoomId == "SA":
                    roomType = "Suite"

                generateInvoice.generateInvoice(
                    str(customerId.get()), name, aadhaar,
                    mobile, roomType, cCheckInDate, cCheckOutDate,
                    cRate, price, tax
                )
                # Generate the invoice and save on desktop

                sendSMS.sendByeSMS(name, price, tax, mobile)
                # Send the goodbye sms to the customer with thr price to be paid

                successMsgBox("Check Out", "Customer has checked out\nInvoice saved on Desktop")
                # Display the success message

                checkOut()
                # Run the checkout function again

            # Remove Customer Button
            removeCustomerButton = tk.Button(frame1, text="Check Out", width=15, command=removeCustomer)
            removeCustomerButton.grid(row=2, column=2, columnspan=2, sticky=tk.W)

            def returnPressedInner(event: tk.Event) -> None:
                """
                Action to perform when return key is pressed when details are displayed
                :param event: Automatically passed by the bind function
                :rtype: None
                """
                eventErrorHandler(event)
                removeCustomer()

            for frame1_children_inner in frame1.winfo_children():
                frame1_children_inner.bind("<Return>", returnPressedInner)

            if darkModeFlag:
                # Dark Mode

                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                       borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                          borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                         borderwidth=3)

                removeCustomerButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = tk.Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, columnspan=2, pady=25, sticky=tk.W)

    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when return key is pressed when Details are not displayed
        :param event: Automatically passed by the bind function
        :rtype: None
        """
        eventErrorHandler(event)
        searchCustomer()

    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def findCustomer() -> None:
    """
    Display the details of a particular the customer
    :rtype: None
    """
    global_.updateStatus("Who Do You Wanna Find?")
    # Update the status bar

    root.title("Hotel Man - Find Customer")
    # Change the title of the window

    clearFrame(frame1)
    # Clear the frame

    # Select Customer Id Label
    customerIdLab = tk.Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=tk.E)

    # Customer Id Entry Box
    customerId = tk.Entry(frame1, justify=tk.CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=tk.W)
    customerId.focus_set()

    def searchCustomer() -> None:
        """
        Search whether customer exists in the database and if exists, display all the information
        :rtype: None
        """

        global_.updateStatus("Finding...")
        # Update the status bar

        customerResult = queries.searchCustomer(str(customerId.get()), "find")
        # Run the MySQL query to see if customerId exists

        if customerResult == 0:
            # Customer Not found

            global_.updateStatus("Couldn't Find Anyone with that ID :(")
            # Update the status bar

            errorMsgBox("Customer", "Customer Id Not Found\nPlease Try Again")
            # Display the error

            customerId.delete(0, tk.END)
            # Clear the entry box

        elif customerResult == 1:
            # Customer Found

            global_.updateStatus("Found Him/Her ;)")
            # Update the status bar

            name, aadhaar, mobile = queries.selectCustomer(customerId.get(), "find")
            # Get the customer's details to display

            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]
            # Add spaces in aadhaar number for better readability

            # Customer Name Label
            customerNameLab = tk.Label(frame1, text="Name of customer:")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=tk.E)

            # Customer Name Entry Box
            customerName = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerName.insert(tk.END, str(name))  # Inserting the already existing values
            customerName.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=tk.W)

            # Customer Aadhaar Label
            customerAadhaarLab = tk.Label(frame1, text="Customer's Aadhaar Number:")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=tk.E)

            # Customer Aadhaar Entry Box
            customerAadhaar = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerAadhaar.insert(tk.END, aadhaar)  # Inserting the already existing values
            customerAadhaar.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=tk.W)

            # Customer Mobile Number Label
            customerMobileLab = tk.Label(frame1, text="Mobile Number:")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=tk.E)

            # Customer Mobile Entry Box
            customerMobile = tk.Entry(frame1, width=30, justify=tk.CENTER)
            customerMobile.insert(tk.END, str(mobile))  # Inserting the already existing values
            customerMobile.configure(state=tk.DISABLED)  # So that details cannot be changed
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=tk.W)

            if darkModeFlag:
                # Dark Mode

                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                       borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                          borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(disabledbackground="#505050", disabledforeground="#888888", relief=tk.FLAT,
                                         borderwidth=3)

    # Search Button
    submitButton = tk.Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, pady=25)

    # Key bind to submit on pressing return
    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when return key is pressed
        :param event:  Automatically passed by the bind function
        :rtype: None
        """
        eventErrorHandler(event)
        searchCustomer()

    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def showCustomers() -> None:
    """
    Display the details of the customers depending upon the sign-in mode
    :rtype: None
    """
    global_.updateStatus("All Customers")
    # Update the status bar

    root.title("Hotel Man - Show All Customers")
    # Change the Title of the window

    clearFrame(frame1)
    # Clear the frame

    customers = queries.showCustomers()
    # Contains the details of all the customers (if any)

    if not customers:
        # If no customers are found in the database

        global_.updateStatus("Try Better Advertisements Maybe? :(")
        # Update status bar

        errorMsgBox("Search", "No Customers Found")
        # Show error

    else:
        # If Customers Found
        global_.updateStatus("All the Customers")
        # Update status bar

        """Add the scrollBar
        We are adding a canvas and displaying all the details on the canvas, the scrollbar controls the canvas"""

        # Create a canvas
        myCanvas = tk.Canvas(frame1)
        myCanvas.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add a scroll Bar for the Canvas
        scrollBar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=myCanvas.yview)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas for scroll Bar
        myCanvas.configure(yscrollcommand=scrollBar.set)
        myCanvas.bind("<Configure>", lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))

        # Bind mouse wheel to scroll Bar
        def onMouseWheel(e):
            myCanvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        myCanvas.bind_all("<MouseWheel>", onMouseWheel)

        frame12 = tk.Frame(myCanvas)
        # Create frame inside the canvas on which details are displayed

        myCanvas.create_window((0, 0), window=frame12, anchor="nw")
        # Add frame in canvas

        if global_.accessLevel == "User":
            # Display the data of only the checked in customers

            """Headings"""
            # Id
            customerIdHeading = tk.Label(
                frame12,
                text="Customer Id",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerIdHeading.grid(row=0, column=0, sticky=tk.NSEW, padx=(50, 0))

            # Name
            customerNameHeading = tk.Label(
                frame12,
                text="Name",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerNameHeading.grid(row=0, column=1, stick=tk.NSEW)

            # Aadhaar
            customerAadhaarHeading = tk.Label(
                frame12,
                text="Aadhaar Number",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerAadhaarHeading.grid(row=0, column=2, sticky=tk.NSEW)

            # Mobile Number
            customerMobileHeading = tk.Label(
                frame12,
                text="Mobile",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerMobileHeading.grid(row=0, column=3, sticky=tk.NSEW)

            # Room Type
            customerRoomHeading = tk.Label(
                frame12,
                text="Room Type",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerRoomHeading.grid(row=0, column=4, sticky=tk.NSEW)

            row_num = 1

            # Loop to display all the customer's information
            for customer_data in customers:

                # Retrieving room name using roomId
                if customer_data[4] == "DA":
                    customerRoom = "Deluxe"
                elif customer_data[4] == "NA":
                    customerRoom = "Normal (AC)"
                elif customer_data[4] == "NN":
                    customerRoom = "Normal"
                elif customer_data[4] == "SA":
                    customerRoom = "Suite"
                else:
                    customerRoom = ""

                aadhaarNumber = customer_data[2][0:4] + " " + customer_data[2][4:8] + " " + customer_data[2][8:12]
                # Add spaces in aadhaar number for better readability

                mobileNUmber = customer_data[3][0:5] + " " + customer_data[3][5:10]
                # Add spaces in mobile number for better readability

                """Contents"""
                # Customer Id
                customerIdContentLabel = tk.Label(
                    frame12,
                    text=customer_data[0],
                    relief=tk.GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerIdContentLabel.grid(row=row_num, column=0, sticky=tk.NSEW, padx=(50, 0))

                # Customer Name
                customerNameContentLabel = tk.Label(
                    frame12,
                    text=customer_data[1],
                    relief=tk.GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerNameContentLabel.grid(row=row_num, column=1, sticky=tk.NSEW)

                # Customer Aadhaar
                customerAadhaarContentLabel = tk.Label(
                    frame12,
                    text=aadhaarNumber,
                    relief=tk.GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerAadhaarContentLabel.grid(row=row_num, column=2, sticky=tk.NSEW)

                # Mobile number
                customerMobileContentLabel = tk.Label(
                    frame12,
                    text=mobileNUmber,
                    relief=tk.GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerMobileContentLabel.grid(row=row_num, column=3, sticky=tk.NSEW)

                # Room Type
                customerRoomContentLabel = tk.Label(
                    frame12,
                    text=customerRoom,
                    relief=tk.GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerRoomContentLabel.grid(row=row_num, column=4, sticky=tk.NSEW)

                row_num += 1

                if darkModeFlag:
                    # Dark Mode

                    customerIdContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerNameContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerAadhaarContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerMobileContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

            if darkModeFlag:
                # Dark Mode

                customerIdHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerNameHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerAadhaarHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerRoomHeading.configure(bg="#404040", fg="#DADADA", bd=0)

        elif global_.accessLevel == "Admin":
            # Display the data of all customers even if the have checked out

            """Headings"""
            # Id
            customerIdHeading = tk.Label(
                frame12,
                text="Customer Id",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerIdHeading.grid(row=0, column=0, sticky=tk.NSEW)

            # Name
            customerNameHeading = tk.Label(
                frame12,
                text="Name",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerNameHeading.grid(row=0, column=1, stick=tk.NSEW)

            # Aadhaar
            customerAadhaarHeading = tk.Label(
                frame12,
                text="Aadhaar Number",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerAadhaarHeading.grid(row=0, column=2, sticky=tk.NSEW)

            # Mobile Number
            customerMobileHeading = tk.Label(
                frame12,
                text="Mobile",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerMobileHeading.grid(row=0, column=3, sticky=tk.NSEW)

            # Room Type
            customerRoomHeading = tk.Label(
                frame12,
                text="Room Type",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerRoomHeading.grid(row=0, column=4, sticky=tk.NSEW)

            # CheckInDate
            CheckInDateHeading = tk.Label(
                frame12,
                text="Check in Date",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            CheckInDateHeading.grid(row=0, column=5, sticky=tk.NSEW)

            # CheckOutDate
            CheckOutDateHeading = tk.Label(
                frame12,
                text="Check out Date",
                bg="#C0C0C0",
                relief=tk.GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            CheckOutDateHeading.grid(row=0, column=6, sticky=tk.NSEW)

            row_number = 1

            # Loop to display all the customer's information
            for customer in customers:

                # Retrieve room name using roomId
                if customer[4] == "DA":
                    customerRoom = "Deluxe"
                elif customer[4] == "NA":
                    customerRoom = "Normal (AC)"
                elif customer[4] == "NN":
                    customerRoom = "Normal"
                elif customer[4] == "SA":
                    customerRoom = "Suite"
                else:
                    customerRoom = ""

                aadhaarNumber = customer[2][0:4] + " " + customer[2][4:8] + " " + customer[2][8:12]
                # Add spaces in aadhaar number for better readability

                mobileNUmber = customer[3][0:5] + " " + customer[3][5:10]
                # Add spaces in mobile number for better readability

                checkOutDate = customer[6]
                # Check out date value

                if checkOutDate is None:
                    checkOutDate = "-"

                # Customer Id
                customerIdContentLabel = tk.Label(
                    frame12,
                    text=customer[0],
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerIdContentLabel.grid(row=row_number, column=0, sticky=tk.NSEW)

                # Customer Name
                customerNameContentLabel = tk.Label(
                    frame12,
                    text=customer[1],
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerNameContentLabel.grid(row=row_number, column=1, sticky=tk.NSEW)

                # Customer Aadhaar
                customerAadhaarContentLabel = tk.Label(
                    frame12,
                    text=aadhaarNumber,
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerAadhaarContentLabel.grid(row=row_number, column=2, sticky=tk.NSEW)

                # Mobile number
                customerMobileContentLabel = tk.Label(
                    frame12,
                    text=mobileNUmber,
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerMobileContentLabel.grid(row=row_number, column=3, sticky=tk.NSEW)

                # Room Type
                customerRoomContentLabel = tk.Label(
                    frame12,
                    text=customerRoom,
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerRoomContentLabel.grid(row=row_number, column=4, sticky=tk.NSEW)

                # Check in Date
                customerCheckInDateContentLabel = tk.Label(
                    frame12,
                    text=customer[5],
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerCheckInDateContentLabel.grid(row=row_number, column=5, sticky=tk.NSEW)

                # Check in Date
                customerCheckOutDateContentLabel = tk.Label(
                    frame12,
                    text=str(checkOutDate),
                    relief=tk.GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerCheckOutDateContentLabel.grid(row=row_number, column=6, sticky=tk.NSEW)

                row_number += 1

                if darkModeFlag:
                    # Dark Mode

                    customerIdContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerNameContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerAadhaarContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerMobileContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerCheckInDateContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerCheckOutDateContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

            def saveCSV() -> None:
                """
                Save a csv file containing the data of all the customers who have ever checked-in
                :rtype: None
                """
                rawData = queries.retrieveAllData()
                finalData: list[list] = []

                for data in rawData:

                    roomType = ""

                    # Retrieve room name using roomId
                    if data[4] == "DA":
                        roomType = "Deluxe"
                    elif data[4] == "NA":
                        roomType = "Normal"
                    elif data[4] == "NN":
                        roomType = "Normal"
                    elif data[4] == "SA":
                        roomType = "Suite"

                    customerData: list[str, str, str, str, str, datetime.date, datetime.date, str, int, float]

                    customerData = [data[0]] + [data[1]] + ["'" + str(data[2])] + [data[3]] + \
                                   [roomType] + [str(data[5])] + [str(data[6])] + [data[7]] + \
                                   [str(data[8])] + [str(float(data[9]))]
                    # ' is added before aadhaar number so that all the digits are displayed in excel

                    finalData += [customerData]

                generateCSV.generateCSV(finalData, getDate())
                # Generate the csv and saving it on the desktop

                successMsgBox("CSV", "File saved on desktop")
                # Show the success message

            # Save Button
            saveCSVButton = tk.Button(frame12, text="Save CSV", command=saveCSV)
            saveCSVButton.grid(row=row_number + 1, column=3, pady=(30, 0), sticky=tk.NSEW)

            if darkModeFlag:
                # Dark Mode

                customerIdHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerNameHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerAadhaarHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerRoomHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                CheckInDateHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                CheckOutDateHeading.configure(bg="#404040", fg="#DADADA", bd=0)

                saveCSVButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

        if darkModeFlag:
            # Dark Mode

            myCanvas.configure(bg="#2A2A2A", bd=0, highlightthickness=0)
            frame12.configure(bg="#2A2A2A", bd=0, padx=5)

            """style = ttk.Style()
            print(style.theme_names())
            print(style.element_options("Vertical.TScrollbar.trough"))
            style.theme_use('alt')
            style.configure("Vertical.TScrollbar", troughcolor="#505050")"""


def addRoom() -> None:
    """
    Show the options to add a room to the database
    :rtype: None
    """
    global_.updateStatus("Add Rooms")
    # Update status bar

    root.title("Hotel Man - Add Room")
    # Change the Title of the window

    clearFrame(frame1)
    # Clear the frame

    # Room Id Label
    roomIdLab = tk.Label(frame1, text="Select Room Type:")
    roomIdLab.grid(row=0, column=0, pady=15, padx=5, sticky=tk.E)

    # Room Id Option Menu
    room = tk.StringVar()  # Tkinter string data type

    # List of room options
    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]

    length = len(max(roomNames, key=len))
    # Length of the word with max length

    room.set("Select")
    # Set default value for Room Selector

    # AC Available Label
    ACLab = tk.Label(frame1, text="AC: ")
    ACLab.grid(row=0, column=2, pady=15, padx=15, sticky=tk.E)

    # AC Value Label
    ACLab2 = tk.Label(frame1)
    ACLab2.grid(row=0, column=3, padx=(15, 0), pady=15, sticky=tk.W)
    ACLab2.configure(text="No Info")

    def updateAC(event: tk.Event) -> None:
        """
        Check if the room selected has AC
        :rtype: None
        """
        eventErrorHandler(event)
        if room.get() == "Normal (No AC)":
            ac = "No"
        elif room.get() == "Select":
            ac = "No Info"
        else:
            ac = "Yes"
        ACLab2.configure(text=ac)

    # Options menu to select the room and update AC status
    roomIdSelector = tk.OptionMenu(frame1, room, *roomNames, command=updateAC)
    roomIdSelector.config(width=length)
    roomIdSelector.grid(row=0, column=1, padx=(15, 30), pady=15, sticky=tk.W)

    # Quantity of rooms Label
    qtyRoomsLab = tk.Label(frame1, text="How many rooms are available? :")
    qtyRoomsLab.grid(row=1, column=0, pady=15, padx=5, sticky=tk.E)

    # Quantity of Rooms Scale
    qtyRooms = tk.Scale(frame1, from_=0, to=10, orient=tk.HORIZONTAL)
    qtyRooms.configure(length=127)
    qtyRooms.grid(row=1, column=1, padx=(15, 30), pady=15, sticky=tk.W)

    # Room Rate Label
    roomRateLab = tk.Label(frame1, text="Rate(\u20B9): ")  # u"\u20B9" -> rupees symbol
    roomRateLab.grid(row=1, column=2, pady=15, padx=15, sticky=tk.E)

    # Room Rate Entry Box
    roomRate = tk.Entry(frame1, justify=tk.CENTER)
    roomRate.configure(width=length + 6)
    roomRate.grid(row=1, column=3, padx=(15, 0), pady=15, sticky=tk.W)

    # Tax of rooms Label
    taxRoomsLab = tk.Label(frame1, text="Room Tax (%):")
    taxRoomsLab.grid(row=2, column=0, pady=15, padx=5, sticky=tk.E)

    # Tax entry box
    taxRoom = tk.Entry(frame1, justify=tk.CENTER)
    taxRoom.configure(width=length + 6)
    taxRoom.grid(row=2, column=1, padx=(15, 30), pady=(15, 0), sticky=tk.W)

    def submitRoomAdd() -> None:
        """
        Send the query to the database to add the room after validating the information entered
        :rtype: None
        """

        if room.get() == "Select":
            # If a room is not selected

            global_.updateStatus("Select A Room Type")
            # Update the status bar

            errorMsgBox("Rooms", "Please Select a Room Type")
            # Display the error

        elif roomRate.get() == "":
            # If room rate is not entered

            global_.updateStatus("Enter Rate")
            # Update the status bar

            errorMsgBox("Rooms", "Rate not Entered")
            # Display the error

        elif taxRoom.get() == "":
            # If room tax is not entered

            global_.updateStatus("Enter Tax")
            # Update the status bar

            errorMsgBox("Rooms", "Tax not Entered")
            # Display the error

        else:
            # Everything is entered
            roomId = ""

            # Convert room type to appropriate RoomId
            if room.get() == "Normal (AC)":
                roomId = "NA"
            elif room.get() == "Normal (No AC)":
                roomId = "NN"
            elif room.get() == "Deluxe":
                roomId = "DA"
            elif room.get() == "Suite":
                roomId = "SA"

            global_.updateStatus("Adding...")
            # Update status bar

            res = queries.addRoom(
                roomId,
                ACLab2.cget("text"),
                int(qtyRooms.get()),
                int(roomRate.get()),
                float(taxRoom.get())
            )
            # Run the MySQL query

            if res == 1:
                # If room was added

                global_.updateStatus("Room Added")
                # Update status bar

                successMsgBox("Room Added", "Room Added Successfully")
                # Display the success message

            elif res == 0:
                # If some error occurred

                global_.updateStatus("Room Exists, Try Updating it")
                # Update status bar

                errorMsgBox("Failed", "Room Already Exists")
                # Display the error message

            addRoom()
            # Run the function again to add more rooms

    # Submit Button
    submitCustomerDetails = tk.Button(frame1, text="Submit", command=submitRoomAdd)
    submitCustomerDetails.configure(width=length + 2)
    submitCustomerDetails.grid(row=2, column=3, padx=(15, 0), pady=15, sticky=tk.W)

    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when the return key is pressed
        :rtype: None
        """
        eventErrorHandler(event)
        submitRoomAdd()

    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        roomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomIdSelector.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=tk.FLAT, borderwidth=3)
        roomIdSelector["menu"].config(bg="#555555", fg="#DADADA", bd=0)

        ACLab.configure(bg="#2A2A2A", fg="#DADADA")
        ACLab2.configure(bg="#2A2A2A", fg="#DADADA")

        qtyRoomsLab.configure(bg="#2A2A2A", fg="#DADADA", padx=5)
        qtyRooms.configure(bg="#2A2A2A", fg="#DADADA", highlightthickness=0, troughcolor="#505050", bd=0)

        roomRateLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomRate.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        taxRoomsLab.configure(bg="#2A2A2A", fg="#DADADA")
        taxRoom.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

        submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def updateRoom() -> None:
    """
    Update the details of a room that exists
    :rtype:
    """
    global_.updateStatus("Update Room")
    # Update status bar

    root.title("Hotel Man - Update Room Details")
    # Change the Title of the window

    clearFrame(frame1)
    # Clear the frame

    # Room Id Label
    roomIdLab = tk.Label(frame1, text="Select Room Type:")
    roomIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=tk.E)

    # List of room options
    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]

    length = len(max(roomNames, key=len))
    # Length of the word with max length

    room = tk.StringVar()  # Tkinter string data type
    # Room Id Option Menu

    room.set("Select")
    # Set default value for Room Selector

    # Options menu to select the room
    roomIdSelector = tk.OptionMenu(frame1, room, *roomNames)
    roomIdSelector.config(width=length)
    roomIdSelector.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=tk.W)

    def searchRoom() -> None:
        """
        Search by roomId if room exists in database
        :rtype: None
        """

        if room.get() == "Select":
            # If room is not selected

            global_.updateStatus("Please Select a room from the Drop-Down")
            # Update the status bar

            errorMsgBox("Room Update", "Please Select a Room Type")
            # Display the error

        else:
            # If room is selected

            # Set the RoomId from room name
            if room.get() == "Normal (AC)":
                updateRoomId = "NA"
            elif room.get() == "Normal (No AC)":
                updateRoomId = "NN"
            elif room.get() == "Deluxe":
                updateRoomId = "DA"
            else:
                updateRoomId = "SA"

            res = queries.searchRoom(updateRoomId)
            # Run the query to update

            if res == 0:
                # If there was some error

                global_.updateStatus("Room Doesn't Exist. Try Adding it First")
                # Update the status bar

                errorMsgBox("Room", "Room Not Found")
                # Display error message

            elif res == 1:
                # No Error

                global_.updateStatus("Room Found")
                # Update the status bar

                qty, rate, tax = queries.selectRoom(updateRoomId)
                # Get qty, rate and tax of selected room

                # Quantity of rooms Label
                qtyRoomsLab = tk.Label(frame1, text="How many rooms are available? :")
                qtyRoomsLab.grid(row=1, column=0, pady=30, padx=5, sticky=tk.E)

                # Quantity of Rooms Selector
                qtyRooms = tk.Scale(frame1, from_=0, to=10, orient=tk.HORIZONTAL)
                qtyRooms.configure(length=127)
                qtyRooms.set(qty)  # Inserting the already existing value
                qtyRooms.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=tk.W)

                # Room Rate Label
                roomRateLab = tk.Label(frame1, text="Rate(\u20B9): ")  # "\u20B9" -> rupees symbol
                roomRateLab.grid(row=1, column=2, pady=25, padx=(15, 0), sticky=tk.W)

                # Room Rate Entry Box
                roomRate = tk.Entry(frame1, justify=tk.CENTER)
                roomRate.configure(width=length + 6)
                roomRate.insert(tk.END, str(rate))  # Inserting the already existing value
                roomRate.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=tk.W)

                # Tax of rooms Label
                taxRoomsLab = tk.Label(frame1, text="Room Tax (%):")
                taxRoomsLab.grid(row=2, column=0, pady=15, padx=5, sticky=tk.E)

                # Tax entry box
                taxRoom = tk.Entry(frame1, width=15, justify=tk.CENTER)
                taxRoom.configure(width=length + 6)
                taxRoom.insert(tk.END, str(tax))  # Inserting the already existing value
                taxRoom.grid(row=2, column=1, padx=(15, 30), pady=15, sticky=tk.W)

                def submitRoomUpdate() -> None:
                    """
                    Send the query to update the room details to the database
                    :rtype: Nome
                    """

                    # Run query to update the room
                    queries.updateRoom(
                        updateRoomId,
                        int(qtyRooms.get()),
                        int(roomRate.get()),
                        float(taxRoom.get())
                    )

                    global_.updateStatus("Room Updated")
                    # Update the status bar

                    successMsgBox("Room Update", "Room Updated Successfully")
                    # Show the success message

                    updateRoom()
                    # Run the function again to update more rooms

                # Update Button
                submitCustomerDetails = tk.Button(frame1, text="Submit", width=length + 2, command=submitRoomUpdate)
                submitCustomerDetails.grid(row=2, column=3, padx=(15, 0), pady=15)

                def returnPressedInner(event: tk.Event) -> None:
                    """
                    Action to perform when return key is pressed when details are displayed
                    :rtype: None
                    """
                    eventErrorHandler(event)
                    submitRoomUpdate()

                for frame1_Children_inner in frame1.winfo_children():
                    frame1_Children_inner.bind("<Return>", returnPressedInner)

                if darkModeFlag:
                    # Dark Mode

                    qtyRoomsLab.configure(bg="#2A2A2A", fg="#DADADA", padx=5)
                    qtyRooms.configure(bg="#2A2A2A", fg="#DADADA", highlightthickness=0, bd=0, troughcolor="#505050")

                    roomRateLab.configure(bg="#2A2A2A", fg="#DADADA")
                    roomRate.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

                    taxRoomsLab.configure(bg="#2A2A2A", fg="#DADADA")
                    taxRoom.configure(bg="#505050", fg="#DADADA", relief=tk.FLAT, borderwidth=3)

                    submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0,
                                                    highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = tk.Button(frame1, text="Search", command=searchRoom)
    submitButton.configure(width=length + 2)
    submitButton.grid(row=0, column=3, padx=(15, 0), pady=25, sticky=tk.W)

    def returnPressed(event: tk.Event) -> None:
        """
        Action to perform when return key is pressed when details are not displayed
        :rtype: None
        """
        eventErrorHandler(event)
        searchRoom()

    for frame1_children in frame1.winfo_children():
        frame1_children.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        roomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomIdSelector.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=tk.FLAT, borderwidth=3)
        roomIdSelector["menu"].config(bg="#555555", fg="#DADADA")

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


def showRooms() -> None:
    """
    Display the details of all the rooms available
    :rtype: None
    """
    global_.updateStatus("Showing All Rooms")
    # Update the status bar

    root.title("Hotel Man - Show All Rooms")
    # Change the Title of the window

    clearFrame(frame1)
    # Clear the frame

    rooms = queries.showRooms()

    if not rooms:
        # If tuple is empty, no rooms found

        errorMsgBox("Search", "No Rooms Found")
        # Display the error

        addRoom()
        # Run the addRoom function so that rooms can be added

    else:
        # Rooms Found, Display the table

        """Headings"""
        # Id
        roomHeading = tk.Label(
            frame1,
            text="Room Type",
            bg="#C0C0C0",
            relief=tk.GROOVE,
            padx=20,
            pady=8)
        roomHeading.grid(row=0, column=0, sticky=tk.NSEW, padx=(125, 0), pady=(100, 0))

        # AC
        acHeading = tk.Label(
            frame1,
            text="AC Room",
            bg="#C0C0C0",
            relief=tk.GROOVE,
            padx=20,
            pady=8)
        acHeading.grid(row=0, column=1, stick=tk.NSEW, pady=(100, 0))

        # Quantity
        qtyHeading = tk.Label(
            frame1,
            text="Vacant",
            bg="#C0C0C0",
            relief=tk.GROOVE,
            padx=20,
            pady=8)
        qtyHeading.grid(row=0, column=2, sticky=tk.NSEW, pady=(100, 0))

        # Rate
        rateHeading = tk.Label(
            frame1,
            text="Rate",
            bg="#C0C0C0",
            relief=tk.GROOVE,
            padx=20,
            pady=8)
        rateHeading.grid(row=0, column=3, sticky=tk.NSEW, pady=(100, 0))

        # Tax
        taxHeading = tk.Label(
            frame1,
            text="Tax (%)",
            bg="#C0C0C0",
            relief=tk.GROOVE,
            padx=20,
            pady=8)
        taxHeading.grid(row=0, column=4, sticky=tk.NSEW, pady=(100, 0))

        # Loop to display all the room's information

        row_number = 1
        for room_data in rooms:

            # Retrieve room name using roomId
            showRoomId = ""
            if room_data[0] == "DA":
                showRoomId = "Deluxe"
            elif room_data[0] == "NA":
                showRoomId = "Normal"
            elif room_data[0] == "NN":
                showRoomId = "Normal"
            elif room_data[0] == "SA":
                showRoomId = "Suite"

            acStatus = ""

            # Retrieve AC Status
            if room_data[1] == "y":
                acStatus = "Yes"
            elif room_data[1] == "n":
                acStatus = "No"

            # Room Id
            idRoomContentLabel = tk.Label(
                frame1,
                text=showRoomId,
                relief=tk.GROOVE,
                padx=20,
                pady=8)
            idRoomContentLabel.grid(row=row_number, column=0, sticky=tk.NSEW, padx=(125, 0))

            # AC room?
            acRoomContentLabel = tk.Label(
                frame1,
                text=acStatus,
                relief=tk.GROOVE,
                padx=20,
                pady=8)
            acRoomContentLabel.grid(row=row_number, column=1, sticky=tk.NSEW)

            # Quantity of rooms empty
            qtyRoomContentLabel = tk.Label(
                frame1,
                text=str(room_data[2]),
                relief=tk.GROOVE,
                padx=20,
                pady=8)
            qtyRoomContentLabel.grid(row=row_number, column=2, sticky=tk.NSEW)

            # Rate of each room
            rateRoomContentLabel = tk.Label(
                frame1,
                text="\u20B9" + str(room_data[3]),
                relief=tk.GROOVE,
                padx=20,
                pady=8)
            rateRoomContentLabel.grid(row=row_number, column=3, sticky=tk.NSEW)  # "\u20B9" -> rupees symbol

            # Tax of rooms
            taxRoomContentLabel = tk.Label(
                frame1,
                text=str(room_data[4]),
                relief=tk.GROOVE,
                padx=20,
                pady=8)
            taxRoomContentLabel.grid(row=row_number, column=4, sticky=tk.NSEW)

            row_number += 1

            if darkModeFlag:
                # Dark Mode

                idRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                acRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                qtyRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                rateRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                taxRoomContentLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

        if darkModeFlag:
            # Dark Mode

            roomHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            acHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            qtyHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            rateHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            taxHeading.configure(bg="#404040", fg="#DADADA", bd=0)


def submitted() -> None:
    """
    Display the main screen with all the options available for the access mode in which the user enters
    :rtype: None
    """
    global frame1

    if global_.condition == 1:
        # If sign in was successful

        global_.updateStatus("Connection Successful")
        # Update the status bar

        imgLabel.destroy()
        # Destroy the logo displayed on the welcome screen

        logInButton.destroy()
        # Destroy the log-in button displayed on the welcome screen

        darkModeButton.destroy()
        # Destroy the dark mode button on the welcome screen

        root.geometry("1050x700")
        # Set the size of the main screen

        """Place all the options and frames"""
        # The main window inside which all the content is placed
        workingWindow = tk.Frame(root, bd=0)
        workingWindow.pack(fill=tk.X, ipadx=20)

        # Left (Navigation) Pane
        frame0 = tk.LabelFrame(workingWindow, pady=50, bd=0)
        frame0.pack(side=tk.LEFT, padx=(10, 10), pady=0)

        imgLight = tk.PhotoImage(file="Assets/LogoBlackNameSmall.png")
        # Load the logo image which will be displayed on the main screen when in light mode

        # Display the logo on top-right corner
        my_canvas = tk.Canvas(frame0)
        my_canvas.create_image(0, 0, anchor=tk.NW, image=imgLight)
        my_canvas.place(x=15, y=0)

        # Customer Options Frame, contains buttons related to the customers
        frame01 = tk.LabelFrame(frame0, text="Customer", pady=10, padx=10)
        frame01.grid(row=1, column=0, pady=(100, 30), padx=10, columnspan=2)

        """Place customer option buttons on frame01"""

        # Button to CheckIn
        button011 = tk.Button(frame01, text="Check In", width=15, command=checkIn)
        button011.pack(pady=3)

        # Button to Update record
        button012 = tk.Button(frame01, text="Update", width=15, command=updateCustomer)
        button012.pack(pady=3)

        # Button to Check Out
        button013 = tk.Button(frame01, text="Check Out", width=15, command=checkOut)
        button013.pack(pady=3)

        # Button to Search for a Customer
        button014 = tk.Button(frame01, text="Find", width=15, command=findCustomer)
        button014.pack(pady=3)

        # Button to show all customers present in the hotel
        button015 = tk.Button(frame01, text="Show All", width=15, command=showCustomers)
        button015.pack(pady=3)

        # Room Options frame, contains buttons related to the rooms
        frame02 = tk.LabelFrame(frame0, text="Rooms", pady=10, padx=10)

        if global_.accessLevel == "User":
            # Rooms option will not be displayed
            # Change the placement of the customer frame to be centered
            frame01.grid(row=0, column=0, pady=130, padx=10, columnspan=2)

        elif global_.accessLevel == "Admin":
            # Rooms option will be displayed

            # Place the room options frame
            frame02.grid(row=2, column=0, pady=30, padx=10, columnspan=2)

            """Place the room option buttons on frame02"""
            # Button to add rooms
            button021 = tk.Button(frame02, text="Add", width=15, command=addRoom)
            button021.pack(pady=3)

            # Button to Update room details
            button022 = tk.Button(frame02, text="Update", width=15, command=updateRoom)
            button022.pack(pady=3)

            # Button to Show all available rooms
            button023 = tk.Button(frame02, text="Show All", width=15, command=showRooms)
            button023.pack(pady=3)

        def signOut() -> None:
            """
            End the connection with the database and close the window and then start the application again
            :rtype: None
            """

            queries.endConn()
            # Sign out of MySQL

            root.destroy()
            # Close the window

            os.system("HotelMan.exe")
            # Start the file again

        # Display the sign out button
        signOutButton = tk.Button(frame0, text="Sign Out", command=signOut, width=10)
        signOutButton.grid(row=3, column=0, padx=(10, 5))

        # Display the exit button
        exitButton = tk.Button(frame0, text="Exit", command=exitApplication, width=10)
        exitButton.grid(row=3, column=1, padx=(5, 10))

        # Right Pane, will display the options when a button is clicked
        frame1 = tk.LabelFrame(workingWindow, pady=150, padx=50, bd=0)
        frame1.pack(padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        if darkModeFlag:
            # Dark Mode

            workingWindow.configure(bg="#2A2A2A")
            frame0.configure(bg="#2A2A2A")
            # Background color of the bottom-most elements

            my_canvas.delete("all")
            # Delete the already existing logo image

            imgDark = tk.PhotoImage(file="Assets/LogoWhiteNameSmall.png")
            # Load the logo image for dark mode

            my_canvas.create_image(0, 0, anchor=tk.NW, image=imgDark)
            my_canvas.configure(bg="#2A2A2A", bd=0, highlightthickness=0)
            # Add the image for dark mode

            frame01.configure(bg="#2A2A2A", fg="#DADADA")
            # Background of the customer options frame

            # Background for the buttons of frame01 (customer information buttons)
            for frame01_buttons in frame01.winfo_children():
                frame01_buttons.configure(bg="#505050", fg="#DADADA", bd=0, pady=3)

            frame02.configure(bg="#2A2A2A", fg="#DADADA")
            # Background of the rooms options frame

            # Background for the buttons of frame02 (rooms information buttons)
            for frame02_buttons in frame02.winfo_children():
                frame02_buttons.configure(bg="#505050", fg="#DADADA", bd=0, pady=3)

            signOutButton.configure(bg="#505050", fg="#DADADA", bd=0, pady=5)
            exitButton.configure(bg="#505050", fg="#DADADA", bd=0, pady=5)

            frame1.configure(bg="#2A2A2A", fg="#DADADA")

        root.mainloop()  # Canvas wont work without mainloop

    else:
        # If connection to database was failed

        global_.updateStatus("Cannot Connect, Try Again")
        # Update the status bar

        errorMsgBox("SignIn Error", "Failed to log in, try again")
        # Display the error Message


def signIn() -> None:
    """
    Display the sign-in screen
    :rtype: None
    """
    global_.updateStatus("Connecting...")
    # Update the status bar

    root.unbind("<Return>")
    # Stop getting the sign in screen everytime user presses enter(return) key

    def escapePressed(event: tk.Event) -> None:
        """
        Escape the program if the esc key is pressed
        :rtype: None
        """
        exitApplication()
        print(event)

    root.bind("<Escape>", escapePressed)

    global_.accessLevel = "User"
    # Default access level mode

    signInScreen = tk.Toplevel()
    # Tkinter new pop-up screen

    signInScreen.title("Sign in")
    # Title for new screen

    signInScreen.iconbitmap("./Assets/LogoBlack.ico")
    # Sign in screen icon

    # Frame for username
    userNameFrame = tk.Frame(signInScreen, pady=5)
    userNameFrame.pack()

    # Enter username Label
    unameLabel = tk.Label(userNameFrame, text="Enter Username: ")
    unameLabel.grid(row=0, column=0)

    # Username Entry Field
    uname = tk.Entry(userNameFrame, justify=tk.CENTER)
    uname.grid(row=0, column=1)
    uname.focus_set()

    # Frame for password
    passwordFrame = tk.Frame(signInScreen, pady=5)
    passwordFrame.pack()

    # Enter Password Label
    pWordLabel = tk.Label(passwordFrame, text="Enter Password: ")
    pWordLabel.grid(row=0, column=0)

    # Password Entry Field
    pWord = tk.Entry(passwordFrame, show="*", justify=tk.CENTER)
    pWord.grid(row=0, column=1)

    def togglePasswordView() -> None:
        """
        Toggle the content of the password entry box from text to * and vice versa
        :rtype: None
        """
        if pWord.cget("show") == "*":
            pWord.configure(show="")
        else:
            pWord.configure(show="*")

    # Toggle Password View
    togglePassword = tk.Button(signInScreen, text="Toggle Password View", command=togglePasswordView)
    togglePassword.pack(pady=(10, 0))

    def submit() -> None:
        """
        Try and Sign-in the user
        """

        global_.username = uname.get()
        # Username that the user entered

        global_.password = pWord.get()
        # Password that the user entered

        sqlInit.createDbAndTables()
        # Initialize the database

        signInScreen.destroy()
        # Close the sign in screen

        submitted()
        # Displaying all the options(checkIn, checkOut...)

    # SignIn Button
    but = tk.Button(signInScreen, text="Sign In", command=submit)
    but.pack(pady=(10, 0))

    signInScreen.configure(pady=50)
    # Vertical Padding of the Sign-in screen

    signInScreen.geometry("500x230")
    # Dimensions of the Sign-in screen

    signInScreen.focus_force()
    # Automatically focus on the pop up screen

    def enterAdmin(event: tk.Event) -> None:
        """
        Change the access level if the user clicks the key combination
        :rtype: None
        """
        eventErrorHandler(event)
        global_.accessLevel = "Admin"
        signInScreen.title("Sign in (Admin)")

    signInScreen.bind("<Alt-KeyPress-8>", enterAdmin)
    # To enter the admin log in mode when user presses alt+8

    def returnPressed(event: tk.Event) -> None:
        """
        Run submit() when return key is pressed
        """
        eventErrorHandler(event)
        submit()

    signInScreen.bind("<Return>", returnPressed)

    if darkModeFlag:
        # Dark Mode

        signInScreen.configure(bg="#333333")
        # Change background color of the sign-in screen pop-up

        signInScreen.iconbitmap("./Assets/LogoColor.ico")
        # Change the icon color

        signInScreen.geometry("500x250")

        userNameFrame.configure(bg="#333333")
        unameLabel.configure(bg="#333333", fg="#DADADA")

        passwordFrame.configure(bg="#333333")
        pWordLabel.configure(bg="#333333", fg="#DADADA")

        uname.configure(bg="#5D5D5D", fg="#DADADA", relief=tk.FLAT, borderwidth=1)
        pWord.configure(bg="#5D5D5D", fg="#DADADA", relief=tk.FLAT, borderwidth=1)

        togglePassword.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)
        but.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)


# Logo image to be displayed on the welcome screen
logoImg = ImageTk.PhotoImage(Image.open("./Assets/LogoBlackName.png"))
imgLabel = tk.Label(image=logoImg)
imgLabel.pack()

# Button to initiate log in and display sign in screen
logInButton = tk.Button(root, text="Log In", command=signIn)
logInButton.pack(pady=(20, 0))


def darkMode() -> None:
    """
    Start the dark mode
    """
    global darkModeFlag
    darkModeFlag = True

    root.configure(bg="#2A2A2A")
    root.iconbitmap("./Assets/LogoColor.ico")
    # Change the icon

    logoImgDark = ImageTk.PhotoImage(Image.open("./Assets/LogoWhiteName.png"))
    imgLabel.configure(bg="#2A2A2A", image=logoImgDark)
    logInButton.configure(bd=0, bg="#505050", fg="#DADADA", padx=8, pady=5)
    global_.statusBar.configure(bg="#343434", fg="#DADADA", bd=0)

    darkModeButton.configure(bd=0, bg="#505050", fg="#DADADA", padx=8, pady=5)
    darkModeButton.configure(state=tk.DISABLED)
    # Cannot turn the dark mode on again


# Button to enable dark mode
darkModeButton = tk.Button(root, text="Dark Mode", command=darkMode)
darkModeButton.pack(pady=(20, 10))

# Status Bar
global_.statusBar = tk.Label(root, text="Welcome", relief=tk.SUNKEN, anchor=tk.E, padx=10, height=2)
global_.statusBar.pack(side=tk.BOTTOM, fill=tk.X)


def returnPressedOuter(event: tk.Event) -> None:
    """
    Start the sign in when return is pressed on the welcome screen
    :rtype: None
    """
    eventErrorHandler(event)
    signIn()


root.bind("<Return>", returnPressedOuter)

root.mainloop()
# Start the main screen
