from flask.cli import FlaskGroup
from flask_login import login_user

from src import app
from src import db
from accounts.models import User

import getpass

from flask_login import LoginManager

from dotenv import load_dotenv

load_dotenv()


cli = FlaskGroup(app)

login_manager = LoginManager()


@cli.command("create_admin")
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


if __name__ == "__main__":
    cli()
