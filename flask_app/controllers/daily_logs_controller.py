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
        return render_template("test_daily_tracker.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")


# DAILY CHECKS ADD/EDIT
# need to rework this section like the weights & measures section below!
@app.route("/daily_checks/add/<date>", methods=["POST"])
def daily_checks_add(date):
    if "id" in session:
        # date_obj = datetime.strptime(date, '%Y-%m-%d')
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

        if daily_log.DailyLog.validate_daily_checks(daily_check_info):
            daily_log.DailyLog.update_daily_checks(daily_check_info)
            # pop any stored session values for this section
            return redirect(f"/daily_tracker/{date}")
        else:
            # store values in session
            # # need to redirect to the modal pop-up to display error for resumbission
            return redirect(f"/daily_tracker/{date}")
    return redirect("/")


# WEIGHTS & MEASUREMENTS ADD/EDIT
@app.route("/weight_measurements/add/<date>")
def weights_measurements_add(date):
    if "id" in session:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        return render_template("weight_measurements_add.html", day=date_obj, type='add')
    return redirect("/")

@app.route("/weight_measurements/insert/<date>", methods=["POST"])
def weights_measurements_insert(date):
    if "id" in session:
        wm_info = {
            "date": date,
            "user_id": session["id"]
        }
        if "weight" in request.form:
            wm_info["weight"] = request.form["weight"]
        else:
            wm_info["weight"] = None
        if "bust" in request.form:
            wm_info["bust"] = request.form["bust"]
        else:
            wm_info["bust"] = None
        if "waist" in request.form:
            wm_info["waist"] = request.form["waist"]
        else:
            wm_info["waist"] = None
        if "abdomen" in request.form:
            wm_info["abdomen"] = request.form["abdomen"]
        else:
            wm_info["abdomen"] = None
        if "hips" in request.form:
            wm_info["hips"] = request.form["hips"]
        else:
            wm_info["hips"] = None
        if "right_arm" in request.form:
            wm_info["right_arm"] = request.form["right_arm"]
        else:
            wm_info["right_arm"] = None
        if "left_arm" in request.form:
            wm_info["left_arm"] = request.form["left_arm"]
        else:
            wm_info["left_arm"] = None
        if "right_thigh" in request.form:
            wm_info["right_thigh"] = request.form["right_thigh"]
        else:
            wm_info["right_thigh"] = None
        if "left_thigh" in request.form:
            wm_info["left_thigh"] = request.form["left_thigh"]
        else:
            wm_info["left_thigh"] = None
        if "right_calf" in request.form:
            wm_info["right_calf"] = request.form["right_calf"]
        else:
            wm_info["right_calf"] = None
        if "left_calf" in request.form:
            wm_info["left_calf"] = request.form["left_calf"]
        else:
            wm_info["left_calf"] = None

        print(f'wm_info = {wm_info}')

        if daily_log.DailyLog.validate_daily_weights_measurements(wm_info):
            daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date})
            if daily_log_id:
                daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
                # call update method for daily logs
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
            else: 
                if len(wm_info["weight"]) < 1:
                    wm_info["weight"] = 0
                if len(wm_info["bust"]) < 1:
                    wm_info["bust"] = 0
                if len(wm_info["waist"]) < 1:
                    wm_info["waist"] = 0
                if len(wm_info["abdomen"]) < 1:
                    wm_info["abdomen"] = 0
                if len(wm_info["hips"]) < 1:
                    wm_info["hips"] = 0
                if len(wm_info["right_arm"]) < 1:
                    wm_info["right_arm"] = 0
                if len(wm_info["left_arm"]) < 1:
                    wm_info["left_arm"] = 0
                if len(wm_info["right_thigh"]) < 1:
                    wm_info["right_thigh"] = 0
                if len(wm_info["left_thigh"]) < 1:
                    wm_info["left_thigh"] = 0
                if len(wm_info["right_calf"]) < 1:
                    wm_info["right_calf"] = 0
                if len(wm_info["left_calf"]) < 1:
                    wm_info["left_calf"] = 0

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
            
            return redirect(f'/weight_measurements/add/{date}')
    return redirect("/")

@app.route("/weight_measurements/edit/<date>")
def weights_measurements_edit(date):
    if "id" in session:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        # pull weights and measurements and pass to html
        return render_template("weight_measurements_update.html", day=date_obj, type='edit')
    return redirect("/")

@app.route("/weight_measurements/update/<date>", methods=["POST"])
def weights_measurements_update(date):
    if "id" in session:
        #get form data
        #validate form input
        #  if valid, call update method
        return redirect(f"/daily_tracker/{date}")
        #if not valid
        #  save fields in session
        #  redirect back to edit route w/ error messages
    return redirect("/")
