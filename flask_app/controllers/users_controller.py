from flask_app import app   
from flask import render_template, session, redirect

@app.route("/")
def home():
    if "id" in session:
        return render_template("home.html")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    return redirect ("dashboard.html")

@app.route("/sign_up", methods=["POST"])
def sign_up():
    return redirect ("account.html")







@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")