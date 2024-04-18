import click
from flask.cli import with_appcontext, cli, AppGroup
from . import db
from .models import User
import getpass
from flask import Blueprint
import datetime

def is_truthy(string: str) -> bool:
    return string.lower() in ["tak", "t", "yes", "y", "1"]

user_cli = Blueprint('user', __name__)

@user_cli.cli.command("create_admin")
@with_appcontext
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Email already registered")
        return 1

    name = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email, name, password, is_admin=True, is_active=True, activated_on=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        print(f"Admin {name} with email {email} created successfully.")
    except Exception as e:
        print(f"Couldn't create admin user: {e}")


@user_cli.cli.command("delete_user")
@click.argument("email")
@with_appcontext
def delete_user(email):
    """Delete a user from the database."""
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            confirm=input(f"Are you sure you want to delete user: {user.name}, registered with email adress: {user.email}? [y/n]")
            if is_truthy(confirm):
                db.session.delete(user)
                db.session.commit()
                print(f"User with email '{email}' has been deleted successfully.")
            else: 
                print("Cancelled")
                return 1
        else:
            print(f"User with email '{email}' not found.")
    except Exception as e:
        print(f"An error occurred while deleting the user: {e}")