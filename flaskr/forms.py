from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators
from wtforms.validators import DataRequired, ValidationError
import phonenumbers

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(),  validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Repeat Password')
    phone_number = StringField('phone_number', validators=[DataRequired()])

    def validate_phone(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        

class LoginForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])




class OtpLoginForm(FlaskForm):
    phone_number = StringField('phone_number', validators=[DataRequired()])

class ConfirmOtpForm(FlaskForm):
    phone_otp = StringField('phone_otp', validators=[DataRequired()])


