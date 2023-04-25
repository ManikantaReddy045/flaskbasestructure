from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flaskr import db
from flask_security import UserMixin, RoleMixin, auth_required

db = SQLAlchemy()



# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(Integer, primary_key = True)
    name= db.Column(String(50), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), unique=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(String(120))
    phone_number = db.Column(String(120), unique=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=True)
    active = db.Column(db.Boolean())
    tf_phone_number = db.Column(db.String(128), nullable=True)
    tf_primary_method = db.Column(db.String(64), nullable=True)
    tf_totp_secret = db.Column(db.String(255), nullable=True)
    

    def __init__(self, name=None, email=None, password=None, phone_number=None, roles=None, fs_uniquifier=None, active = None,
                tf_phone_number=None,  tf_primary_method=None, tf_totp_secret=None, confirmed_at=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.active = active
        self.fs_uniquifier = fs_uniquifier
        self.tf_phone_number=tf_phone_number
        self.tf_primary_method=tf_primary_method
        self.tf_totp_secret=tf_totp_secret
       
        


    def __repr__(self):
        return f'<User {self.name!r}>'
    
