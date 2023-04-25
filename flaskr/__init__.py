import os
import json
from . import auth, views
import sentry_sdk
from flask import Flask, render_template_string
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_mail import *  
from flaskr.email import mail
from flask_security import SQLAlchemyUserDatastore, Security, auth_required
from dotenv import load_dotenv


def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.run()



    sentry_sdk.init(
        dsn=os.getenv("dsn"),
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
    from logging.config import dictConfig


    load_dotenv()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_PORT = os.getenv('MAIL_PORT'),
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=False),
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', default=True),
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER'),
    mail.init_app(app)


    app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    from flaskr.models import db, User, Role
    from flask_migrate import Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email',
    'authenticator', 'sms']  # 'sms' also valid but requires an sms provider
    app.config['SECURITY_TWO_FACTOR'] = True
    app.config["SECURITY_TWO_FACTOR_REQUIRED"]=True
    rescue_email = os.getenv('SECURITY_TWO_FACTOR_RESCUE_MAIL')
    app.config['SECURITY_TWO_FACTOR_RESCUE_MAIL'] = rescue_email
    app.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = False
    
    # Generate a good totp secret using: passlib.totp.generate_secret()
    app.config['SECURITY_TOTP_SECRETS'] = {"1": "TjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu9B"}
    app.config['SECURITY_TOTP_ISSUER'] = "flaskr"
    

   
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")
    # app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


    
    app.config["SECURITY_SMS_SERVICE"] = "Twilio"
    security_config = os.getenv('SECURITY_SMS_SERVICE_CONFIG')
    app.config['SECURITY_SMS_SERVICE_CONFIG'] = json.loads(security_config)
    app.config["SECURITY_CHANGE_PASSWORD_TEMPLATE"]=True
    app.config["SECURITY_EMAIL_SUBJECT_CONFIRM"]="Please confirm your email"
    app.config["SECURITY_AUTO_LOGIN_AFTER_CONFIRM"]=True
    app.config["SECURITY_LOGIN_WITHOUT_CONFIRMATION"]=False
    app.config['SECURITY_SEND_PASSWORD_RESET_EMAIL']=True
    app.config["SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL"]=True
    app.config["SECURITY_EMAIL_SUBJECT_PASSWORD_RESET"]="Password reset instructions"
    app.config["SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE"]="Your password has been reset"
    # app.config["SECURITY_LOGIN_URL"] ="/user/sigin"
    # app.config["SECURITY_REGISTER_URL"]="/user/signup"
    app.config["SECURITY_CHANGE_PASSWORD_TEMPLATE"]="security/change_password.html"
    app.config["SECURITY_RESET_PASSWORD_TEMPLATE"]="security/reset_password.html"
    app.config["SECURITY_REGISTERABLE"]=True
    app.config["SECURITY_TWO_FACTOR_AUTHENTICATOR_VALIDITY"]=100
    app.config["SECURITY_CHANGEABLE"]=True
    app.config["SECURITY_CHANGE_URL"]="/change"
    app.config["SECURITY_RECOVERABLE"]=True
    app.config["SECURITY_RESET_URL"]="/reset"
    app.config["SECURITY_FORGOT_PASSWORD_TEMPLATE"]="security/forgot_password.html"
    app.config["SECURITY_TWO_FACTOR_VERIFY_CODE_TEMPLATE"]="security/two_factor_verify_code.html"
    app.config["SECURITY_TWO_FACTOR_SETUP_TEMPLATE"]="security/two_factor_setup.html"
    app.config["SECURITY_TWO_FACTOR_SETUP_URL"]="/tf-setup"
    app.config["SECURITY_TWO_FACTOR_TOKEN_VALIDATION_URL"]="/tf-validate"
    app.config["SECURITY_REGISTER_URL"]="/register"
    app.config["SECURITY_LOGOUT_URL"]="/logout"
    app.config["SECURITY_SEND_REGISTER_EMAIL"]=True
    app.config["SECURITY_EMAIL_SUBJECT_REGISTER"]="welcome"
    app.config["SECURITY_REGISTER_USER_TEMPLATE"]="security/register_user.html"


    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)


    @app.route('/')
    @auth_required()
    def home():
        return render_template_string("Hello {{ current_user.email }}")
    # one time setup
    with app.app_context():
        # Create a user to test with
        db.create_all()
        if not app.security.datastore.find_user(email='tests@me.com'):
            app.security.datastore.create_user(email='tests@me.com', password='password')
        db.session.commit()

    @app.route('/debug-sentry')
    def trigger_error():
        division_by_zero = 1 / 0



    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)

    return app


