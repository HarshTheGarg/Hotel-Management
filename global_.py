"""
File to store global variables used in all the files
"""

# User Access
global accessLevel

# Sign In Username
global username

# Sign In Password
global password

# For Status Bar
global status

# Status Bar
global statusBar

# MySQL Connection
global conn

# MySQL Cursor
global cur

# Rooms Table name
global tbRooms

# Customers Table name
global tbCustomers

# All Customers Table name
global tbAllCustomers

# Condition Checker
# 1: Ok, 0: Not Ok
global condition



# Update the status Bar
def updateStatus(text):
    statusBar.configure(text=text)
