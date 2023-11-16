from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from flask_wtf.file import FileRequired, FileField, FileAllowed, FileSize
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flask_login import current_user

from src import db, bcrypt

from sqlalchemy import select

from accounts.models import User, AssignedKeys, UserKey


class QueryCSV(FlaskForm):
    query = StringField("Query", validators=[DataRequired()])
    selected_file = SelectField(
        "CSV",
        choices=[],
        validators=[],
    )
    selected_key = SelectField(
        "Key",
        choices=[],
        validators=[],
    )

    def setchoices(self, choices_selectCSV, choices_selectKey):
        self.selected_file.choices = choices_selectCSV
        self.selected_key.choices = choices_selectKey


class RegisterCSV(FlaskForm):
    fileDescritpion = StringField("Description", validators=[DataRequired()])
    file = FileField(
        validators=[
            FileRequired(),
            FileAllowed(["csv"], "CSV only!"),
            FileSize(max_size=1048576),
        ]
    )
