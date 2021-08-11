"""
Generates and saves CSV file containing all the customers data on desktop
"""

# To Create the Directory
import os

import csv


# To generate CSV file
def generateCSV(data, date):

    # Create the folder on desktop
    desktop_path = os.environ["HOMEPATH"] + "\\Desktop"
    if os.path.exists("C:" + desktop_path + "\\HotelMan"):
        pass
    else:
        os.mkdir("C:" + desktop_path + "\\HotelMan")

    fields = ["Customer ID", "Name", "Aadhaar", "Mobile", "Room Type", "Check In Date",
              "Check Out Date", "Check In Status", "Room Rate"]

    with open("C:" + desktop_path + f"\\HotelMan\\HotelMan_{date.year}_{date.month}_{date.day}.csv",
              "w", newline=""
              ) as file:
        csv_w = csv.writer(file)
        csv_w.writerow(fields)
        csv_w.writerows(data)

