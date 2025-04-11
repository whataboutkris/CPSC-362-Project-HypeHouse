from flask import Blueprint, jsonify, request

"""
Blueprint for managing listings and bookings.
Routes:
  /listings (GET):
    Retrieve all listings from the database.
    Returns:
      JSON response containing a list of all listings with their details.
  /listings/<int:id> (GET, PUT, DELETE):
    - GET:
      Retrieve a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing to retrieve.
      Returns:
        JSON response containing the details of the specified listing.
    - PUT:
      Update a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing to update.
        JSON body:
          title (str, optional): The new title of the listing.
          name (str, optional): The new name of the listing.
          description (str, optional): The new description of the listing.
          photos (list of str, optional): The new photos of the listing.
          price (float, optional): The new price of the listing.
      Returns:
        JSON response with a success message upon successful update.
    - DELETE:
      Delete a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing to delete.
      Returns:
        JSON response with a success message upon successful deletion.
  /listings/<int:id>/bookings (GET, POST, DELETE):
    - GET:
      Retrieve all bookings for a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing whose bookings are to be retrieved.
      Returns:
        JSON response containing a list of all bookings for the specified listing.
    - POST:
      Create a new booking for a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing to create a booking for.
        JSON body:
          host_id (int): The ID of the host for the booking.
          booker_id (int): The ID of the booker for the booking.
          start_date (str): The start date of the booking (YYYY-MM-DD format).
          end_date (str): The end date of the booking (YYYY-MM-DD format).
      Returns:
        JSON response with a success message upon successful creation of the booking.
    - DELETE:
      Delete the first booking for a specific listing by its ID.
      Parameters:
        id (int): The ID of the listing whose booking is to be deleted.
      Returns:
        JSON response with a success message upon successful deletion of the booking.
"""

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

