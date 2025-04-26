from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.db import db, Listing

"""
Blueprint for managing listings.

Routes:
  GET /listings:
    Retrieve all listings from the database.
    Returns:
      JSON list of listings with their details.

  POST /listings:
    Create a new listing in the database.
    Request Body (JSON):
      {
        "title": "Beautiful Apartment",
        "name": "Cozy Place",
        "description": "A cozy place to stay.",
        "photos": ["photo1.jpg", "photo2.jpg"],
        "price": 100.0,
        "host_id": 1
      }
    Returns:
      JSON response with success message.

  GET /listings/<int:id>:
    Retrieve a specific listing by ID.
    Returns:
      JSON object containing the listing's details.

  PATCH /listings/<int:id>:
    Update a specific listing by ID.
    Request Body (JSON):
      Any of the fields: title, name, description, photos, price.
    Returns:
      JSON response with success message.

  DELETE /listings/<int:id>:
    Delete a specific listing by ID.
    Returns:
      JSON response with success message.
"""

listings = Blueprint("listings", __name__)

@listings.route("/listings", methods=["GET"])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings]), 200

@listings.route("/listings", methods=["POST"])
def create_listing():
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

@listings.route("/listings/<int:id>", methods=["GET", "PATCH", "DELETE"])
def handle_listing(id):
    listing = Listing.query.get_or_404(id)

    if request.method == "GET":
        return jsonify(listing.to_dict()), 200

    elif request.method == "PATCH":
        data = request.get_json()
        listing.title = data.get("title", listing.title)
        listing.name = data.get("name", listing.name)
        listing.description = data.get("description", listing.description)
        listing.photos = ",".join(data.get("photos", listing.photos.split(",")))
        listing.price = data.get("price", listing.price)

        db.session.commit()
        return jsonify({"message": "Listing updated successfully"}), 200

    elif request.method == "DELETE":
        db.session.delete(listing)
        db.session.commit()
        return jsonify({"message": "Listing deleted successfully"}), 200

