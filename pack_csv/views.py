from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime
from src import db, bcrypt
from accounts.models import UserFiles, UserKey, User, AssignedKeys
from sqlalchemy import select
from werkzeug.utils import secure_filename
import os
from src import app
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent


from langchain.llms import OpenAI


from .forms import RegisterCSV, QueryCSV


csv_bp = Blueprint("pack_csv", __name__)


def GetResponse(query, file, api_key):
    user_files_path = os.path.join(
        app.instance_path, current_user.email.replace("@", "_")
    )

    agent = create_csv_agent(
        OpenAI(temperature=0, openai_api_key=api_key),
        os.path.join(user_files_path, file),
        verbose=True,
        return_intermediate_steps=True,
    )
    response = agent({"input": query})
    reply = response["output"]

    return reply


@csv_bp.route("/query_csv", methods=["GET", "POST"])
@login_required
def query_csv():
    reply = None
    filelist = []
    user_files_path = os.path.join(
        app.instance_path, current_user.email.replace("@", "_")
    )

    with os.scandir(user_files_path) as it:
        for entry in it:
            if entry.is_file():
                filelist.append(entry.name)
    keys = (
        db.session.query(UserKey)
        .join(User, User.id == AssignedKeys.id_user)
        .join(AssignedKeys, UserKey.id == AssignedKeys.id_key)
        .filter(User.id == current_user.id)
        .all()
    )
    key_choices = []
    for key in keys:
        key_choices.append([key.id, key.key_description])

    form = QueryCSV(request.form)

    form.setchoices(filelist, key_choices)
    if form.is_submitted():
        file = form.selected_file.data
        key = form.selected_key.data
        query = form.query.data

        secret_key = UserKey.query.filter_by(id=key).first()
        if secret_key is not None:
            try:
                reply = GetResponse(query, file, secret_key.hash_key)
            except Exception as error:
                flash(
                    f"An error ocurred.\nThe error could be excessive tokens used (depends on you aPI key tier). Error message was: \n {error}",
                    "danger",
                )
            return render_template("pack_csv/query.html", form=form, reply=reply)
        else:
            flash(
                f"Invalid Key",
                "danger",
            )

    return render_template("pack_csv/query.html", form=form, reply=reply)


def get_dir_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


@csv_bp.route("/upload_csv", methods=["GET", "POST"])
@login_required
def upload_csv():
    user_files_path = os.path.join(
        app.instance_path, current_user.email.replace("@", "_")
    )
    if not os.path.isdir(user_files_path):
        os.mkdir(user_files_path)

    filelist = []

    with os.scandir(user_files_path) as it:
        for entry in it:
            if entry.is_file():
                filelist.append(entry.name)

    form = RegisterCSV()
    if request.method == "POST":
        if "csv-delete" in request.form:
            file = request.form.get("filename")
            try:
                os.remove(os.path.join(user_files_path, file))
                return redirect(url_for("pack_csv.upload_csv"))
            except Exception as error:
                flash(f"Failed to deleted file: {file}. Message: \n {error}", "danger")
        else:
            if form.validate_on_submit():
                # Create User directory For Files
                user_used_storage = get_dir_size(user_files_path)
                if get_dir_size(user_files_path) > 5242880:
                    flash(f"You exceeded you storage limit.", "danger")
                else:
                    filename = secure_filename(form.file.data.filename)
                    try:
                        form.file.data.save(os.path.join(user_files_path, filename))
                        return redirect(url_for("pack_csv.upload_csv"))
                    except Exception as error:
                        flash(
                            f"Failed to save file: {filename}. Message: \n {error}",
                            "danger",
                        )

    return render_template("pack_csv/upload.html", form=form, filelist=filelist)
