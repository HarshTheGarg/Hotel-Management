"""
Main python file
Hotel Management Project
"""

# tkinter for gui
from tkinter import *

# pop up message box
from tkinter import messagebox

# for scrollBar
from tkinter import ttk

# MySQL connection initializer
import MySql.mysqlInit as sqlInit

# Queries to be run
from MySql import queries

# Variables file
import global_

# To generate invoice
import generateInvoice

# File to send SMS
# import sendOTP  # todo

# To restart the file
import os

# To use images
from PIL import ImageTk, Image

# To generate OTP
import random

# To get current date
import datetime

# To generate CSV file
import generateCSV

# global variables to use throughout the file
global frame1
global otpEntered

# Tkinter gui initialized
root = Tk()

# Window Title
root.title("Hotel Man")

# Window icon
root.iconbitmap("./Assets/LogoBlack.ico")

# Initial window size
root.geometry("500x350")
root.resizable(height=0, width=0)

darkModeFlag = False


# To clear a frame before populating it
def clearFrame(frame):
    for i in frame.winfo_children():
        i.destroy()


# To check if Entry is integer
def intCheck(text):
    # int() will return no error if it can convert the argument
    try:
        int(text)
        return 1  # No error
    except ValueError:
        return 0  # Error


# To check if correct number of digits are entered (To be used for aadhaar and mobile number)
def lenCheck(text, length):
    if len(text) == length:
        return 1  # Correct length
    else:
        return 0  # Wrong length


# Success message pop up box using tkinter.messagebox
def successMsgBox(title, message):
    messagebox.showinfo(title, message)


# Error message pop up box using tkinter.messagebox
def errorMsgBox(title="Error", message="Some Error Occurred"):
    messagebox.showerror(title, message)


# Confirm Message Box
def confirmMsgBox(title, message):
    return messagebox.askquestion(title, message)


# OTP Generator
def genOTP():
    otp = random.randrange(10000, 99999)
    print(otp)
    return otp


# Get current date in required format
def getDate():
    return datetime.date.today()


# Function to exit
def exitApplication():
    confirm = confirmMsgBox("Exit", "Are you sure you want to exit?")

    if confirm == "yes":
        global_.updateStatus("Bye!")
        # Sign out of MySQL
        queries.endConn()

        # To close the current window and the logo canvas
        root.destroy()
        # root.quit()


# To add customer to database
def checkIn():
    global_.updateStatus("Customers!! :-D")

    # Changing the title of the window
    root.title("Hotel Man - Check In")

    # Clearing the right frame, since there might be some content
    clearFrame(frame1)

    # Displaying the options

    # Customer Name Label
    customerNameLab = Label(frame1, text="Name of Customer:")
    customerNameLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # Customer Name Entry Box
    customerName = Entry(frame1, width=30, justify=CENTER)
    customerName.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)
    customerName.focus_set()

    # Customer Aadhaar Label
    customerAadhaarLab = Label(frame1, text="Customer's Aadhaar Number:")
    customerAadhaarLab.grid(row=0, column=2, pady=25, padx=5, sticky=E)

    # Customer Aadhaar Entry Box
    customerAadhaar = Entry(frame1, width=30, justify=CENTER)
    customerAadhaar.grid(row=0, column=3, padx=(15, 0), pady=25, sticky=W)

    # Customer Mobile Number Label
    customerMobileLab = Label(frame1, text="Mobile Number:")
    customerMobileLab.grid(row=1, column=0, pady=25, padx=5, sticky=E)

    # Customer Mobile Entry Box
    customerMobile = Entry(frame1, width=30, justify=CENTER)
    customerMobile.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)

    # Customer Room Id Label
    customerRoomIdLab = Label(frame1, text="Room Type: ")
    customerRoomIdLab.grid(row=1, column=2, pady=25, padx=5, sticky=E)

    # Rooms Option Menu
    room = StringVar()  # Tkinter string data type

    # All the options to be displayed
    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]

    # Set default value to be displayed
    room.set("Select")

    # To display the drop down menu
    customerRoomId = OptionMenu(frame1, room, *roomNames)
    customerRoomId.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

    # To send query to add customer to database
    def addCustomer():

        # To use the global variable
        global otpEntered

        # If room is not selected
        if room.get() == "Select":

            global_.updateStatus("Select a room")

            errorMsgBox("Customer", "Please Select a room")

        # If some room is selected, setting roomId to suitable value
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

            # Removing the spaces from the customer's aadhaar number and saving it in aadhaarNumber
            aadhaarNumber = customerAadhaar.get().replace(" ", "")

            # Removing the spaces from the customer's mobile number and saving it in mobileNumber
            mobileNumber = customerMobile.get().replace(" ", "")

            # Checking if the aadhaar number is of correct length and all integers
            if intCheck(aadhaarNumber) == 0 or lenCheck(aadhaarNumber, 12) == 0:

                global_.updateStatus("Aadhaar Number Doesn't Exists")

                errorMsgBox("Wrong Input", "Please Input Correct Aadhaar number")

            # Checking if the mobile number is of correct length and all integers
            elif intCheck(mobileNumber) == 0 or lenCheck(mobileNumber, 10) == 0:

                global_.updateStatus("Mobile number Doesn't Exist")

                errorMsgBox("Wrong Input", "Please Input Correct Mobile number")

            # If both the mobile, aadhaar number are correct
            else:

                # Generating the OTP
                # otp = genOTP()  # todo

                # sendOTP.sendSMS(otp, mobileNumber)  # todo

                # global_.updateStatus("OTP Sent!")  # todo

                def validate():

                    # todo
                    # if str(otp) != otpEntered:

                    if False:

                        global_.updateStatus("Oops! Try Again")

                        errorMsgBox("OTP", "Wrong OTP Entered")

                    else:
                        # Running the MySQL query
                        # customerAdded -> tuple -> (condition, message)
                        customerAdded = queries.addCustomer(
                            customerName.get().title(),
                            aadhaarNumber,
                            mobileNumber,
                            roomId,
                            str(getDate())
                        )

                        # No error
                        if customerAdded[0] == 0:

                            global_.updateStatus("Try Again...:-\\")

                            # Displaying the error
                            errorMsgBox("Customer Check In", customerAdded[1])

                        # Some error
                        elif customerAdded[0] == 1:

                            global_.updateStatus("Customer Added! ^_^ ^_^")

                            # Displaying the success message
                            successMsgBox(
                                "Customer Check In", "Customer Checked In\n"
                                                     "Customer Id is {}".format(customerAdded[1]))

                            # Running the function again to add another customer
                            checkIn()

                def showOTPScreen():

                    # Tkinter new screen
                    otpScreen = Toplevel()

                    # Title for new screen
                    otpScreen.title("One Time Password")

                    # Sign in screen icon
                    otpScreen.iconbitmap("./Assets/LogoBlack.ico")

                    # Frame for otp
                    otpFrame = Frame(otpScreen, pady=5)
                    otpFrame.pack()

                    # Enter OTP Label
                    otpLabel = Label(otpFrame, text="Enter OTP: ")
                    otpLabel.grid(row=0, column=0)

                    # OTP Entry Field
                    otpEntry = Entry(otpFrame, justify=CENTER)
                    otpEntry.grid(row=0, column=1)
                    otpEntry.focus_set()
                    otpEntry.configure(show="*")

                    def submit():
                        global otpEntered
                        otpEntered = otpEntry.get()
                        otpScreen.destroy()
                        validate()

                    # Submit Button
                    but = Button(otpScreen, text="Submit", command=submit)
                    but.pack(pady=(10, 0))

                    # Key bind to submit on pressing return
                    def returnPressedInner(event):
                        print(event)
                        addCustomer()

                    for j in otpScreen.winfo_children():
                        j.bind("<Return>", returnPressedInner)

                    # Vertical Padding of the popup screen
                    otpScreen.configure(pady=50)

                    # Dimensions of the SignIn screen
                    otpScreen.geometry("500x230")

                    # To automatically focus on the pop up screen
                    otpScreen.focus_force()

                    # Dark Mode
                    if darkModeFlag:
                        otpScreen.configure(bg="#333333")
                        otpScreen.iconbitmap("./Assets/LogoColor.ico")

                        otpFrame.configure(bg="#333333")

                        otpLabel.configure(bg="#333333", fg="#DADADA")
                        otpEntry.configure(bg="#5D5D5D", fg="#DADADA", relief=FLAT, borderwidth=1)

                        but.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)

                # showOTPScreen()  # todo

                validate()  # todo: remove

    # Submit Button
    submitCustomerDetails = Button(frame1, text="Submit", width=15, command=addCustomer)
    submitCustomerDetails.grid(row=2, column=1, columnspan=2, pady=15)

    # Key bind to submit on pressing return
    def returnPressed(event):
        print(event)
        addCustomer()

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerName.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerAadhaar.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerMobile.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        customerRoomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerRoomId.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=FLAT, borderwidth=3)
        customerRoomId["menu"].config(bg="#555555", fg="#DADADA", bd=0)

        submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# Update Customer Info:
def updateCustomer():
    global_.updateStatus("Filled Something Wrong?")

    # Changing the Title of the window
    root.title("Hotel Man - Update Customer details")

    # Clearing the frame
    clearFrame(frame1)

    # Select Customer Id Label
    customerIdLab = Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # CustomerId entry Box
    customerId = Entry(frame1, justify=CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)
    customerId.focus_set()

    # To Fetch Customer's Details
    def searchCustomer():

        # Running the MySQL query to see if customerId exists
        customerResult = queries.searchCustomer(str(customerId.get()))

        # Customer Not found
        if customerResult == 0:

            global_.updateStatus("Couldn't Find Him/Her")

            # Displaying the error
            errorMsgBox("Customer", "Customer Not Found\n"
                                    "Please Try Again")

            # Running the main update function again
            updateCustomer()

        # Customer Found
        elif customerResult == 1:

            global_.updateStatus("Correct Your Mistakes")

            # Getting the customer's details to display
            name, aadhaar, mobile = queries.selectCustomer(customerId.get())

            # Adding spaces in aadhaar number for better readability
            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]

            # Customer Name Label
            customerNameLab = Label(frame1, text="Name of customer:")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=E)

            # Customer Name Entry Box
            customerName = Entry(frame1, width=30, justify=CENTER)
            customerName.insert(END, str(name))  # Inserting the already existing values
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)
            customerName.focus_set()

            # Customer Aadhaar Label
            customerAadhaarLab = Label(frame1, text="Customer's Aadhaar Number:")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=E)

            # Customer Aadhaar Entry Box
            customerAadhaar = Entry(frame1, width=30, justify=CENTER)
            customerAadhaar.insert(END, aadhaar)  # Inserting the already existing values
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

            # Customer Mobile Number Label
            customerMobileLab = Label(frame1, text="Mobile Number: ")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=E)

            # Customer Mobile Entry Box
            customerMobile = Entry(frame1, width=30, justify=CENTER)
            customerMobile.insert(END, str(mobile))  # Inserting the already existing values
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=W)

            # To send the query to update details
            def submitUpdateCustomer():

                # Removing spaces from aadhaar number entered and saving it in aadhaarNumber
                aadhaarNumber = customerAadhaar.get().replace(" ", "")

                # Removing spaces from mobile number entered and saving it in mobileNumber
                mobileNumber = customerMobile.get().replace(" ", "")

                # Checking if the aadhaar number is of correct length and all integers
                if intCheck(aadhaarNumber) == 0 or lenCheck(aadhaarNumber, 12) == 0:

                    global_.updateStatus("Aadhaar Doesn't Exist")

                    errorMsgBox("Wrong Input", "Please Input Correct Aadhaar number")

                # Checking if the mobile number is of correct length and all integers
                elif intCheck(mobileNumber) == 0 or lenCheck(mobileNumber, 10) == 0:

                    global_.updateStatus("Mobile Number Doesn't Exist")

                    errorMsgBox("Wrong Input", "Please Input Correct Mobile number")

                # If both the mobile, aadhaar number are correct
                else:

                    global_.updateStatus("Updating...")

                    # Running the query
                    queries.updateCustomer(customerId.get(), customerName.get(), aadhaarNumber, mobileNumber)

                    # Display the success message
                    successMsgBox("Customer", "Record Updated Successfully")

                    # Running the update function again
                    updateCustomer()

            # Update Customer Details Button
            submitCustomerDetails = Button(frame1, text="Update", width=15, command=submitUpdateCustomer)
            submitCustomerDetails.grid(row=2, column=2, columnspan=2, sticky=W)

            # Key bind to submit on pressing return
            def returnPressedInner(event):
                submitUpdateCustomer()
                print(event)

            for j in frame1.winfo_children():
                j.bind("<Return>", returnPressedInner)

            # Dark Mode
            if darkModeFlag:
                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

                submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, columnspan=2, pady=25, sticky=W)

    # Key bind to submit on pressing return
    def returnPressed(event):
        searchCustomer()
        print(event)

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# To remove a customer
def checkOut():
    global_.updateStatus("MONEY! YAY!!!")

    # Changing the Title of the window
    root.title("Hotel Man - Check Out")

    # Clearing the frame
    clearFrame(frame1)

    # Select Customer Id Label
    customerIdLab = Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # Customer Id Entry Box
    customerId = Entry(frame1, justify=CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)
    customerId.focus_set()

    # To search the customer in database
    def searchCustomer():
        # Running the MySQL query to see if customerId exists
        customerResult = queries.searchCustomer(str(customerId.get()))

        # Customer Not found
        if customerResult == 0:

            global_.updateStatus("Couldn't Find the Customer")

            # Displaying the error
            errorMsgBox("Customer", "Customer Not Found\n"
                                    "Please Try Again")

            customerId.delete(0, END)

        # Customer Found
        elif customerResult == 1:

            global_.updateStatus("Sure this is the one?")

            # Getting the customer's details to display
            name, aadhaar, mobile = queries.selectCustomer(customerId.get())

            # Adding spaces in aadhaar number for better readability
            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]

            # Customer Name Label
            customerNameLab = Label(frame1, text="Name of customer: ")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=E)

            # Customer Name Entry Box
            customerName = Entry(frame1, width=30, justify=CENTER)
            customerName.insert(END, str(name))  # Inserting the already existing values
            customerName.configure(state=DISABLED)  # So that details cannot be changed
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)

            # Customer Aadhaar Label
            customerAadhaarLab = Label(frame1, text="Customer's Aadhaar Number: ")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=E)

            # Customer Aadhaar Entry Box
            customerAadhaar = Entry(frame1, width=30, justify=CENTER)
            customerAadhaar.insert(END, aadhaar)  # Inserting the already existing values
            customerAadhaar.configure(state=DISABLED)  # So that details cannot be changed
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

            # Customer Mobile Number Label
            customerMobileLab = Label(frame1, text="Mobile Number: ")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=E)

            # Customer Mobile Entry Box
            customerMobile = Entry(frame1, width=30, justify=CENTER)
            customerMobile.insert(END, str(mobile))  # Inserting the already existing values
            customerMobile.configure(state=DISABLED)  # So that details cannot be changed
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=W)

            # To send the query to remove details
            def removeCustomer():

                global_.updateStatus("Removing...")

                # Sending the query to remove the customer
                cRoomId, cCheckInDate, cCheckOutDate, cRate, price = \
                    queries.removeCustomer(str(customerId.get()), getDate())

                roomType = ""

                # Retrieving room name using roomId
                if cRoomId == "DA":
                    roomType = "Deluxe"
                elif cRoomId == "NA":
                    roomType = "Normal"
                elif cRoomId == "NN":
                    roomType = "Normal"
                elif cRoomId == "SA":
                    roomType = "Suite"

                generateInvoice.generateInvoice(
                    str(customerId.get()), name, aadhaar, mobile, roomType, cCheckInDate, cCheckOutDate, cRate, price
                )

                # Displaying the success message
                successMsgBox("Check Out", "Customer has checked out\nInvoice saved on Desktop")

                # Running the checkout function again
                checkOut()

            # Remove Customer Button
            removeCustomerButton = Button(frame1, text="Check Out", width=15, command=removeCustomer)
            removeCustomerButton.grid(row=2, column=2, columnspan=2, sticky=W)

            # Key bind to submit on pressing return
            def returnPressedInner(event):
                removeCustomer()
                print(event)

            for j in frame1.winfo_children():
                j.bind("<Return>", returnPressedInner)

            if darkModeFlag:
                # Dark Mode
                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                       borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                          borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                         borderwidth=3)

                removeCustomerButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, columnspan=2, pady=25, sticky=W)

    # Key bind to submit on pressing return
    def returnPressed(event):
        searchCustomer()
        print(event)

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# To fetch customer's details
def findCustomer():
    global_.updateStatus("Who Do You Wanna Find?")

    # Changing the Title of the window
    root.title("Hotel Man - Find Customer")

    # Clearing the frame
    clearFrame(frame1)

    # Select Customer Id Label
    customerIdLab = Label(frame1, text="Enter Customer Id:")
    customerIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # Customer Id Entry Box
    customerId = Entry(frame1, justify=CENTER)
    customerId.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)
    customerId.focus_set()

    # To search the customer in database
    def searchCustomer():

        global_.updateStatus("Finding...")

        # Running the MySQL query to see if customerId exists
        customerResult = queries.searchCustomer(str(customerId.get()), "find")

        # Customer Not found
        if customerResult == 0:

            global_.updateStatus("Couldn't Find Anyone with that ID :(")

            # Displaying the error
            errorMsgBox("Customer", "Customer Id Not Found\n"
                                    "Please Try Again")

            customerId.delete(0, END)

        # Customer Found
        elif customerResult == 1:

            global_.updateStatus("Found Him/Her ;)")

            # Getting the customer's details to display
            name, aadhaar, mobile = queries.selectCustomer(customerId.get(), "find")

            # Adding spaces in aadhaar number for better readability
            aadhaar = aadhaar[0:4] + " " + aadhaar[4:8] + " " + aadhaar[8:12]

            # Customer Name Label
            customerNameLab = Label(frame1, text="Name of customer:")
            customerNameLab.grid(row=1, column=0, pady=30, padx=5, sticky=E)

            # Customer Name Entry Box
            customerName = Entry(frame1, width=30, justify=CENTER)
            customerName.insert(END, str(name))  # Inserting the already existing values
            customerName.configure(state=DISABLED)  # So that details cannot be changed
            customerName.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)

            # Customer Aadhaar Label
            customerAadhaarLab = Label(frame1, text="Customer's Aadhaar Number:")
            customerAadhaarLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=E)

            # Customer Aadhaar Entry Box
            customerAadhaar = Entry(frame1, width=30, justify=CENTER)
            customerAadhaar.insert(END, aadhaar)  # Inserting the already existing values
            customerAadhaar.configure(state=DISABLED)  # So that details cannot be changed
            customerAadhaar.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

            # Customer Mobile Number Label
            customerMobileLab = Label(frame1, text="Mobile Number:")
            customerMobileLab.grid(row=2, column=0, pady=25, padx=5, sticky=E)

            # Customer Mobile Entry Box
            customerMobile = Entry(frame1, width=30, justify=CENTER)
            customerMobile.insert(END, str(mobile))  # Inserting the already existing values
            customerMobile.configure(state=DISABLED)  # So that details cannot be changed
            customerMobile.grid(row=2, column=1, padx=(15, 30), pady=25, sticky=W)

            if darkModeFlag:
                # Dark Mode
                customerNameLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerName.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                       borderwidth=3)

                customerAadhaarLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerAadhaar.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                          borderwidth=3)

                customerMobileLab.configure(bg="#2A2A2A", fg="#DADADA")
                customerMobile.configure(disabledbackground="#505050", disabledforeground="#888888", relief=FLAT,
                                         borderwidth=3)

    # Search Button
    submitButton = Button(frame1, text="Search", command=searchCustomer)
    submitButton.grid(row=0, column=2, pady=25)

    # Key bind to submit on pressing return
    def returnPressed(event):
        searchCustomer()
        print(event)

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        customerIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        customerId.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# To see all checked in Customers
def showCustomers():
    global_.updateStatus("All Customers")

    # Changing the Title of the window
    root.title("Hotel Man - Show All Customers")

    # Clearing the frame
    clearFrame(frame1)

    # to use throughout the function
    customerRoom = ""

    # A tuple of tuples of customer's information
    customers = queries.showCustomers()

    # If no customers are there
    if not customers:

        global_.updateStatus("Try Better Advertisements Maybe? :(")

        # Show error
        errorMsgBox("Search", "No Customers Found")

    # If Customers Found
    else:
        global_.updateStatus("All the Customers")

        # Adding the scrollBar
        # Create a canvas
        myCanvas = Canvas(frame1)
        myCanvas.pack(side=LEFT, fill=X, expand=True)

        # Add a scroll Bar to the Canvas
        scrollBar = ttk.Scrollbar(frame1, orient=VERTICAL, command=myCanvas.yview)
        scrollBar.pack(side=RIGHT, fill=Y)

        # Configure the canvas for scroll Bar
        myCanvas.configure(yscrollcommand=scrollBar.set)
        myCanvas.bind("<Configure>", lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))

        # Bind mouse wheel to scroll Bar
        def onMouseWheel(e):
            myCanvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        myCanvas.bind_all("<MouseWheel>", onMouseWheel)

        # Create frame inside the canvas
        frame12 = Frame(myCanvas)

        # Add frame to window in canvas
        myCanvas.create_window((0, 0), window=frame12, anchor="nw")

        if global_.accessLevel == "User":

            # Headings
            # Id
            customerIdHeading = Label(
                frame12,
                text="Customer Id",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerIdHeading.grid(row=0, column=0, sticky=NSEW, padx=(50, 0))

            # Name
            customerNameHeading = Label(
                frame12,
                text="Name",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerNameHeading.grid(row=0, column=1, stick=NSEW)

            # Aadhaar
            customerAadhaarHeading = Label(
                frame12,
                text="Aadhaar Number",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerAadhaarHeading.grid(row=0, column=2, sticky=NSEW)

            # Mobile Number
            customerMobileHeading = Label(
                frame12,
                text="Mobile",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerMobileHeading.grid(row=0, column=3, sticky=NSEW)

            # Room Type
            customerRoomHeading = Label(
                frame12,
                text="Room Type",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=20,
                pady=8,
                font=("Ariel", 10))
            customerRoomHeading.grid(row=0, column=4, sticky=NSEW)

            # j is row number
            j = 1

            # Loop to display all the customer's information
            for i in customers:

                # Retrieving room name using roomId
                if i[4] == "DA":
                    customerRoom = "Deluxe"
                elif i[4] == "NA":
                    customerRoom = "Normal (AC)"
                elif i[4] == "NN":
                    customerRoom = "Normal"
                elif i[4] == "SA":
                    customerRoom = "Suite"

                # Adding spaces in aadhaar number for better readability
                aadhaarNumber = i[2][0:4] + " " + i[2][4:8] + " " + i[2][8:12]

                # Adding spaces in mobile number for better readability
                mobileNUmber = i[3][0:5] + " " + i[3][5:10]

                # Customer Id
                customerId = Label(
                    frame12,
                    text=i[0],
                    relief=GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerId.grid(row=j, column=0, sticky=NSEW, padx=(50, 0))

                # Customer Name
                customerName = Label(
                    frame12,
                    text=i[1],
                    relief=GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerName.grid(row=j, column=1, sticky=NSEW)

                # Customer Aadhaar
                customerAadhaar = Label(
                    frame12,
                    text=aadhaarNumber,
                    relief=GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerAadhaar.grid(row=j, column=2, sticky=NSEW)

                # Mobile number
                customerMobile = Label(
                    frame12,
                    text=mobileNUmber,
                    relief=GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerMobile.grid(row=j, column=3, sticky=NSEW)

                # Room Type
                customerRoomLabel = Label(
                    frame12,
                    text=customerRoom,
                    relief=GROOVE,
                    padx=20,
                    pady=8,
                    font=("Ariel", 10))
                customerRoomLabel.grid(row=j, column=4, sticky=NSEW)

                j += 1

                # Dark Mode
                if darkModeFlag:
                    customerId.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerName.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerAadhaar.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerMobile.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerRoomLabel.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

            # Dark Mode
            if darkModeFlag:
                customerIdHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerNameHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerAadhaarHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerRoomHeading.configure(bg="#404040", fg="#DADADA", bd=0)

        elif global_.accessLevel == "Admin":
            # Headings
            # Id
            customerIdHeading = Label(
                frame12,
                text="Customer Id",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerIdHeading.grid(row=0, column=0, sticky=NSEW)

            # Name
            customerNameHeading = Label(
                frame12,
                text="Name",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerNameHeading.grid(row=0, column=1, stick=NSEW)

            # Aadhaar
            customerAadhaarHeading = Label(
                frame12,
                text="Aadhaar Number",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerAadhaarHeading.grid(row=0, column=2, sticky=NSEW)

            # Mobile Number
            customerMobileHeading = Label(
                frame12,
                text="Mobile",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerMobileHeading.grid(row=0, column=3, sticky=NSEW)

            # Room Type
            customerRoomHeading = Label(
                frame12,
                text="Room Type",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            customerRoomHeading.grid(row=0, column=4, sticky=NSEW)

            # CheckInDate
            CheckInDateHeading = Label(
                frame12,
                text="Check in Date",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            CheckInDateHeading.grid(row=0, column=5, sticky=NSEW)

            # CheckOutDate
            CheckOutDateHeading = Label(
                frame12,
                text="Check out Date",
                bg="#C0C0C0",
                relief=GROOVE,
                padx=10,
                pady=9,
                font=("Ariel", 9))
            CheckOutDateHeading.grid(row=0, column=6, sticky=NSEW)

            # j is row number
            j = 1

            # Loop to display all the customer's information
            for i in customers:

                # Retrieving room name using roomId
                if i[4] == "DA":
                    customerRoom = "Deluxe"
                elif i[4] == "NA":
                    customerRoom = "Normal (AC)"
                elif i[4] == "NN":
                    customerRoom = "Normal"
                elif i[4] == "SA":
                    customerRoom = "Suite"

                # Adding spaces in aadhaar number for better readability
                aadhaarNumber = i[2][0:4] + " " + i[2][4:8] + " " + i[2][8:12]

                # Adding spaces in mobile number for better readability
                mobileNUmber = i[3][0:5] + " " + i[3][5:10]

                # Check out date value
                checkOutDate = i[6]

                if checkOutDate is None:
                    checkOutDate = "-"

                # Customer Id
                customerId = Label(
                    frame12,
                    text=i[0],
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerId.grid(row=j, column=0, sticky=NSEW)

                # Customer Name
                customerName = Label(
                    frame12,
                    text=i[1],
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerName.grid(row=j, column=1, sticky=NSEW)

                # Customer Aadhaar
                customerAadhaar = Label(
                    frame12,
                    text=aadhaarNumber,
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerAadhaar.grid(row=j, column=2, sticky=NSEW)

                # Mobile number
                customerMobile = Label(
                    frame12,
                    text=mobileNUmber,
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerMobile.grid(row=j, column=3, sticky=NSEW)

                # Room Type
                customerRoom = Label(
                    frame12,
                    text=customerRoom,
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerRoom.grid(row=j, column=4, sticky=NSEW)

                # Check in Date
                customerCheckInDate = Label(
                    frame12,
                    text=i[5],
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerCheckInDate.grid(row=j, column=5, sticky=NSEW)

                # Check in Date
                customerCheckOutDate = Label(
                    frame12,
                    text=str(checkOutDate),
                    relief=GROOVE,
                    padx=10,
                    pady=8,
                    font=("Ariel", 8))
                customerCheckOutDate.grid(row=j, column=6, sticky=NSEW)

                j += 1

                # Dark Mode
                if darkModeFlag:
                    customerId.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerName.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerAadhaar.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerMobile.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerRoom.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerCheckInDate.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                    customerCheckOutDate.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

            # Save CSV File on desktop
            def saveCSV():
                rawData = queries.retrieveAllData()
                finalData = []

                for data in rawData:

                    roomType = ""

                    # Retrieving room name using roomId
                    if data[4] == "DA":
                        roomType = "Deluxe"
                    elif data[4] == "NA":
                        roomType = "Normal"
                    elif data[4] == "NN":
                        roomType = "Normal"
                    elif data[4] == "SA":
                        roomType = "Suite"

                    customerData = []

                    customerData += [data[0]] + [data[1]] + ["'" + str(data[2])] + [data[3]] + \
                                    [roomType] + [str(data[5])] + [str(data[6])] + [data[7]] + [str(data[8])]

                    finalData += [customerData]

                generateCSV.generateCSV(finalData, getDate())
                successMsgBox("CSV", "File saved on desktop")

            # Save Button
            saveCSVButton = Button(frame12, text="Save CSV", command=saveCSV)
            saveCSVButton.grid(row=j + 1, column=3, pady=(30, 0), sticky=NSEW)

            # Dark Mode
            if darkModeFlag:
                customerIdHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerNameHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerAadhaarHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerMobileHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                customerRoomHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                CheckInDateHeading.configure(bg="#404040", fg="#DADADA", bd=0)
                CheckOutDateHeading.configure(bg="#404040", fg="#DADADA", bd=0)

                saveCSVButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)

        # Dark Mode
        if darkModeFlag:
            myCanvas.configure(bg="#2A2A2A", bd=0, highlightthickness=0)
            frame12.configure(bg="#2A2A2A", bd=0, padx=5)

            """style = ttk.Style()
            print(style.theme_names())
            print(style.element_options("Vertical.TScrollbar.trough"))
            style.theme_use('alt')
            style.configure("Vertical.TScrollbar", troughcolor="#505050")"""


# To add a room to the database
def addRoom():
    global_.updateStatus("Expanding? Gud :)")

    # Changing the Title of the window
    root.title("Hotel Man - Add Room")

    # Clearing the frame
    clearFrame(frame1)

    # Room Id Label
    roomIdLab = Label(frame1, text="Select Room Type:")
    roomIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # Room Id Option Menu
    room = StringVar()  # Tkinter string data type

    # List of room options
    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]

    # Setting default value for Room Selector
    room.set("Select")

    # AC Available Label
    ACLab = Label(frame1, text="AC: ")
    ACLab.grid(row=0, column=2, pady=25, padx=15, sticky=E)

    # AC Value Label
    ACLab2 = Label(frame1)
    ACLab2.grid(row=0, column=3, padx=(5, 0), pady=25, sticky=W)
    ACLab2.configure(text="No Info")

    # To check if AC is available
    def updateAC(event):
        if room.get() == "Normal (No AC)":
            ac = "No"
        elif room.get() == "Select":
            ac = "No Info"
        else:
            ac = "Yes"
        ACLab2.configure(text=ac)

        print(event)

    # Options menu to select the room and update AC status
    roomIdSelector = OptionMenu(frame1, room, *roomNames, command=updateAC)
    roomIdSelector.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)

    # Quantity of rooms Label
    qtyRoomsLab = Label(frame1, text="How many rooms are available? :")
    qtyRoomsLab.grid(row=1, column=0, pady=25, padx=5, sticky=E)

    # Quantity of Rooms Scale
    qtyRooms = Scale(frame1, from_=1, to=10, orient=HORIZONTAL)
    qtyRooms.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)

    # Room Rate Label
    roomRateLab = Label(frame1, text="Rate({}): ".format("\u20B9"))  # u"\u20B9" -> rupees symbol
    roomRateLab.grid(row=1, column=2, pady=25, padx=15, sticky=E)

    # Room Rate Entry Box
    roomRate = Entry(frame1, width=6, justify=CENTER)
    roomRate.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

    # To send query to add room to database
    def submitRoomAdd():

        # If a room is not selected
        if room.get() == "Select":

            global_.updateStatus("Select A Room Type")

            # Displaying the error
            errorMsgBox("Rooms", "Please Select a Room Type")

        elif roomRate.get() == "":

            global_.updateStatus("Enter Rate")

            # Displaying the error
            errorMsgBox("Rooms", "Rate not Entered")

        # If a room is selected
        else:
            roomId = ""

            # Converting room type to appropriate RoomId
            if room.get() == "Normal (AC)":
                roomId = "NA"
            elif room.get() == "Normal (No AC)":
                roomId = "NN"
            elif room.get() == "Deluxe":
                roomId = "DA"
            elif room.get() == "Suite":
                roomId = "SA"

            global_.updateStatus("Adding...")

            # Running the MySQL query
            res = queries.addRoom(
                roomId,
                ACLab2.cget("text"),
                qtyRooms.get(),
                roomRate.get()
            )

            # res == 1 -> Room added
            if res == 1:

                global_.updateStatus("Room Added")

                # Displaying the success message
                successMsgBox("Room Added", "Room Added Successfully")

            # res == 0 -> Error
            elif res == 0:

                global_.updateStatus("Room Exists, Try Updating it")

                # Displaying the error message
                errorMsgBox("Failed", "Room Already Exists")

            addRoom()

    # Submit Button
    submitCustomerDetails = Button(frame1, text="Submit", width=15, command=submitRoomAdd)
    submitCustomerDetails.grid(row=2, column=1, columnspan=2, pady=15)

    # Key bind to submit on pressing return
    def returnPressed(event):
        submitRoomAdd()
        print(event)

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        roomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomIdSelector.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=FLAT, borderwidth=3)
        roomIdSelector["menu"].config(bg="#555555", fg="#DADADA", bd=0)

        ACLab.configure(bg="#2A2A2A", fg="#DADADA")
        ACLab2.configure(bg="#2A2A2A", fg="#DADADA")

        qtyRoomsLab.configure(bg="#2A2A2A", fg="#DADADA", padx=5)
        qtyRooms.configure(bg="#2A2A2A", fg="#DADADA", highlightthickness=0, troughcolor="#505050", bd=0)

        roomRateLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomRate.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

        submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# To update room qty/rate
def updateRoom():
    global_.updateStatus("Update Room")

    # Changing the Title of the window
    root.title("Hotel Man - Update Room Details")

    # Clearing the frame
    clearFrame(frame1)

    # Room Id Label
    roomIdLab = Label(frame1, text="Select Room Type:")
    roomIdLab.grid(row=0, column=0, pady=30, padx=5, sticky=E)

    # Room Id Option Menu
    room = StringVar()  # Tkinter string data type

    # List of room options
    roomNames = [
        "Normal (AC)",
        "Normal (No AC)",
        "Deluxe",
        "Suite"
    ]

    # Setting default value for Room Selector
    room.set("Select")

    # Options menu to select the room
    roomIdSelector = OptionMenu(frame1, room, *roomNames)
    roomIdSelector.grid(row=0, column=1, padx=(15, 30), pady=25, sticky=W)

    # To search by roomId if room exists in database
    def searchRoom():

        # Checking if room is not selected
        if room.get() == "Select":

            global_.updateStatus("Please Select a room from the Drop-Down")

            # Displaying the error
            errorMsgBox("Room Update", "Please Select a Room Type")

        # If a room is selected
        else:

            # Setting the RoomId from room name
            if room.get() == "Normal (AC)":
                updateRoomId = "NA"
            elif room.get() == "Normal (No AC)":
                updateRoomId = "NN"
            elif room.get() == "Deluxe":
                updateRoomId = "DA"
            else:
                updateRoomId = "SA"

            # Running the query to update
            res = queries.searchRoom(updateRoomId)

            # If there was some error
            if res == 0:

                global_.updateStatus("Room Doesn't Exist. Try Adding it First")

                # Displaying error message
                errorMsgBox("Room", "Room Not Found")

            # No Error
            elif res == 1:

                global_.updateStatus("Room Found")

                # Get qty and rate of selected room
                qty, rate = queries.selectRoom(updateRoomId)

                # Quantity of rooms Label
                qtyRoomsLab = Label(frame1, text="How many rooms are available?: ")
                qtyRoomsLab.grid(row=1, column=0, pady=30, padx=5, sticky=E)

                # Quantity of Rooms Selector
                qtyRooms = Scale(frame1, from_=1, to=10, orient=HORIZONTAL)
                qtyRooms.set(qty)  # Inserting the already existing value
                qtyRooms.grid(row=1, column=1, padx=(15, 30), pady=25, sticky=W)

                # Room Rate Label
                roomRateLab = Label(frame1, text="Rate({}): ".format("\u20B9"))  # "\u20B9" -> rupees symbol
                roomRateLab.grid(row=1, column=2, pady=25, padx=(0, 5), sticky=E)

                # Room Rate Entry Box
                roomRate = Entry(frame1, width=6, justify=CENTER)
                roomRate.insert(END, str(rate))  # Inserting the already existing value
                roomRate.grid(row=1, column=3, padx=(15, 0), pady=25, sticky=W)

                # To send query to update room
                def submitRoomUpdate():

                    # Running query to update the room
                    queries.updateRoom(
                        updateRoomId,
                        qtyRooms.get(),
                        roomRate.get()
                    )

                    global_.updateStatus("Room Updated")

                    # Showing the success message
                    successMsgBox("Room Update", "Room Updated Successfully")

                    # Running the function again
                    updateRoom()

                # Update Button
                submitCustomerDetails = Button(frame1, text="Submit", width=15, command=submitRoomUpdate)
                submitCustomerDetails.grid(row=2, column=1, columnspan=2, pady=15, padx=(15, 0))

                # Key bind to submit on pressing return
                def returnPressedInner(event):
                    submitRoomUpdate()
                    print(event)

                for j in frame1.winfo_children():
                    j.bind("<Return>", returnPressedInner)

                # Dark Mode
                if darkModeFlag:
                    qtyRoomsLab.configure(bg="#2A2A2A", fg="#DADADA", padx=5)
                    qtyRooms.configure(bg="#2A2A2A", fg="#DADADA", highlightthickness=0, bd=0, troughcolor="#505050")

                    roomRateLab.configure(bg="#2A2A2A", fg="#DADADA")
                    roomRate.configure(bg="#505050", fg="#DADADA", relief=FLAT, borderwidth=3)

                    submitCustomerDetails.configure(bg="#505050", fg="#DADADA", bd=0,
                                                    highlightthickness=0, pady=5, padx=8)

    # Search Button
    submitButton = Button(frame1, text="Search", command=searchRoom)
    submitButton.grid(row=0, column=2, pady=25, sticky=W)

    # Key bind to submit on pressing return
    def returnPressed(event):
        searchRoom()
        print(event)

    for i in frame1.winfo_children():
        i.bind("<Return>", returnPressed)

    # Dark Mode
    if darkModeFlag:
        roomIdLab.configure(bg="#2A2A2A", fg="#DADADA")
        roomIdSelector.configure(bg="#505050", fg="#DADADA", highlightthickness=0, relief=FLAT, borderwidth=3)
        roomIdSelector["menu"].config(bg="#555555", fg="#DADADA")

        submitButton.configure(bg="#505050", fg="#DADADA", bd=0, highlightthickness=0, pady=5, padx=8)


# To display all the rooms
def showRooms():
    global_.updateStatus("Showing All Rooms")

    # Changing the Title of the window
    root.title("Hotel Man - Show All Rooms")

    # Clearing the frame
    clearFrame(frame1)

    # Tuple of tuples containing info of all rooms
    rooms = queries.showRooms()

    # If tuple is empty, no rooms found
    if not rooms:

        # Displaying the error
        errorMsgBox("Search", "No Rooms Found")
        addRoom()

    # Rooms Found, Displaying the table
    else:

        # Headings
        # Id
        roomHeading = Label(
            frame1,
            text="Room Type",
            bg="#C0C0C0",
            relief=GROOVE,
            padx=20,
            pady=8)
        roomHeading.grid(row=0, column=0, sticky=NSEW, padx=(125, 0), pady=(100, 0))

        # AC
        acHeading = Label(
            frame1,
            text="AC Room",
            bg="#C0C0C0",
            relief=GROOVE,
            padx=20,
            pady=8)
        acHeading.grid(row=0, column=1, stick=NSEW, pady=(100, 0))

        # Quantity
        qtyHeading = Label(
            frame1,
            text="Vacant",
            bg="#C0C0C0",
            relief=GROOVE,
            padx=20,
            pady=8)
        qtyHeading.grid(row=0, column=2, sticky=NSEW, pady=(100, 0))

        # Rate
        rateHeading = Label(
            frame1,
            text="Rate",
            bg="#C0C0C0",
            relief=GROOVE,
            padx=20,
            pady=8)
        rateHeading.grid(row=0, column=3, sticky=NSEW, pady=(100, 0))

        # j is row number
        j = 1

        # Loop to display all the room's information
        for i in rooms:

            showRoomId = ""
            # Retrieving room name using roomId
            if i[0] == "DA":
                showRoomId = "Deluxe"
            elif i[0] == "NA":
                showRoomId = "Normal"
            elif i[0] == "NN":
                showRoomId = "Normal"
            elif i[0] == "SA":
                showRoomId = "Suite"

            acStatus = ""

            # Retrieving AC Status
            if i[1] == "y":
                acStatus = "Yes"
            elif i[1] == "n":
                acStatus = "No"

            # Quantity of room vacant
            qty = i[2]

            # Rate of room
            rate = i[3]

            # Room Id
            idRoom = Label(
                frame1,
                text=showRoomId,
                relief=GROOVE,
                padx=20,
                pady=8)
            idRoom.grid(row=j, column=0, sticky=NSEW, padx=(125, 0))

            # AC room?
            acRoom = Label(
                frame1,
                text=acStatus,
                relief=GROOVE,
                padx=20,
                pady=8)
            acRoom.grid(row=j, column=1, sticky=NSEW)

            # Quantity of rooms empty
            qtyRoom = Label(
                frame1,
                text=str(qty),
                relief=GROOVE,
                padx=20,
                pady=8)
            qtyRoom.grid(row=j, column=2, sticky=NSEW)

            # Rate of each room
            rateRoom = Label(
                frame1,
                text="\u20B9" + str(rate),
                relief=GROOVE,
                padx=20,
                pady=8)
            rateRoom.grid(row=j, column=3, sticky=NSEW)  # "\u20B9" -> rupees symbol

            j += 1

            if darkModeFlag:
                idRoom.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                acRoom.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                qtyRoom.configure(bg="#4F4F4F", fg="#DADADA", bd=0)
                rateRoom.configure(bg="#4F4F4F", fg="#DADADA", bd=0)

        if darkModeFlag:
            roomHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            acHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            qtyHeading.configure(bg="#404040", fg="#DADADA", bd=0)
            rateHeading.configure(bg="#404040", fg="#DADADA", bd=0)


# To be run when clicked submit on sign in screen
def submitted():
    # To use throughout the function
    global frame1

    # If sign in successful
    if global_.condition == 1:

        global_.updateStatus("Connection Successful")

        imgLabel.destroy()
        logInButton.destroy()
        darkModeButton.destroy()

        # To set the size of the main screen
        root.geometry("1050x700")
        img = PhotoImage(file="Assets/LogoBlackNameSmall.png")
        imgDark = PhotoImage(file="Assets/LogoWhiteNameSmall.png")

        # Placing all the options and frames
        workingWindow = Frame(root, bd=0)
        workingWindow.pack(fill=X, ipadx=20)

        # Left (Navigation) Pane
        frame0 = LabelFrame(workingWindow, pady=50, bd=0)
        frame0.pack(side=LEFT, padx=(10, 10), pady=0)

        # Display the logo on top
        my_canvas = Canvas(frame0)
        my_canvas.create_image(0, 0, anchor=NW, image=img)
        my_canvas.place(x=15, y=0)

        # Customer Options Frame
        frame01 = LabelFrame(frame0, text="Customer", pady=10, padx=10)
        frame01.grid(row=1, column=0, pady=(100, 30), padx=10, columnspan=2)

        # Button to CheckIn
        button011 = Button(frame01, text="Check In", width=15, command=checkIn)
        button011.pack(pady=3)

        # Button to Update record
        button012 = Button(frame01, text="Update", width=15, command=updateCustomer)
        button012.pack(pady=3)

        # Button to Check Out
        button013 = Button(frame01, text="Check Out", width=15, command=checkOut)
        button013.pack(pady=3)

        # Button to Search for a Customer
        button014 = Button(frame01, text="Find", width=15, command=findCustomer)
        button014.pack(pady=3)

        # Button to show all customers present in the hotel
        button015 = Button(frame01, text="Show All", width=15, command=showCustomers)
        button015.pack(pady=3)

        # Room Options
        frame02 = LabelFrame(frame0, text="Rooms", pady=10, padx=10)

        if global_.accessLevel == "User":
            # For better placement
            frame01.grid(row=0, column=0, pady=130, padx=10, columnspan=2)

        # To display the rooms options
        elif global_.accessLevel == "Admin":

            # Room Options
            frame02.grid(row=2, column=0, pady=30, padx=10, columnspan=2)

            # Button to add rooms
            button021 = Button(frame02, text="Add", width=15, command=addRoom)
            button021.pack(pady=3)

            # Button to Update room details
            button022 = Button(frame02, text="Update", width=15, command=updateRoom)
            button022.pack(pady=3)

            # Button to Show all available rooms
            button023 = Button(frame02, text="Show All", width=15, command=showRooms)
            button023.pack(pady=3)

        # Function to sign out
        def signOut():

            # Sign out of MySQL
            queries.endConn()

            # To close the current window and the logo canvas
            root.destroy()

            # To start the file again
            os.system("python main.py")

        # Display the sign out button
        signOutButton = Button(frame0, text="Sign Out", command=signOut, width=10)
        signOutButton.grid(row=3, column=0, padx=(10, 5))

        # Display the exit button
        exitButton = Button(frame0, text="Exit", command=exitApplication, width=10)
        exitButton.grid(row=3, column=1, padx=(5, 10))

        # Right Pane
        frame1 = LabelFrame(workingWindow, pady=150, padx=50, bd=0)
        frame1.pack(padx=10, side=LEFT, fill=BOTH, expand=True)

        # Dark Mode
        if darkModeFlag:
            workingWindow.configure(bg="#2A2A2A")
            frame0.configure(bg="#2A2A2A")

            my_canvas.delete("all")
            my_canvas.create_image(0, 0, anchor=NW, image=imgDark)
            my_canvas.configure(bg="#2A2A2A", bd=0, highlightthickness=0)

            frame01.configure(bg="#2A2A2A", fg="#DADADA")
            for i in frame01.winfo_children():
                i.configure(bg="#505050", fg="#DADADA", bd=0, pady=3)

            frame02.configure(bg="#2A2A2A", fg="#DADADA")
            for i in frame02.winfo_children():
                i.configure(bg="#505050", fg="#DADADA", bd=0, pady=3)

            signOutButton.configure(bg="#505050", fg="#DADADA", bd=0, pady=5)
            exitButton.configure(bg="#505050", fg="#DADADA", bd=0, pady=5)

            frame1.configure(bg="#2A2A2A", fg="#DADADA")

        root.mainloop()  # Canvas wont work without mainloop

    # If connection to database was failed
    else:

        global_.updateStatus("Cannot Connect, Try Again")

        # Display the error Message
        errorMsgBox("SignIn Error", "Failed to log in, try again")

        # To start log in process just by pressing the return(enter) key
        def returnPressedOuter_(event):
            signIn()
            print(event)

        root.bind("<Return>", returnPressedOuter_)


# To display sign in screen
def signIn():

    global_.updateStatus("Connecting...")

    # To stop getting the sign in screen everytime user presses enter(return) key
    root.unbind("<Return>")

    # To quit the program when escape key is pressed
    def escapePressed(event):
        exitApplication()
        print(event)

    root.bind("<Escape>", escapePressed)

    global_.accessLevel = "User"

    # Tkinter new screen
    signInScreen = Toplevel()

    # Title for new screen
    signInScreen.title("Sign in")

    # Sign in screen icon
    signInScreen.iconbitmap("./Assets/LogoBlack.ico")

    # Frame for username
    userNameFrame = Frame(signInScreen, pady=5)
    userNameFrame.pack()

    # Enter username Label
    unameLabel = Label(userNameFrame, text="Enter Username: ")
    unameLabel.grid(row=0, column=0)

    # Username Entry Field
    uname = Entry(userNameFrame, justify=CENTER)
    uname.grid(row=0, column=1)
    uname.focus_set()

    # Frame for password
    passwordFrame = Frame(signInScreen, pady=5)
    passwordFrame.pack()

    # Enter Password Label
    pWordLabel = Label(passwordFrame, text="Enter Password: ")
    pWordLabel.grid(row=0, column=0)

    # Password Entry Field
    pWord = Entry(passwordFrame, show="*", justify=CENTER)
    pWord.grid(row=0, column=1)

    # To Toggle password View
    def togglePasswordView():
        if pWord.cget("show") == "*":
            pWord.configure(show="")
        else:
            pWord.configure(show="*")

    # Toggle Password View
    togglePassword = Button(signInScreen, text="Toggle Password View", command=togglePasswordView)
    togglePassword.pack(pady=(10, 0))

    # Function for Button to sign in
    def submit():

        # Get and store the username the user entered
        global_.username = uname.get()

        # Get and store the password the user entered
        global_.password = pWord.get()

        # Initialize the database
        sqlInit.createDbAndTables()

        # Closing the sign in screen automatically
        signInScreen.destroy()

        # Displaying all the options(checkIn, checkOut...)
        submitted()

    # SignIn Button
    but = Button(signInScreen, text="Sign In", command=submit)
    but.pack(pady=(10, 0))

    # Vertical Padding of the popup screen
    signInScreen.configure(pady=50)

    # Dimensions of the SignIn screen
    signInScreen.geometry("500x230")

    # To automatically focus on the pop up screen
    signInScreen.focus_force()

    # To change the mode to admin mode
    def enterAdmin(event):
        global_.accessLevel = "Admin"
        print(event.char)
        signInScreen.title("Sign in (Admin)")

    # To enter the admin log in mode when user presses alt+8
    signInScreen.bind("<Alt-KeyPress-8>", enterAdmin)

    # Key bind to submit on pressing return
    def returnPressed(event):
        submit()
        print(event)

    signInScreen.bind("<Return>", returnPressed)

    if darkModeFlag:

        # Dark
        signInScreen.configure(bg="#333333")
        signInScreen.iconbitmap("./Assets/LogoColor.ico")
        signInScreen.geometry("500x250")

        userNameFrame.configure(bg="#333333")
        unameLabel.configure(bg="#333333", fg="#DADADA")

        passwordFrame.configure(bg="#333333")
        pWordLabel.configure(bg="#333333", fg="#DADADA")

        uname.configure(bg="#5D5D5D", fg="#DADADA", relief=FLAT, borderwidth=1)
        pWord.configure(bg="#5D5D5D", fg="#DADADA", relief=FLAT, borderwidth=1)

        togglePassword.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)
        but.configure(bd=0, bg="#555555", fg="#DADADA", padx=8, pady=5)


# Logo image
logoImgDark = ImageTk.PhotoImage(Image.open("./Assets/LogoWhiteName.png"))
logoImg = ImageTk.PhotoImage(Image.open("./Assets/LogoBlackName.png"))
imgLabel = Label(image=logoImg)
imgLabel.pack()

# Button to initiate log in and display sign in screen
logInButton = Button(root, text="Log In", command=signIn)
logInButton.pack(pady=(20, 0))


# Enable Dark Mode
def darkMode():

    global darkModeFlag
    darkModeFlag = True

    root.configure(bg="#2A2A2A")
    root.iconbitmap("./Assets/LogoColor.ico")

    imgLabel.configure(bg="#2A2A2A", image=logoImgDark)
    logInButton.configure(bd=0, bg="#505050", fg="#DADADA", padx=8, pady=5)
    global_.statusBar.configure(bg="#343434", fg="#DADADA", bd=0)

    darkModeButton.configure(bd=0, bg="#505050", fg="#DADADA", padx=8, pady=5)
    darkModeButton.configure(state=DISABLED)


# Button to enable dark mode
darkModeButton = Button(root, text="Dark Mode", command=darkMode)
darkModeButton.pack(pady=(20, 10))

# Status Bar
global_.statusBar = Label(root, text="Welcome", relief=SUNKEN, anchor=E, padx=10, height=2)


global_.statusBar.pack(side=BOTTOM, fill=X)
# To start log in process just by pressing the return(enter) key


def returnPressedOuter(event):
    signIn()
    print(event)


root.bind("<Return>", returnPressedOuter)


# Start the main screen
root.mainloop()
