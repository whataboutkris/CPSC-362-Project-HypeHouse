from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    # return index.html
    print("Index route was called")
    return render_template("pages/index.html")

@main.route("/login")
def login_page():
    return render_template("pages/login.html")

@main.route("/dashboard")
def dashboard():
    return render_template("pages/dashboard.html")