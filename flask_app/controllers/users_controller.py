from flask_app import app   
from flask import render_template, session, redirect, request
from flask_app.models import user

@app.route("/")
def home():
    return render_template("login_signup.html")


# LOGIN AND SIGN UP
@app.route("/login", methods=["POST"])
def login():
    login_data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    if user.User.validate_login(login_data):
            user_info = user.User.get_by_email(login_data)
            session["id"] = user_info.id
            return redirect ("/dashboard")
    else:
        return redirect("/")

@app.route("/sign_up", methods=["POST"])
def sign_up():
    signup_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if user.User.validate_signup(signup_data):
        session.clear()
        session["id"] = user.User.insert(signup_data)
        return redirect ("/account")
    else:
        session["first_name"] = signup_data["first_name"]
        session["last_name"] = signup_data["last_name"]
        session["email"] = signup_data["email"]
        return redirect("/")


# DASHBOARD
@app.route("/dashboard")
def show_dashboard():
    if "id" in session:
        # pull in user's calculated info and pass to page
        return render_template("dashboard.html")
    return redirect("/")


# ACCOUNT
@app.route("/account")
def show_account():
    if "id" in session:
        return render_template("account.html")
    return redirect("/")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")