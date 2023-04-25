import datetime
import random
from tokenize import generate_tokens
from flask.views import View
from flask import (
    Blueprint, flash, render_template, request, redirect, session, url_for
)
from flaskr import db
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.email import send_email
from flaskr.models import User
from flaskr.database import db_session,init_db
from flaskr.forms import RegistrationForm, LoginForm, OtpLoginForm, ConfirmOtpForm
from flaskr.otp_conform import send_confirmation_code
from flaskr.token import confirm_token, generate_token

bp = Blueprint("user", __name__, url_prefix='/user')




@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('user/home.html')



@bp.route('/signup', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate:
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(name = form.name.data, email = form.email.data,
                    password = hashed_password, phone_number = form.phone_number.data)
        if user:
            session['email'] = user.email
            token = generate_tokens(user.email)
            confirm_url = url_for("user.confirm_email", token=token, _external=True)
            html = render_template("user/confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            db_session.add(user)
            db_session.commit()
            flash("A confirmation email has been sent via email.", "success")
            return redirect(url_for('user.home'))
        else:
            flash("Please enter the correct details")
    return render_template('user/signup.html', form=form)



@bp.route("/confirm/<token>")
def confirm_email(token):
    print(token,'-----------')
    email = confirm_token(token)
    address= session['email']
    user = User.query.filter_by(email = address).first()
    if user.email == email:
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("user.sigin"))



@bp.route('/sigin', methods=('GET', 'POST'))
def sigin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(name=form.name.data).first()
        
        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user.password, form.password.data):
                session['logged_in'] = True
                session['email'] = user.email 
                session['name'] = user.name
                flash("You Loged in sucessful")
                # After successful login, redirecting to home page
                return redirect(url_for('user.home'))
            else:
                # if password is in correct , redirect to login page
                flash('Username or Password Incorrect', "Danger")
    # rendering login page
    return render_template('user/sigin.html', form = form)



    


@bp.route('/otplogin', methods=('GET', 'POST'))
def otplogin():
    form = OtpLoginForm(request.form)
    if request.method == 'POST' and form.validate:
        phone_number = User.query.filter_by(phone_number=form.phone_number.data).first()
        if phone_number is not None:
            phone_otp = generate_code()
            session['phone_otp'] = phone_otp
            print("Please Dont share Otp", phone_otp)
            return redirect(url_for('user.confirm_otp'))
        else:
            flash("Please enter the correct phoneNumber")  
    return render_template('user/generateotp.html', form = form)  

def generate_code():
    return str(random.randrange(1000, 9999))


@bp.route('/confirmotp', methods=('GET', 'POST'))
def confirm_otp(): 
    form = ConfirmOtpForm(request.form)
    if request.method == 'POST': 
        phone_otp = form.phone_otp.data 
        otp = session['phone_otp']  
        if phone_otp == otp:
            session['logged_in'] = True
            return redirect(url_for('user.home'))
        else:
            flash("You entered wrong otp")
    return render_template('user/confirm_otp.html', form = form)


@bp.route('/logout/')
def logout():
    # Removing data from session by setting logged_flag to False.
    session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('user.home'))

