from flask_app import app
from flask import render_template, session, redirect, request
from datetime import datetime
from flask_app.models import daily_log


# DAILY LOG/TRACKER DISPLAY
@app.route("/daily_tracker/<date>")
def daily_tracker(date):
    if "id" in session:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date})
        if daily_log_id:
            daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
        else: 
            daily_log_info = False
        return render_template("daily_tracker.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")


# DAILY CHECKS ADD/EDIT
@app.route("/daily_checks/add/<date>", methods=["POST"])
def daily_checks_add(date):
    if "id" in session:
        daily_check_info = {
            "date": date,
            "user_id": session["id"]
        }
        if len(request.form["water"]) < 1:
            daily_check_info["water"] = 0
        else:
            daily_check_info["water"] = 0
        if "daily_bonus" in request.form:
            daily_check_info["flex_daily_bonus"] = 1
        else:
            daily_check_info["flex_daily_bonus"] = 0
        if "exercise" in request.form:
            daily_check_info["exercise"] = 1
        else:
            daily_check_info["exercise"] = 0
        
        if daily_log.DailyLog.validate_daily_checks(daily_check_info):
            daily_log.DailyLog.insert_daily_checks(daily_check_info)
            # pop any stored session values for this section
            return redirect(f"/daily_tracker/{date}")
        else:
            # store values in session
            # need to redirect to the modal pop-up to display error for resumbission
            return redirect(f"/daily_tracker/{date}")
    return redirect("/")

@app.route("/daily_checks/update/<date>", methods=["POST"])
def daily_checks_update(date):
    if "id" in session:
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date})

        print(f'request.form = {request.form}')
        daily_check_info = {
            "user_id": session["id"],
            "water": request.form["water"],
            "id": daily_log_id
        }
        if ("daily_bonus" in request.form) and request.form["daily_bonus"] == 'on':
            daily_check_info["flex_daily_bonus"] = 1
        else:
            daily_check_info["flex_daily_bonus"] = 0
        if ("exercise" in request.form) and request.form["exercise"] == 'on':
            daily_check_info["exercise"] = 1
        else:
            daily_check_info["exercise"] = 0
        print(f'request.form = {request.form}')
        print(f'daily_check_info = {daily_check_info}')

        if daily_log.DailyLog.validate_daily_checks(daily_check_info):
            daily_log.DailyLog.update_daily_checks(daily_check_info)
            # pop any stored session values for this section
            return redirect(f"/daily_tracker/{date}")
        else:
            # store values in session
            # # need to redirect to the modal pop-up to display error for resumbission
            return redirect(f"/daily_tracker/{date}")
    return redirect("/")


