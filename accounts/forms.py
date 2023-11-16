from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, StringField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flask_login import current_user

from src import db, bcrypt

from sqlalchemy import select

from accounts.models import User, AssignedKeys, UserKey


class AssignKeys(FlaskForm):
    id_user = SelectField(
        "User",
        choices=[],
        validators=[],
    )
    id_key = SelectField(
        "Key",
        choices=[],
        validators=[],
    )

    def setchoices(self, choices_user, choices_keys):
        self.id_user.choices = choices_user
        self.id_key.choices = choices_keys


class RegisterKey(FlaskForm):
    key_description = StringField("Key Description", validators=[DataRequired()])
    key = StringField("Key", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class UpdatePassword(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(UpdatePassword, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=current_user.email).first()
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    isAdmin = BooleanField(
        "Admin?",
        validators=[],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True
