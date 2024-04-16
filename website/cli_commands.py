import getpass


def register_commands(app):
    @app.cli.command("create_admin")
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
        except Exception:
            print("Couldn't create admin user.")
