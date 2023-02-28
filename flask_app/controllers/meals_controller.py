from flask_app import app
from flask import session, redirect


# MEAL ADD/EDIT
@app.route("/meal/update/<date>/<meal_type>", methods=["POST"])
def update_meal(date, meal_type):
    if "id" in session:
        # validate meal entry
        #   if valid, determine if new entry (insert) or updated entry (update)
        return redirect(f"/daily_tracker/{date}")
    return redirect("/")
