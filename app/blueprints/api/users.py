from flask import Blueprint, jsonify, request

users = Blueprint("users", __name__)

from app.db import db
from app.db import User

@users.route("/users", methods=["GET"])
def get_users():
    """Get all users."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# handle user creation somewhere else? (maybe) --> creation handled in auth.py

@users.route("/users/<int:id>", methods=["GET", "PATCH", "DELETE"])
def user(id):
    user = User.query.get_or_404(id)                    
    
    if request.method == "GET":
        return jsonify(user.to_dict()), 200
    
    elif request.method == "PATCH":
        data = request.get_json()
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        user.is_host = data.get("is_host", user.is_host)
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    
    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200