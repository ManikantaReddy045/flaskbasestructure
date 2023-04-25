from flask_mail import Message
from flask import current_app
from flask_mail import Mail


mail = Mail()

MAIL_USERNAME ='reddymani707@gmail.com'

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=MAIL_USERNAME,
    )
    mail.send(msg)