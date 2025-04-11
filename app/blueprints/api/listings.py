from flask import Blueprint, jsonify, request

listings = Blueprint("listings", __name__)

from app.db import db
from app.db import Listing, Booking

@listings.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.all()
    return jsonify([
        {
            "id": listing.id,
            "title": listing.title,
            "name": listing.name,
            "description": listing.description,
            "photos": listing.photos.split(","),
            "price": listing.price,
            "host_id": listing.host_id
        }
        for listing in listings
    ])

@listings.route("/listings/<int:id>", methods=["GET", "PUT", "DELETE"])
def listing(id):
    listing = Listing.query.get_or_404(id)
    
    if request.method == "GET":
        return jsonify({
            "id": listing.id,
            "title": listing.title,
            "name": listing.name,
            "description": listing.description,
            "photos": listing.photos.split(","),
            "price": listing.price,
            "host_id": listing.host_id
        })
    
    elif request.method == "PUT":
        data = request.get_json()
        listing.title = data.get("title", listing.title)
        listing.name = data.get("name", listing.name)
        listing.description = data.get("description", listing.description)
        listing.photos = ",".join(data.get("photos", listing.photos.split(",")))
        listing.price = data.get("price", listing.price)
        
        db.session.commit()
        return jsonify({"message": "Listing updated successfully"})
    
    elif request.method == "DELETE":
        db.session.delete(listing)
        db.session.commit()
        return jsonify({"message": "Listing deleted successfully"})
    
@listings.route("/listings/<int:id>/bookings", methods=["GET", "POST", "DELETE"])
def booking(id):
    listing = Listing.query.get_or_404(id)
    
    if request.method == "GET":
        bookings = Booking.query.filter_by(listing_id=id).all()
        return jsonify([
            {
                "id": booking.id,
                "listing_id": booking.listing_id,
                "host_id": booking.host_id,
                "booker_id": booking.booker_id,
                "start_date": booking.start_date,
                "end_date": booking.end_date
            }
            for booking in bookings
        ])
    
    elif request.method == "POST":
        data = request.get_json()
        new_booking = Booking(
            listing_id=id,
            host_id=data["host_id"],
            booker_id=data["booker_id"],
            start_date=data["start_date"],
            end_date=data["end_date"]
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Booking created successfully"}), 201
    
    elif request.method == "DELETE":
        booking = Booking.query.filter_by(listing_id=id).first_or_404()
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"})

