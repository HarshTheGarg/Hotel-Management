"""
Script to send an OTP to the customer
"""

from twilio.rest import Client  # API Client which sends the sms
# pip install twilio

# To use environment variables
import os

sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


def sendOTP(otp: int, number: str) -> None:
    """
    Send the otp to the customer's mobile number to verify him/her
    :param otp: Otp to be sent
    :param number: Number on which the otp is to be sent
    """

    client = Client(sid, auth_token)
    # Creating the twilio client object

    client.messages.create(body=f"\nYour OTP is: {otp}\n"
                                f"Please do not share with anyone",
                           from_="+12565790887",
                           to=f"+91{number}"
                           )
    # Sending the message

    # Body is the content of the message. A text is prepended stating that we are using the free version of twilio.
    # This can be removed by buying the full version

    # from_ specifies the number which was generated by the twilio website for our account.
    # We are not receiving messages from this number as we are using the free trial version of the api

    # to specifies the number to which the message is to be sent


def sendWelcomeSMS(
        customerName: str, customerId: str, roomId: str, rate: int, tax: float, number: str
) -> None:
    """
    Send the welcome SMS to the customer
    """

    if roomId == "DA":
        roomType = "Deluxe"
    elif roomId == "NA":
        roomType = "Normal (AC)"
    elif roomId == "NN":
        roomType = "Normal (No AC)"
    else:
        roomType = "Suite"

    client = Client(sid, auth_token)
    # Creating the twilio client object

    client.messages.create(body=f"\nWelcome {customerName} \n"
                                f"Your CustomerId is {customerId} "
                                f"and you are staying in a {roomType} room\n"
                                f"(Rate -> \u20B9{rate} Tax -> {tax}%)",
                           from_="+12565790887",
                           to=f"+91{number}"
                           )
    # Sending the message

    # Body is the content of the message. A text is prepended stating that we are using the free version of twilio.
    # This can be removed by buying the full version

    # from_ specifies the number which was generated by the twilio website for our account.
    # We are not receiving messages from this number as we are using the free trial version of the api

    # to specifies the number to which the message is to be sent


def sendByeSMS(name: str, price: int, tax: float, number: str) -> None:
    """
    Send the customer the total price to be paid and a good bye message
    """

    priceFinal = round(int(price) * (1 + float(tax) / 100), 2)
    # Final price to be paid

    client = Client(sid, auth_token)
    # Creating the twilio client object

    client.messages.create(body=f"\nHello {name}!\n"
                                f"Please pay \u20B9 {round(priceFinal, 0)} at the reception\n"
                                f"You can ask for a copy of the receipt at the reception.\n"
                                f"Thank you, Please visit again",
                           from_="+12565790887",
                           to=f"+91{number}"
                           )
    # Sending the message

    # Body is the content of the message. A text is prepended stating that we are using the free version of twilio.
    # This can be removed by buying the full version

    # from_ specifies the number which was generated by the twilio website for our account.
    # We are not receiving messages from this number as we are using the free trial version of the api

    # to specifies the number to which the message is to be sent
