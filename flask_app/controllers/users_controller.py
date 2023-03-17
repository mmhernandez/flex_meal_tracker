from flask_app import app   
from flask import render_template, session, redirect, request
from flask_app.models import user, daily_log


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
        weight_stats = daily_log.DailyLog.get_weight_delta({"id": session["id"]})
        measurement_stats = daily_log.DailyLog.get_measurements_delta({"id": session["id"]})
        exercise_stats = daily_log.DailyLog.get_exercise_percent({"id": session["id"]})

        print(f'weight_stats = {weight_stats}')
        print(f'measurement_stats = {measurement_stats}')
        return render_template("dashboard.html", weight=weight_stats, measurements=measurement_stats, exercise=exercise_stats)
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

@app.route("/report/<type>")
def show_report(type):
    if "id" in session:
        data = {
            "user_id": session["id"]
        }
        if type == "week":
            data["duration"] = -7
            data["type"] = "week"
        elif type == "month":
            data["duration"] = -30
            data["type"] = "month"
        data = daily_log.DailyLog.get_logs_w_meals_by_date_and_user(data)

        return render_template("reports.html", type=type, data=data)
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
            "age": request.form["age"]
        }
        if len(request.form["weight"]) < 1:
            account_info["weight"] = None
        else: 
            account_info["weight"] = request.form["weight"]
        if len(request.form["bust"]) < 1:
            account_info["bust"] = None
        else: 
            account_info["bust"] = request.form["bust"]
        if len(request.form["waist"]) < 1:
            account_info["waist"] = None
        else: 
            account_info["waist"] = request.form["waist"]
        if len(request.form["abdomen"]) < 1:
            account_info["abdomen"] = None
        else: 
            account_info["abdomen"] = request.form["abdomen"]
        if len(request.form["hips"]) < 1:
            account_info["hips"] = None
        else: 
            account_info["hips"] = request.form["hips"]
        if len(request.form["right_arm"]) < 1:
            account_info["right_arm"] = None
        else: 
            account_info["right_arm"] = request.form["right_arm"]
        if len(request.form["left_arm"]) < 1:
            account_info["left_arm"] = None
        else: 
            account_info["left_arm"] = request.form["left_arm"]
        if len(request.form["right_thigh"]) < 1:
            account_info["right_thigh"] = None
        else: 
            account_info["right_thigh"] = request.form["right_thigh"]
        if len(request.form["left_thigh"]) < 1:
            account_info["left_thigh"] = None
        else: 
            account_info["left_thigh"] = request.form["left_thigh"]
        if len(request.form["right_calf"]) < 1:
            account_info["right_calf"] = None
        else: 
            account_info["right_calf"] = request.form["right_calf"]
        if len(request.form["left_calf"]) < 1:
            account_info["left_calf"] = None
        else: 
            account_info["left_calf"] = request.form["left_calf"]

        user_info = user.User.get_all_by_id({"id": session["id"]})
        if request.form["email"] != user_info.email:
            account_info["email"] == request.form["email"]   
        
        if user.User.validate_account_info(account_info):
            user.User.update(account_info)
            
            temp = session["id"]
            session.clear()
            session["id"] = temp
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