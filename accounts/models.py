from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from src import bcrypt, db


class UserFiles(db.Model):
    __tablename__ = "files_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, ForeignKey("users.id"))
    filedescription = db.Column(db.String, unique=False, nullable=False)
    filepath = db.Column(db.String, unique=False, nullable=False)
    uploaded = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_user, filedescription, filepath):
        self.id_user = id_user
        self.filedescription = filedescription
        self.filepath
        self.uploaded = datetime.now()

    def __repr__(self):
        return f"<file id: {self.id}>"


class AssignedKeys(db.Model):
    __tablename__ = "keys_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, ForeignKey("users.id"))
    id_key = db.Column(db.Integer, ForeignKey("keys.id"))
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, id_user, id_key):
        self.id_user = id_user
        self.id_key = id_key
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<assign id: {self.id}>"


class UserKey(db.Model):
    __tablename__ = "keys"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key_description = db.Column(db.String, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    hash_key = db.Column(db.String, nullable=False)

    def __init__(self, key_description, hash_key):
        self.key_description = key_description
        self.hash_key = hash_key
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<key_description {self.key_description}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    changed_pass = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.changed_pass = None

    def __repr__(self):
        return f"<email {self.email}>"
