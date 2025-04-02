from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.db import User  # Import User model directly from db.py

api = Blueprint("api", __name__)

'''
api.route: in this case when the URL directory "/add_user" is at the end, we check if there is an existing user
           if there is an exisiting user, the error message "Email is already in use" will be displayed. If the
           email is not being in use, the user's password gets hashed by the werkzeug's generate_password_hash. 
           the users first name, last name, email and the HASHED password gets stored in the data base
'''

@api.route("/add_user", methods = ["POST"])
def add_user():
    data = request.json
    existing_user = User.query.filter_by(email = data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email is already in use"}), 400
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        first_name = data["first_name"],
        last_name = data["last_name"],
        email = data["email"],
        password_hash = hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added"}), 201

'''
api.route: "/users" will return every user's cell number, first name, last name, and email
'''
@api.route("/users", methods = ["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id" : user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        for user in users
    ])

'''
api.route: "/login" first thing that it does is filter through the email column to check if the email is in use
           if it returns an error saying that the email is not recognized, then checks the hashed password with the 
           stored hashed password.
'''
@api.route("/login", methods = ["POST"])
def login():
    data = request
    user_login = User.query.filter_by(email = data["email"]).first()
    if not User:
        return jsonify({"error": "This email is not recognized."}), 400
    if not check_password_hash(User.password_hash, data["password"]):
        return jsonify({"error": "Incorrect password."})
    return jsonify({"message": f"Welcome back"})
