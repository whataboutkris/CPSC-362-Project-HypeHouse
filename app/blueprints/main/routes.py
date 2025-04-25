from datetime import datetime
from app.db import User, Listing, Booking, db
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, session, redirect, url_for, flash


main = Blueprint("main", __name__)

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

@main.route("/dashboard")
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
    

@main.route("/booking/<int:house_id>")
def booking(house_id):
    listing = {
        'id': house_id,
        'title': 'Sample House',
        'description': 'Sample description for this home.',
        'price': 150,
        'photos': "https://placehold.co/300x150"
    }
    owner = { 'name': 'Test Owner' }

    return render_template("pages/booking.html", house=listing, owner=owner)

@main.route("/confirm_booking", methods=["POST"])
def confirm_booking():
    listing_id = request.form['listing_id']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

    booker_id = session.get('user_id') or 1
    listing = Listing.query.get_or_404(listing_id)
    host_id = listing.host_id

    new_booking = Booking(
        listing_id=listing_id,
        host_id=host_id,
        booker_id=booker_id,
        start_date=start_date,
        end_date=end_date
    )

    db.session.add(new_booking)
    db.session.commit()

    redirect_target = request.args.get('redirect')
    if redirect_target == "bookings":
        return redirect("/dashboard#Bookings")
    return redirect(url_for('main.dashboard'))
