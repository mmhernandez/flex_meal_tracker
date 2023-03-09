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
        breakfast_meal_info = {
            "meal_type": "breakfast",
            "details": request.form["breakfast_details"],
            "proteins": request.form["breakfast_proteins"],
            "fats": request.form["breakfast_fats"],
            "fruits": request.form["breakfast_fruits"],
            "vegetables": request.form["breakfast_vegetables"]
        }
        if len(request.form["breakfast_proteins"]) < 1:
            breakfast_meal_info["proteins"] = 0
        else: 
            breakfast_meal_info["proteins"] = request.form["breakfast_proteins"]
        if len(request.form["breakfast_fats"]) < 1:
            breakfast_meal_info["fats"] = 0
        else: 
            breakfast_meal_info["fats"] = request.form["breakfast_fats"]
        if len(request.form["breakfast_fruits"]) < 1:
            breakfast_meal_info["fruits"] = 0
        else: 
            breakfast_meal_info["fruits"] = request.form["breakfast_fruits"]
        if len(request.form["breakfast_vegetables"]) < 1:
            breakfast_meal_info["vegetables"] = 0
        else: 
            breakfast_meal_info["vegetables"] = request.form["breakfast_vegetables"]
        is_breakast_valid = meal.Meal.validate_meal(breakfast_meal_info)

        lunch_meal_info = {
            "meal_type": "lunch",
            "details": request.form["lunch_details"],
            "proteins": request.form["lunch_proteins"],
            "fats": request.form["lunch_fats"],
            "fruits": request.form["lunch_fruits"],
            "vegetables": request.form["lunch_vegetables"]
        }
        if len(request.form["lunch_proteins"]) < 1:
            lunch_meal_info["proteins"] = 0
        else: 
            lunch_meal_info["roteins"] = request.form["lunch_proteins"]
        if len(request.form["lunch_fats"]) < 1:
            lunch_meal_info["fats"] = 0
        else: 
            lunch_meal_info["fats"] = request.form["lunch_fats"]
        if len(request.form["lunch_fruits"]) < 1:
            lunch_meal_info["fruits"] = 0
        else: 
            lunch_meal_info["fruits"] = request.form["lunch_fruits"]
        if len(request.form["lunch_vegetables"]) < 1:
            lunch_meal_info["vegetables"] = 0
        else: 
            lunch_meal_info["vegetables"] = request.form["lunch_vegetables"]
        is_lunch_valid = meal.Meal.validate_meal(lunch_meal_info)

        dinner_meal_info = {
            "meal_type": "dinner",
            "details": request.form["dinner_details"],
            "proteins": request.form["dinner_proteins"],
            "fats": request.form["dinner_fats"],
            "fruits": request.form["dinner_fruits"],
            "vegetables": request.form["dinner_vegetables"]
        }
        if len(request.form["dinner_proteins"]) < 1:
            dinner_meal_info["proteins"] = 0
        else: 
            dinner_meal_info["proteins"] = request.form["dinner_proteins"]
        if len(request.form["dinner_fats"]) < 1:
            dinner_meal_info["fats"] = 0
        else: 
            dinner_meal_info["fats"] = request.form["dinner_fats"]
        if len(request.form["dinner_fruits"]) < 1:
            dinner_meal_info["fruits"] = 0
        else: 
            dinner_meal_info["fruits"] = request.form["dinner_fruits"]
        if len(request.form["dinner_vegetables"]) < 1:
            dinner_meal_info["vegetables"] = 0
        else: 
            dinner_meal_info["vegetables"] = request.form["dinner_vegetables"]
        is_dinner_valid = meal.Meal.validate_meal(dinner_meal_info)

        snack_meal_info = {
            "meal_type": "snack",
            "details": request.form["snack_details"],
            "proteins": request.form["snack_proteins"],
            "fats": request.form["snack_fats"],
            "fruits": request.form["snack_fruits"],
            "vegetables": request.form["snack_vegetables"]
        }
        if len(request.form["snack_proteins"]) < 1:
            snack_meal_info["proteins"] = 0
        else: 
            snack_meal_info["proteins"] = request.form["snack_proteins"]
        if len(request.form["snack_fats"]) < 1:
            snack_meal_info["fats"] = 0
        else: 
            snack_meal_info["fats"] = request.form["snack_fats"]
        if len(request.form["snack_fruits"]) < 1:
            snack_meal_info["fruits"] = 0
        else: 
            snack_meal_info["fruits"] = request.form["snack_fruits"]
        if len(request.form["snack_vegetables"]) < 1:
            snack_meal_info["vegetables"] = 0
        else: 
            snack_meal_info["vegetables"] = request.form["snack_vegetables"]
        is_snack_valid = meal.Meal.validate_meal(snack_meal_info)

        daily_log_id = daily_log.DailyLog.get_id_by_date({"date": date, "user_id": session["id"]})
        if is_breakast_valid and is_lunch_valid and is_dinner_valid and is_snack_valid:
            if daily_log_id:
                breakfast_meal_info["daily_log_id"] = daily_log_id
                lunch_meal_info["daily_log_id"] = daily_log_id
                dinner_meal_info["daily_log_id"] = daily_log_id
                snack_meal_info["daily_log_id"] = daily_log_id

                daily_log_info = daily_log.DailyLog.get_all_by_id({"id": daily_log_id})
                if daily_log_info.meals:
                    meal.Meal.update_meal_details(breakfast_meal_info)
                    meal.Meal.update_meal_details(lunch_meal_info) 
                    meal.Meal.update_meal_details(dinner_meal_info)
                    meal.Meal.update_meal_details(snack_meal_info)
                
                else:
                    meal.Meal.insert_meal_details(breakfast_meal_info)
                    meal.Meal.insert_meal_details(lunch_meal_info)
                    meal.Meal.insert_meal_details(dinner_meal_info) 
                    meal.Meal.insert_meal_details(snack_meal_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
            else: 
                new_daily_log_id = daily_log.DailyLog.insert_blank_for_meal({"date": date, "user_id": session["id"]})

                breakfast_meal_info["daily_log_id"] = new_daily_log_id
                meal.Meal.insert_meal_details(breakfast_meal_info)

                lunch_meal_info["daily_log_id"] = new_daily_log_id
                meal.Meal.insert_meal_details(lunch_meal_info)

                dinner_meal_info["daily_log_id"] = new_daily_log_id
                meal.Meal.insert_meal_details(dinner_meal_info)

                snack_meal_info["daily_log_id"] = new_daily_log_id
                meal.Meal.insert_meal_details(snack_meal_info)
                
                temp = session["id"]
                session.clear()
                session["id"] = temp
                return redirect(f"/daily_tracker/{date}")
        else:
            session["breakfast_details"] = breakfast_meal_info["details"]
            session["breakfast_proteins"] = breakfast_meal_info["proteins"]
            session["breakfast_fats"] = breakfast_meal_info["fats"]
            session["breakfast_fruits"] = breakfast_meal_info["fruits"]
            session["breakfast_vegetables"] = breakfast_meal_info["vegetables"]
            session["lunch_details"] = lunch_meal_info["details"]
            session["lunch_proteins"] = lunch_meal_info["proteins"]
            session["lunch_fats"] = lunch_meal_info["fats"]
            session["lunch_fruits"] = lunch_meal_info["fruits"]
            session["lunch_vegetables"] = lunch_meal_info["vegetables"]
            session["dinner_details"] = dinner_meal_info["details"]
            session["dinner_proteins"] = dinner_meal_info["proteins"]
            session["dinner_fats"] = dinner_meal_info["fats"]
            session["dinner_fruits"] = dinner_meal_info["fruits"]
            session["dinner_vegetables"] = dinner_meal_info["vegetables"]
            session["snack_details"] = snack_meal_info["details"]
            session["snack_proteins"] = snack_meal_info["proteins"]
            session["snack_fats"] = snack_meal_info["fats"]
            session["snack_fruits"] = snack_meal_info["fruits"]
            session["snack_vegetables"] = snack_meal_info["vegetables"]
            
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
        return render_template("meal_details.html", day=date_obj, log_info=daily_log_info)
    return redirect("/")
