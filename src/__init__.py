import os
from decouple import config
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Registering blueprints
from accounts.views import accounts_bp
from core.views import core_bp
from pack_csv.views import csv_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)
app.register_blueprint(csv_bp)

from accounts.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
