from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime
from src import db, bcrypt
from accounts.models import User, AssignedKeys, UserKey
from sqlalchemy import select

accounts_bp = Blueprint("accounts", __name__)

from .forms import LoginForm, RegisterForm, UpdatePassword, RegisterKey, AssignKeys


@accounts_bp.route("/assign_keys", methods=["GET", "POST"])
@login_required
def assign_keys():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    keys = (
        db.session.query(UserKey)
        .join(User, User.id == AssignedKeys.id_user)
        .join(AssignedKeys, UserKey.id == AssignedKeys.id_key)
        .filter(User.id == current_user.id)
        .all()
    )

    choices_keys = [("0", "Select Key")]
    choices_user = [("0", "Select User")]

    for user in users:
        choices_user.append((user.id, user.email))

    for key in keys:
        choices_keys.append((key.id, key.key_description))

    form = AssignKeys(request.form)

    if form.is_submitted():
        # request.form.get('comp_select')
        print(form.id_user.data)
        print(form.id_key.data)
        assign_key = AssignedKeys(
            id_user=form.id_user.data,
            id_key=form.id_key.data,
        )

        assigned_keys = AssignedKeys.query.filter_by(
            id_user=assign_key.id_user, id_key=assign_key.id_key
        ).first()

        if assigned_keys is None:
            db.session.add(assign_key)
            db.session.commit()
            flash(f"Key assigned", "success")
        else:
            flash(f"Key already assigned", "danger")

        return redirect(url_for("accounts.assign_keys"))
    else:
        form.setchoices(choices_user, choices_keys)

    return render_template("accounts/assign_keys.html", form=form)


@accounts_bp.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    form = UpdatePassword(request.form)
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.password.data)
        current_user.changed_pass = datetime.now()
        db.session.commit()
        flash(f"Password Updated Sucessfully", "success")
        return redirect(url_for("core.home"))

    return render_template("accounts/changepassword.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            if user.changed_pass is None:
                return redirect(url_for("accounts.changepassword"))
            else:
                # if user pass older than 6 months
                return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    form = RegisterForm(request.form)
    if request.method == "POST":
        if "delete-user" in request.form:
            user_id = int(request.form.get("user-id"))
            user = User.query.filter(User.id == user_id).first()
            User.query.filter(User.id == user_id).delete()
            db.session.commit()
            if current_user.id == int(user_id):
                logout()
            flash(f"You deleted {user.email}.", "success")
        else:
            form = RegisterForm(request.form)
            if form.validate_on_submit():
                user = User(
                    email=form.email.data,
                    password=form.password.data,
                    is_admin=form.isAdmin.data,
                )
                db.session.add(user)
                db.session.commit()
                flash(f"You registered {user.email}.", "success")

        return redirect(url_for("accounts.register"))
    else:
        return render_template("accounts/register.html", form=form, users=users)


@accounts_bp.route("/register_keys", methods=["GET", "POST"])
@login_required
def register_keys():
    keys = (
        db.session.query(UserKey)
        .join(User, User.id == AssignedKeys.id_user)
        .join(AssignedKeys, UserKey.id == AssignedKeys.id_key)
        .filter(User.id == current_user.id)
        .all()
    )

    form = RegisterKey(request.form)
    if request.method == "POST":
        if "delete-key" in request.form:
            key_id = int(request.form.get("key-id"))
            key = UserKey.query.filter(UserKey.id == key_id).first()
            UserKey.query.filter(UserKey.id == key_id).delete()
            db.session.commit()
            flash(f"You deleted {key.key_description}.", "success")
            return redirect(url_for("accounts.register_keys"))
        else:
            if form.validate_on_submit():
                key = UserKey(
                    key_description=form.key_description.data,
                    hash_key=form.key.data,
                )
                duplicate_key = False

                for row in keys:
                    if key.key_description == row.key_description:
                        duplicate_key = True
                        break

                if duplicate_key == False:
                    db.session.add(key)
                    db.session.commit()

                    userkey = AssignedKeys(id_user=current_user.id, id_key=key.id)

                    db.session.add(userkey)
                    db.session.commit()
                    flash(f"You registered a new key.", "success")
                    return redirect(url_for("accounts.register_keys"))
                else:
                    flash(f"Duplicate key.", "danger")

    return render_template("accounts/register_keys.html", form=form, keys=keys)
