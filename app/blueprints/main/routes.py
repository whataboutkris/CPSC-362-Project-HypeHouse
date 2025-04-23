from datetime import datetime
from app.db import User, Listing, Booking, db
from flask import Blueprint, render_template, request, session, redirect, url_for, flash


main = Blueprint("main", __name__)

@main.route("/")
def index():
    # return index.html
    print("Index route was called")
    return render_template("pages/index.html")

@main.route("/login")
def login_page():
    print("Login route was called.")
    return render_template("pages/login.html")

@main.route("/dashboard")
def dashboard():
    listings = Listing.query.all() 
    image_list = [
        "https://www.houseplans.net/news/wp-content/uploads/2023/07/57260-768.jpeg",
        "https://media.timeout.com/images/105931772/750/562/image.jpg",
        "https://miro.medium.com/v2/resize:fit:4400/1*BOiBE_Aib2o1nulkFqdcGA.jpeg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToQzZZNZxA5kW3grRqMm5GcCqRVRve7liCIw&s",
        "https://i.pinimg.com/736x/2d/7d/41/2d7d414222ac5baba7b529d596e7f0b8.jpg"
        
    ]
    return render_template("pages/dashboard.html", image_list=image_list)

@main.route("/booking/<int:house_id>")
def booking(house_id):
    listing = Listing.query.get_or_404(house_id)
    owner = User.query.get(listing.host_id)
    return render_template("pages/booking.html", house=listing, owner=owner)

@main.route("/confirm_booking", methods=["POST"])
def confirm_booking():
    listing_id = request.form['listing_id']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    booker_id = session.get('user_id')  # or current_user.id if using Flask-Login

    listing = Listing.query.get_or_404(listing_id)
    host_id = listing.owner_id

    new_booking = Booking(
        listing_id=listing_id,
        host_id=host_id,
        booker_id=booker_id,
        start_date=start_date,
        end_date=end_date
    )

    db.session.add(new_booking)
    db.session.commit()

    flash('✅ Booking confirmed!')
    return redirect(url_for('dashboard'))