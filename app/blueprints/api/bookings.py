from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import db, Listing, Booking, Message
from datetime import datetime
from flask import abort

bookings = Blueprint("bookings", __name__)

@bookings.route('/booking/<int:id>')
def booking_page(id):
    # Fetch the listing details from the database
    listing = Listing.query.get_or_404(id)
    return render_template('pages/booking.html', listing=listing)

@bookings.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    listing_id = request.form.get('listing_id')  
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Validate input
    if not listing_id or not start_date or not end_date:
        flash('Invalid booking details', 'error')
        print("booking error occured")
        return redirect(url_for('main.main.dashboard'))

    # Fetch the listing
    listing = Listing.query.get_or_404(listing_id)

    # Parse dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('booking_page', id=listing_id))

    # Create new booking
    new_booking = Booking( #this doesnt work currently, need the flask.loigin
        listing_id=listing.id,
        start_date=start_date,
        end_date=end_date,
        booker_id=current_user.id,
        host_id=listing.host_id
    )

    db.session.add(new_booking)
    db.session.commit()


    #print("booking somehow came thru")
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('main.dashboard'))

#Delete a booking
@bookings.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)

    # Make sure the user is allowed to cancel
    #if booking.booker_id != current_user.id:
        #return {"message": "Unauthorized"}, 403

    db.session.delete(booking)
    db.session.commit()

    return {"message": "Booking cancelled successfully!"}, 200

@bookings.route("/inbox/<booking_id>", methods=["GET", "POST"])
def inbox(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if current_user.id not in[booking.booker_id, booking.host_id]:
        abort(403)

    if request.method == "POST":
        content = request.form.get("message")
        if content:
            new_message = Message(
                booking_id=booking.id,
                sender_id=current_user.id,
                content=content
                )
            db.session.add(new_message)
            db.session.commit()
            flash("Message sent!", "Success")
        return redirect(url_for('bookings.inbox', booking_id=booking.id))
    
    messages = Message.query.filter_by(booking_id=booking.id).order_by(Message.timestamp)
    return render_template("pages/inbox.html", booking=booking, messages=messages)