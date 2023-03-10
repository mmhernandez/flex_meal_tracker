from flask_app import app   
from flask import render_template, session, redirect, request
from flask_app.models import user, daily_log
import requests
from email.message import EmailMessage
import ssl
import smtplib

@app.route("/")
def home():
    if "id" in session:
        return redirect("/dashboard")
    return render_template("home.html")


# LOGIN AND SIGN UP
@app.route("/log_in")
def login_page():
    if "id" in session:
        return redirect("/dashboard")
    return render_template("login.html")

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
        return redirect("/log_in")

@app.route("/sign_up")
def signup_page():
    if "id" in session:
        return redirect("/dashboard")
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
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
        return redirect("/sign_up")


# DASHBOARD
@app.route("/dashboard")
def show_dashboard():
    if "id" in session:
        wm_stats = daily_log.DailyLog.get_weight_measurement_delta({"id": session["id"]})
        exercise_stats = daily_log.DailyLog.get_exercise_percent({"id": session["id"]})

        return render_template("dashboard.html", wm=wm_stats, exercise=exercise_stats)
    return redirect("/")

@app.route("/exercise", methods=["POST"])
def get_exercise_data():
    if "id" in session:
        if request.form["muscle"] == 'Any':
            muscle = False
        else:
            muscle = request.form["muscle"]

        if muscle:
            api_url = f'https://api.api-ninjas.com/v1/exercises?muscle={muscle}'
        else:
            api_url = 'https://api.api-ninjas.com/v1/exercises'

        api_response = requests.get(api_url, headers={'X-Api-Key': 't7/NdZxSywmrfbmtsPJatw==gDNIQ5EbW62OBoGz'})
        if api_response.status_code == requests.codes.ok:
            response_list = api_response.json()
        else:
            print("Error:", api_response.status_code, api_response.text)

        return render_template("exercises.html", exercise_list=response_list)
    return redirect("/")

@app.route("/email/exercises", methods=["POST"])
def email_exercises():
    if "id" in session:
        print(request.form)

        # send email using python: https://youtu.be/g_j6ILT-X0k
        email_sender = 'flexmealtracker@gmail.com'
        email_password = 'dfkckfavyazvgrkx'  #Email password: flexPython88
        email_recipient = user.User.get_email_by_id({"id": session["id"]})
        subject = 'Exercise List'

        ordered_form_data = []
        #loop through request form in chunks of 10, to group like data together
        #start at 0, then 10, then 20, etc, until 40 (since each exercise has 5 data points)
        chunk = 0
        while chunk <= 40:
            for i in range (chunk, 10):
                ordered_form_data.append(request.form[0])
            chunk += 10

        print(ordered_form_data)
        body = '''
            
        '''

        # em = EmailMessage()
        # em["From"] = email_sender
        # em["To"] = email_recipient
        # em["Subject"] = subject
        # em.set_content(body)

        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        #     smtp.login(email_sender, email_password)
        #     smtp.sendmail(email_sender, email_recipient, em.as_string())

        return redirect("/dashboard")
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
        account_info = {
            "id": session["id"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "age": request.form["age"],
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
            if "age" in session:
                session.pop("age")
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
            session["age"] = account_info["age"]
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

@app.route("/account/cancel/edit")
def cancel_edit_account():
    if "id" in session:
        temp = session["id"]
        session.clear()
        session["id"] = temp
        return redirect("/account")
    return redirect("/")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")