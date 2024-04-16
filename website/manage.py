import click
from flask.cli import with_appcontext, cli, AppGroup
from . import db
from .models import User
import getpass
from flask import Blueprint
import datetime


user_cli = Blueprint('user', __name__)

@user_cli.cli.command("create_admin")
@with_appcontext
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    name = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email, password, name, is_admin=True, is_active=True, activated_on=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        print("Admin user created successfully.")
    except Exception as e:
        print(f"Couldn't create admin user: {e}")
