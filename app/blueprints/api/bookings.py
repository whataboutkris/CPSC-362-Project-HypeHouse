from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import db, Listing, Booking

bookings = Blueprint("bookings", __name__)

@bookings.route('/booking/<int:id>')
def booking_page(id):
    # Fetch the listing details from the database
    listing = Listing.query.get_or_404(id)
    return render_template('pages/booking.html', listing=listing)

@bookings.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    id = request.form.get('id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Validate input
    if not id or not start_date or not end_date:
        flash('Invalid booking details', 'error')
        return redirect(url_for('main.dashboard'))  # ← better: just send them back to dashboard

    # Fetch the listing
    listing = Listing.query.get_or_404(id)

    # Create new booking
    new_booking = Booking(
        id=listing.id,
        date_start=start_date,
        date_end=end_date,
        booker_id=current_user.id,
        host_id=listing.host_id
    )

    db.session.add(new_booking)
    db.session.commit()

    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('dashboard'))