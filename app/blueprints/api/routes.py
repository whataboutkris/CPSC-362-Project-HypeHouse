from flask import Blueprint
api = Blueprint("api", __name__)

from app.blueprints.api.listings import listings
from app.blueprints.api.auth import auth_blueprint

api.register_blueprint(listings) # /api/listings
api.register_blueprint(auth_blueprint) # /api/auth