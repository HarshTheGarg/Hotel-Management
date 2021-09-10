"""
Generate and saves CSV file containing all the customers data on desktop
"""

import os  # Create the Directory

import datetime  # To specify datatype

import csv  # Lib to create csv


# To generate CSV file
def generateCSV(data: list[list], date: datetime.date) -> None:
    """
    Generate CSV file and save in the HotelMan directory on desktop
    :param data:
    :param date:
    :rtype: None
    """
    # Create the folder on desktop
    desktop_path: str = os.environ["HOMEPATH"] + "\\Desktop"
    # Path to the desktop

    # Check if the directory already exists
    if os.path.exists("C:" + desktop_path + "\\HotelMan"):
        # Directory exists
        pass

    else:
        # Directory doesn't exist
        os.mkdir("C:" + desktop_path + "\\HotelMan")
        # Make the directory

    # Create the file
    fields: list = ["Customer ID", "Name", "Aadhaar", "Mobile", "Room Type", "Check In Date",
                    "Check Out Date", "Check In Status", "Room Rate", "Tax"]
    # All the headers to be added to the file

    with open("C:" + desktop_path + f"\\HotelMan\\HotelMan_{date.year}_{date.month}_{date.day}.csv",
              "w", newline=""
              ) as file:
        csv_w = csv.writer(file)
        # CSV writer option

        csv_w.writerow(fields)
        # Write the header row

        csv_w.writerows(data)
        # Write all the data
