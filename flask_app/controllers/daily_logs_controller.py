from flask_app import app
from flask import render_template, session, redirect

# DAILY LOG/TRACKER DISPLAY
@app.route("/daily_tracker/<date:date>")
def daily_tracker():
    if "id" in session:
        return render_template("daily_tracker.html")
    return redirect("/")


# DAILY LOG ADD/EDIT


# MEAL ADD/EDIT
@app.route("/meal/add/<date>/<meal_type>")
def update_meal(date, meal_type):
    if "id" in session:
        return redirect("/daily_tracker")
    return redirect("/")
