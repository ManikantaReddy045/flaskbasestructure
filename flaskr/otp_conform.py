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
    account_sid = os.getenv("ACCOUNT_SID"),
    auth_token = os.getenv("AUTH_TOKEN"),
    twilio_number = os.getenv("PHONE_NUMBER"),
    client = Client(account_sid, auth_token)
    client.api.messages.create(phone_number,
                           from_=twilio_number,
                           body=body)