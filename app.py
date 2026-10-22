from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User, VaultEntry
from crypto import encrypt_password, decrypt_password

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

import bcrypt
import secrets
import string

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()


def generate_password(length=20):
    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*()?"
    )

    return "".join(
        secrets.choice(chars)
        for _ in range(length)
    )


@app.route("/")
def home():
    return redirect(url_for("login"))


# -----------------------
# REGISTER
# -----------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "Username already exists"

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        new_user = User(
            username=username,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------
# LOGIN
# -----------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "Invalid username or password"

        if bcrypt.checkpw(
            password.encode(),
            user.password_hash.encode()
        ):
            login_user(user)
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")


# -----------------------
# LOGOUT
# -----------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# -----------------------
# DASHBOARD
# -----------------------

@app.route("/dashboard")
@login_required
def dashboard():

    search = request.args.get("search", "")

    entries = VaultEntry.query.filter(
        VaultEntry.user_id == current_user.id,
        VaultEntry.site.contains(search)
    ).all()

    count = len(entries)

    return render_template(
        "dashboard.html",
        username=current_user.username,
        entries=entries,
        search=search,
        count=count
    )


# -----------------------
# ADD PASSWORD
# -----------------------

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        site = request.form["site"]
        account_username = request.form["account_username"]
        password = request.form["password"]

        encrypted_password = encrypt_password(password)

        new_entry = VaultEntry(
            site=site,
            account_username=account_username,
            encrypted_password=encrypted_password,
            user_id=current_user.id
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_password.html")


# -----------------------
# VIEW PASSWORD
# -----------------------

@app.route("/view/<int:entry_id>")
@login_required
def view_password(entry_id):

    entry = VaultEntry.query.filter_by(
        id=entry_id,
        user_id=current_user.id
    ).first_or_404()

    password = decrypt_password(
        entry.encrypted_password
    )

    return f"""
    <h2>{entry.site}</h2>

    <p>User: {entry.account_username}</p>

    <p><b>Password:</b> {password}</p>

    <a href="/dashboard">Back</a>
    """


# -----------------------
# DELETE PASSWORD
# -----------------------

@app.route("/delete/<int:entry_id>")
@login_required
def delete_password(entry_id):

    entry = VaultEntry.query.filter_by(
        id=entry_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for("dashboard"))


# -----------------------
# EDIT PASSWORD
# -----------------------

@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_password(entry_id):

    entry = VaultEntry.query.filter_by(
        id=entry_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        entry.site = request.form["site"]
        entry.account_username = request.form["username"]

        entry.encrypted_password = encrypt_password(
            request.form["password"]
        )

        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template(
        "edit_password.html",
        entry=entry
    )


# -----------------------
# PASSWORD GENERATOR
# -----------------------

@app.route("/generate")
@login_required
def generate():

    password = generate_password()

    return password


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )