from twilio.rest import Client
from flaskr.config import *
from flask import session
import random


def send_confirmation_code(phone_number):
    verification_code = generate_code()
    send_sms(phone_number, verification_code)
    session['verification_code'] = verification_code
    return verification_code


def generate_code():
    return str(random.randrange(1000, 9999))


def send_sms(phone_number, body):
    account_sid = "AC58b95906d06caeb274aa775ef0eb090f",
    auth_token = "9bdfb75b3967b8ff5d300f66bd44f21e",
    twilio_number = "+15677042726",
    client = Client(account_sid, auth_token)
    client.api.messages.create(phone_number,
                           from_=twilio_number,
                           body=body)