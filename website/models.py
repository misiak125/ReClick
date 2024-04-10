from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model, UserMixin):

    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(1000))
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_banned = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, is_admin=False, is_banned=False):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password, method='scrypt')
        self.created_on = datetime.datetime.now()
        self.is_admin = is_admin
        self.is_banned = is_banned

    

