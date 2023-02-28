from flask_app import app
from flask import render_template, session, redirect, request
from datetime import datetime


# DAILY LOG/TRACKER DISPLAY
@app.route("/daily_tracker/<date>")
def daily_tracker(date):
    if "id" in session:
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        return render_template("daily_tracker.html", day=date_obj)
    return redirect("/")


# DAILY CHECKS ADD/EDIT
@app.route("/daily_checks/update/<date>", methods=["POST"])
def daily_checks_update(date):
    if "id" in session:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        daily_check_info = {
            "date": date_obj,
            "water": request.form["water"],
            "user_id": session["id"]
        }
        if "daily_bonus" in request.form:
            daily_check_info["flex_daily_bonus"] = 1
        if "exercise" in request.form:
            daily_check_info["exercise"] = 1

        # validate form input
        #   if valid, check if insert or update and call the appropriate method
        
        print(daily_check_info)
        return redirect(f"/daily_tracker/{date}")
    return redirect("/")


