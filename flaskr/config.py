import os

basedir = os.path.abspath(os.path.dirname(__file__))

account_sid = "",
auth_token = "",
twilio_number = "",



# class Config:
# Mail Settings
MAIL_DEFAULT_SENDER = "reddymani707@gmail.com"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = "reddymani707@gmail.com"
MAIL_PASSWORD = "Mani@12345"

# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Mani%4012345@localhost:5432/userss"


POSTGRES_USER= 'postgres'
POSTGRES_PASSWORD= 'Mani@12345'
POSTGRES_DB= 'userss'
POSTGRES_HOST = 'localhost'

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mani%4012345@localhost:5432/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT="fkslkfsdlkfnsdfnsfd"
    SECRET_KEY="fdkjshfhjsdfdskfdsfdcbsjdkfdsdf"