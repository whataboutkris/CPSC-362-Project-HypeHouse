# app/db.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the db object
db = SQLAlchemy()

'''
class User:
    id, first_name, last_name, email, password_hash
    id = primary key
    name = first_name + last_name
    email = unique
    password_hash = hashed password
    phone_number = unique
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    phone_number = db.Column(db.String(15), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)

'''
class Session:
    id, user_id, token, expiration
    id = primary key
    user_id = foreign key to User table
    token = unique session token
    expiration = datetime of when the session expires
'''
class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # Foreign key to User table
    token = db.Column(db.String(128), nullable = False)
    expiration = db.Column(db.DateTime, nullable = False)

'''
class Listing:
    id, title, name, description, photos, price, host_id
    id = primary key
    title = title of the listing
    name = name of the listing
    description = description of the listing
    photos = photos of the listing (assuming stored as a comma-separated string)
'''
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    photos = db.Column(db.String(500), nullable = False)  # Assuming photos are stored as a comma-separated string
    price = db.Column(db.Float, nullable = False)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # Foreign key to User table

'''
class Booking:
    id, listing_id, host_id, booker_id, start_date, end_date
    id = primary key
    listing_id = foreign key to Listing table
    host_id = foreign key to User table
    booker_id = foreign key to User table
    start_date = start date of the booking
    end_date = end date of the booking
'''
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable = False)  # Foreign key to Listing table
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # Foreign key to User table
    booker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # Foreign key to User table
    start_date = db.Column(db.DateTime, nullable = False)
    end_date = db.Column(db.DateTime, nullable = False)