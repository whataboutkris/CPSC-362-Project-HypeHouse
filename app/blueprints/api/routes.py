from flask import Blueprint
api = Blueprint("api", __name__)

from app.blueprints.api.listings import listings
from app.blueprints.api.bookings import property_blueprint

api.register_blueprint(listings) # /api/listings
api.register_blueprint(property_blueprint) # /api/bookings