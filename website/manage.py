import click
from flask.cli import with_appcontext, cli
from . import db
from .models import User
import getpass


@cli.command("create_admin")
@with_appcontext
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print("Admin user created successfully.")
    except Exception as e:
        print(f"Couldn't create admin user: {e}")
