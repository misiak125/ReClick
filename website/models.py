from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.orm import relationship


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = relationship("User", back_populates="games")

    def __init__(self, user_id, score):
        self.user_id = user_id
        self.score = score

class User(db.Model, UserMixin):

    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    name = db.Column(db.String(100))
    
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_banned = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    activated_on = db.Column(db.DateTime, nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)


    games = relationship("Game", back_populates="user")

   
    def __init__(self, email, name, password, is_admin=False, is_banned=False, is_confirmed=False, activated_on=None, profile_picture=None):

        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.created_on = datetime.datetime.now()
        self.is_admin = is_admin            
        self.is_banned = is_banned
        self.is_confirmed = is_confirmed
        self.activated_on = activated_on
        self.profile_picture = profile_picture

    def __repr__(self):
        return f"<email: {self.email}, username: {self.name}>"
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_to_id = db.Column(db.Integer, nullable=False)
    user_from_id = db.Column(db.Integer, nullable=False)
    user_from_name = db.Column(db.String(100), nullable=False)

    def __init__ (self, body, timestamp, user_to_id, user_from_id, user_from_name):
        self.body=body
        self.timestamp = timestamp
        self.user_to_id = user_to_id
        self.user_from_id = user_from_id
        self.user_from_name = user_from_name

    def __repr__(self):
        return '<Post %r>' % (self.body)

