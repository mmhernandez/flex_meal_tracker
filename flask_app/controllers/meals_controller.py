from flask_app import app
from flask import session, redirect, render_template, request
from datetime import datetime
from flask_app.models import daily_log, meal


# MEAL DETAILS ADD/EDIT
@app.route("/meal_details/add/<date>")
def meal_details_add(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        return render_template("meal_details.html", day=date_obj)
    return redirect("/")

@app.route("/meal_details/action/<date>", methods=["POST"])
def meal_details_action(date):
    if "id" in session:
        meal_detal_info = {
            "date": date,
            "user_id": session["id"],
            "breakfast_details": request.form["breakfast_details"],
            "breakfast_proteins": request.form["breakfast_proteins"],
            "breakfast_fats": request.form["breakfast_fats"],
            "breakfast_fruits": request.form["breakfast_fruits"],
            "breakfast_vegetables": request.form["breakfast_vegetables"],
            "lunch_details": request.form["lunch_details"],
            "lunch_proteins": request.form["lunch_proteins"],
            "lunch_fats": request.form["lunch_fats"],
            "lunch_fruits": request.form["lunch_fruits"],
            "lunch_vegetables": request.form["lunch_vegetables"],
            "dinner_details": request.form["dinner_details"],
            "dinner_proteins": request.form["dinner_proteins"],
            "dinner_fats": request.form["dinner_fats"],
            "dinner_fruits": request.form["dinner_fruits"],
            "dinner_vegetables": request.form["dinner_vegetables"],
            "snack_details": request.form["snack_details"],
            "snack_proteins": request.form["snack_proteins"],
            "snack_fats": request.form["snack_fats"],
            "snack_fruits": request.form["snack_fruits"],
            "snack_vegetables": request.form["snack_vegetables"]
        }

        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        if meal.Meal.validate_meal(meal_detal_info):
            if daily_log_id:
                meal_detal_info["id"] = daily_log_id
                # daily_log.DailyLog.update_daily_checks(daily_check_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
            else: 
                # daily_log.DailyLog.insert_daily_checks(daily_check_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
        else:
            session["breakfast_details"] = meal_detal_info["breakfast_details"],
            session["breakfast_proteins"] = meal_detal_info["breakfast_proteins"],
            session["breakfast_fats"] = meal_detal_info["breakfast_fats"],
            session["breakfast_fruits"] = meal_detal_info["breakfast_fruits"],
            session["breakfast_vegetables"] = meal_detal_info["breakfast_vegetables"],
            session["lunch_details"] = meal_detal_info["lunch_details"],
            session["lunch_proteins"] = meal_detal_info["lunch_proteins"],
            session["lunch_fats"] = meal_detal_info["lunch_fats"],
            session["lunch_fruits"] = meal_detal_info["lunch_fruits"],
            session["lunch_vegetables"] = meal_detal_info["lunch_vegetables"],
            session["dinner_details"] = meal_detal_info["dinner_details"],
            session["dinner_proteins"] = meal_detal_info["dinner_proteins"],
            session["dinner_fats"] = meal_detal_info["dinner_fats"],
            session["dinner_fruits"] = meal_detal_info["dinner_fruits"],
            session["dinner_vegetables"] = meal_detal_info["dinner_vegetables"],
            session["snack_details"] = meal_detal_info["snack_details"],
            session["snack_proteins"] = meal_detal_info["snack_proteins"],
            session["snack_fats"] = meal_detal_info["snack_fats"],
            session["snack_fruits"] = meal_detal_info["snack_fruits"],
            session["snack_vegetables"] = meal_detal_info["snack_vegetables"]
            
            if daily_log_id:
                return redirect(f'/meal_details/edit/{date}')
            else:
                return redirect(f'/meal_details/add/{date}')
    return redirect("/")

@app.route("/meal_details/edit/<date>")
def meal_details_update(date):
    if "id" in session:
        date_obj = datetime.strptime(date,'%Y-%m-%d')
        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
        return render_template("meal_detailss.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")
