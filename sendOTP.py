"""
Script to send an OTP to the customer
"""

# pip install twilio
from twilio.rest import Client

# To use environment variables
import os


def sendSMS(otp, number):
    sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(sid, auth_token)

    client.messages.create(body="Your OTP is: {}\nPlease do not share with anyone".format(otp), from_="+12565790887",
                           to="+91{}".format(number))

