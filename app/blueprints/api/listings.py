from flask import Blueprint, jsonify, request

"""
Blueprint for managing listings and bookings.
Routes:
  /listings (GET):
    Retrieve all listings from the database.
    Returns:
      JSON response containing a list of all listings with their details.
  /listings/<int:id> (GET, PATCH, DELETE):
    Retrieve, update, or delete a specific listing by ID.
    Methods:
      GET: Retrieve details of a specific listing.
      PATCH: Update details of a specific listing.
      DELETE: Delete a specific listing from the database.
    Returns:
      JSON response with the details of the listing, or a success message for updates/deletes.
  /listings/<int:id> (POST):
    Create a new listing in the database.
    Request Body:
      JSON object containing the details of the new listing.
    Returns:
      JSON response with a success message.
    Example:
      {
        "title": "Beautiful Apartment",
        "name": "Cozy Place",
        "description": "A cozy place to stay.",
        "photos": ["photo1.jpg", "photo2.jpg"],
        "price": 100.0,
        "host_id": 1
      }
    Returns:
      JSON response with a success message.
    Example:
      {
        "message": "Listing created successfully"
      }
"""

listings = Blueprint("listings", __name__)

from app.db import db
from app.db import Listing

@listings.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listings.to_dict() for listing in listings]), 200

@listings.route("/listings/<int:id>", methods=["GET", "POST", "PATCH", "DELETE"])
def listing(id):
    listing = Listing.query.get_or_404(id)
    
    if request.method == "GET":
        return jsonify(listing.to_dict()), 200
    
    elif request.method == "POST":
        data = request.get_json()
        new_listing = Listing(
            title=data["title"],
            name=data["name"],
            description=data["description"],
            photos=",".join(data["photos"]),
            price=data["price"],
            host_id=data["host_id"]
        )
        db.session.add(new_listing)
        db.session.commit()
        return jsonify({"message": "Listing created successfully"}), 201
    
    elif request.method == "PATCH":
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
