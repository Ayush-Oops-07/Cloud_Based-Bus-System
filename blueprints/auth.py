from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not all([name, email, password]):
            flash("Please fill in required fields.", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return render_template("auth/register.html")

        user = User(
            username=name,
            email=email,
            phone=phone,
            password_hash=password, # ⬅️ Store password directly
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# In blueprints/auth.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user
from models import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        
        # ➡️ Use the correct attribute for the password
        if not user or user.password_hash != password:
            # ➡️ Use flash to store the message
            flash("Invalid credentials", "danger") 
            # ➡️ Render the template again without redirect
            return render_template("auth/login.html")

        login_user(user)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("passenger.search"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful.", "info")
    return redirect(url_for("auth.login"))




