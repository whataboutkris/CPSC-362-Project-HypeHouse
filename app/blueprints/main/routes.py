from datetime import datetime
from app.db import User, Listing, Booking, db
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.blueprints.main import main

booking_db = []

@main.route("/")
def index():
    # return index.html
    print("Index route was called")
    return render_template("pages/splash.html")

@main.route("/login", methods=["GET", "POST"])
def login_page():
    print ("Login route was")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Admin credentials (username: admin, password: admin)
        if username == "admin" and password == "admin":
            # Redirect to dashboard if the credentials are correct
            return redirect(url_for('main.dashboard'))
        else:
            # Flash an error message if the credentials are incorrect
            flash("The username/password is incorrect.", "error")
            return render_template("pages/login.html")
    
    return render_template("pages/login.html")

@main.route("/register", methods=["GET"])
def register_page():
    return render_template("pages/register.html")

@main.route("/about")
def about_page():
    return render_template("pages/about.html")

@main.route("/dashboard", methods=["GET", "POST"])
#if you're here, you should have "host" privileges!
def dashboard():
    listings = Listing.query.all() 
    bookings = Booking.query.all()
    image_list = [
        "https://www.houseplans.net/news/wp-content/uploads/2023/07/57260-768.jpeg",
        "https://media.timeout.com/images/105931772/750/562/image.jpg",
        "https://miro.medium.com/v2/resize:fit:4400/1*BOiBE_Aib2o1nulkFqdcGA.jpeg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToQzZZNZxA5kW3grRqMm5GcCqRVRve7liCIw&s",
        "https://i.pinimg.com/736x/2d/7d/41/2d7d414222ac5baba7b529d596e7f0b8.jpg"
        
    ]
    if request.method == "POST":
        # Add new listing functionality here (if needed)
        pass

    return render_template("pages/dashboard.html", listings=listings, bookings = bookings)

    #return render_template("pages/dashboard.html", image_list=image_list)

