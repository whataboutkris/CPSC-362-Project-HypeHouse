from flask import Blueprint, jsonify, request
from flask_login import login_required

property_blueprint = Blueprint('property', __name__)

# SAMPLE 
bookings = [
    {
        "id": 1,
        "listing_id": 101,
        "date_start": "2025-04-15",
        "date_end": "2025-04-20",
        "booker_id": 123,
        "host_id": 321
    }
]

'''
Shows all bookings
'''
@property_blueprint.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    return jsonify(bookings)


'''
Creates a new booking
'''
@property_blueprint.route('/bookings', methods=['POST'])
@login_required
def add_booking():
    new_booking = request.json
    bookings.append(new_booking)
    return jsonify(new_booking), 201

'''
Deletes an existing booking
'''
@property_blueprint.route('/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if booking:
        bookings.remove(booking)
        return jsonify({"message": "Booking deleted"})
    return jsonify({"error": "Booking not found"}), 404

