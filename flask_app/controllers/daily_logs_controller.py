from flask_app import app
from flask import render_template, session, redirect, request, jsonify
from datetime import datetime
from flask_app.models import daily_log, meal


# DAILY LOG/TRACKER DISPLAY
@app.route("/daily_tracker/<date>")
def daily_tracker(date):
    if "id" in session:
        print(f'date formatted properly = {date}')
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        if daily_log_id:
            daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
            summary_info = meal.Meal.get_daily_summary({"daily_log_id": daily_log_id})
        else: 
            daily_log_info = False
            summary_info = False
        return render_template("daily_tracker.html", day=date_obj, log_info=daily_log_info, sums=summary_info)
    return redirect("/")

@app.route("/calendar_builder/<month>/<day>/<year>")
def daily_tracker_date_check(month, day, year):
    if "id" in session:
        check = False
        date = f'{year}-{month}-{day}'
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date_obj, "user_id": session["id"]})
        if daily_log_id:
            check = True
        return jsonify(result=check)
    return redirect("/")


# DAILY CHECKS ADD/EDIT
@app.route("/daily_checks/add/<date>")
def daily_checks_add(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        return render_template("daily_checks.html", day=date_obj)
    return redirect("/")

@app.route("/daily_checks/action/<date>", methods=["POST"])
def daily_checks_action(date):
    if "id" in session:
        daily_check_info = {
            "date": date,
            "user_id": session["id"]
        }
        if len(request.form["water"]) < 1:
            daily_check_info["water"] = 0
        else:
            daily_check_info["water"] = request.form["water"]
        if "daily_bonus" in request.form:
            daily_check_info["flex_daily_bonus"] = 1
        else:
            daily_check_info["flex_daily_bonus"] = 0
        if "exercise" in request.form:
            daily_check_info["exercise"] = 1
        else:
            daily_check_info["exercise"] = 0
        
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        if daily_log.DailyLog.validate_daily_checks(daily_check_info):
            if daily_log_id:
                daily_check_info["id"] = daily_log_id
                daily_log.DailyLog.update_daily_checks(daily_check_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
            else: 
                daily_log.DailyLog.insert_daily_checks(daily_check_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
        else:
            session["water"] = daily_check_info["water"]
            session["flex_daily_bonus"] = daily_check_info["flex_daily_bonus"]
            session["exercise"] = daily_check_info["exercise"]
            
            if daily_log_id:
                return redirect(f'/daily_checks/edit/{date}')
            else:
                return redirect(f'/daily_checks/add/{date}')
    return redirect("/")

@app.route("/daily_checks/edit/<date>")
def daily_checks_update(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
        return render_template("daily_checks.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")

@app.route("/daily_checks/action/cancel/<date>")
def daily_checks_action_cancel(date):
    if "id" in session:
        temp = session["id"]
        session.clear()
        session["id"] = temp
        return redirect(f"/daily_tracker/{date}")
    return redirect("/")

# DAILY CHECKS DELETE
@app.route("/daily_checks/delete/<date>")
def daily_checks_delete(date):
    if "id" in session:
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        daily_log.DailyLog.delete_daily_checks({"id": daily_log_id})
        return redirect(f'/daily_tracker/{date}')
    return redirect("/")


# WEIGHTS & MEASUREMENTS ADD/EDIT
@app.route("/weight_measurements/add/<date>")
def weights_measurements_add(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        return render_template("weight_measurements.html", day=date_obj)
    return redirect("/")

@app.route("/weight_measurements/action/<date>", methods=["POST"])
def weights_measurements_action(date):
    if "id" in session:
        wm_info = {
            "date": date,
            "user_id": session["id"]
        }
        if len(request.form["weight"]) < 1:
            wm_info["weight"] = None
        else: 
            wm_info["weight"] = request.form["weight"]
        if len(request.form["bust"]) < 1:
            wm_info["bust"] = None
        else: 
            wm_info["bust"] = request.form["bust"]
        if len(request.form["waist"]) < 1:
            wm_info["waist"] = None
        else: 
            wm_info["waist"] = request.form["waist"]
        if len(request.form["abdomen"]) < 1:
            wm_info["abdomen"] = None
        else: 
            wm_info["abdomen"] = request.form["abdomen"]
        if len(request.form["hips"]) < 1:
            wm_info["hips"] = None
        else: 
            wm_info["hips"] = request.form["hips"]
        if len(request.form["right_arm"]) < 1:
            wm_info["right_arm"] = None
        else: 
            wm_info["right_arm"] = request.form["right_arm"]
        if len(request.form["left_arm"]) < 1:
            wm_info["left_arm"] = None
        else: 
            wm_info["left_arm"] = request.form["left_arm"]
        if len(request.form["right_thigh"]) < 1:
            wm_info["right_thigh"] = None
        else: 
            wm_info["right_thigh"] = request.form["right_thigh"]
        if len(request.form["left_thigh"]) < 1:
            wm_info["left_thigh"] = None
        else: 
            wm_info["left_thigh"] = request.form["left_thigh"]
        if len(request.form["right_calf"]) < 1:
            wm_info["right_calf"] = None
        else: 
            wm_info["right_calf"] = request.form["right_calf"]
        if len(request.form["left_calf"]) < 1:
            wm_info["left_calf"] = None
        else: 
            wm_info["left_calf"] = request.form["left_calf"]

        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        if daily_log.DailyLog.validate_daily_weights_measurements(wm_info):
            if daily_log_id:
                wm_info["id"] = daily_log_id
                daily_log.DailyLog.update_weights_measurements(wm_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
            else: 
                daily_log.DailyLog.insert_weights_measurements(wm_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
        else:
            session["weight"] = wm_info["weight"]
            session["bust"] = wm_info["bust"]
            session["waist"] = wm_info["waist"]
            session["abdomen"] = wm_info["abdomen"]
            session["hips"] = wm_info["hips"]
            session["right_arm"] = wm_info["right_arm"]
            session["left_arm"] = wm_info["left_arm"]
            session["right_thigh"] = wm_info["right_thigh"]
            session["left_thigh"] = wm_info["left_thigh"]
            session["right_calf"] = wm_info["right_calf"]
            session["left_calf"] = wm_info["left_calf"]
            
            if daily_log_id:
                return redirect(f'/weight_measurements/edit/{date}')
            else:
                return redirect(f'/weight_measurements/add/{date}')
    return redirect("/")

@app.route("/weight_measurements/edit/<date>")
def weights_measurements_edit(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
        return render_template("weight_measurements.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")

@app.route("/weight_measurements/action/cancel/<date>")
def weights_measurements_action_cancel(date):
    if "id" in session:
        temp = session["id"]
        session.clear()
        session["id"] = temp
        return redirect(f"/daily_tracker/{date}")
    return redirect("/")
