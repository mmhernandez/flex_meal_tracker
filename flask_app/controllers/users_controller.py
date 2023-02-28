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
            session["id"] = user.User.get_id_by_email(login_data)
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
    if user.User.validate_user(signup_data):
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
        user_info = user.User.get_all_by_id({"id": session["id"]})
        return render_template("account.html", user=user_info)
    return redirect("/")

@app.route("/account/edit")
def edit_account():
    if "id" in session:
        user_info = user.User.get_all_by_id({"id": session["id"]})
        return render_template("account_edit.html", user=user_info)
    return redirect("/")

@app.route("/account/update", methods=["POST"])
def update_account():
    if "id" in session:
        print(request.form)
        account_info = {
            "id": session["id"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "sex": request.form["sex"],
            "weight": request.form["weight"],
            "bust": request.form["bust"],
            "waist": request.form["waist"],
            "abdomen": request.form["abdomen"],
            "hips": request.form["hips"],
            "right_arm": request.form["right_arm"],
            "left_arm": request.form["left_arm"],
            "right_thigh": request.form["right_thigh"],
            "left_thigh": request.form["left_thigh"],
            "right_calf": request.form["right_calf"],
            "left_calf": request.form["left_calf"]
        }
        user_info = user.User.get_all_by_id({"id": session["id"]})
        if request.form["email"] != user_info.email:
            account_info["email"] == request.form["email"]   
        
        if user.User.validate_account_info(account_info):
            user.User.update(account_info)
            if "first_name" in session:
                session.pop("first_name")
            if "last_name" in session:
                session.pop("last_name")
            if "email" in session:
                session.pop("email")
            if "sex" in session:
                session.pop("sex")
            if "weight" in session:
                session.pop("weight")
            if "bust" in session:
                session.pop("bust")
            if "waist" in session:
                session.pop("waist")
            if "abdomen" in session:
                session.pop("abdomen")
            if "hips" in session: 
                session.pop("hips")
            if "right_arm" in session:
                session.pop("right_arm")
            if "left_arm" in session:
                session.pop("left_arm")
            if "right_thigh" in session:
                session.pop("right_thigh")
            if "left_thigh" in session:
                session.pop("left_thigh")
            if "right_calf" in session:
                session.pop("right_calf")
            if "left_calf" in session: 
                session.pop("left_calf")
                
            return redirect("/account")
        else:
            session["first_name"] = account_info["first_name"]
            session["last_name"] = account_info["last_name"]
            session["sex"] = account_info["sex"]
            session["weight"] = account_info["weight"]
            session["bust"] = account_info["bust"]
            session["waist"] = account_info["waist"]
            session["abdomen"] = account_info["abdomen"]
            session["hips"] = account_info["hips"]
            session["right_arm"] = account_info["right_arm"]
            session["left_arm"] = account_info["left_arm"]
            session["right_thigh"] = account_info["right_thigh"]
            session["left_thigh"] = account_info["left_thigh"]
            session["right_calf"] = account_info["right_calf"]
            session["left_calf"] = account_info["left_calf"]
            if "email" in account_info:
                session["email"] = account_info["email"]
            return redirect("/account/edit")
    return redirect("/")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")