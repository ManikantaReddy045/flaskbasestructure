import os
from . import auth, blog, views
import sentry_sdk
from flask import Flask, render_template_string
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_mail import *  
from flaskr.email import mail
from flask_security import SQLAlchemyUserDatastore, Security, auth_required

def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.run()



    sentry_sdk.init(
        dsn="https://2892a33d6f2b492fa984b4e0d4d011c0@o4504966018826240.ingest.sentry.io/4505012076478464",
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
    from logging.config import dictConfig



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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    app.config.update(

        MAIL_DEFAULT_SENDER = "reddymani707@gmail.com",
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_DEBUG = False,
        MAIL_USERNAME = "reddymani707@gmail.com",
        MAIL_PASSWORD = "xonsywdpxauzmizc",
    )
    mail.init_app(app)
    
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)

    app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres:Mani%4012345@localhost:5432/flask"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    from flaskr.models import db, User, Role
    from flask_migrate import Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email',
    'authenticator', 'sms']  # 'sms' also valid but requires an sms provider
    app.config['SECURITY_TWO_FACTOR'] = True
    app.config["SECURITY_TWO_FACTOR_REQUIRED"]=True
    app.config['SECURITY_TWO_FACTOR_RESCUE_MAIL'] = "reddymani707@gmail.com"

    app.config['SECURITY_TWO_FACTOR_ALWAYS_VALIDATE'] = False
    

    # Generate a good totp secret using: passlib.totp.generate_secret()
    app.config['SECURITY_TOTP_SECRETS'] = {"1": "TjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu9B"}
    app.config['SECURITY_TOTP_ISSUER'] = "flaskr"

   
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')

    
    app.config["SECURITY_SMS_SERVICE"] = "Twilio"
    app.config["SECURITY_SMS_SERVICE_CONFIG"] = {'ACCOUNT_SID':"AC58b95906d06caeb274aa775ef0eb090f", 'AUTH_TOKEN': "9bdfb75b3967b8ff5d300f66bd44f21e", 'PHONE_NUMBER': "+15677042726"}
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


    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)

    return app


