# app/db.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the db object
db = SQLAlchemy()

'''
This part below is the model that the data base will be using.
id: (integer, primary key is turned on), Primary key is a way to be able to fast search specific accounts
first_name: users first name up to 100 characters, nullable means that this WILL NOT be left blank
last_name: users last name up to 100 characters, nullable means that this WILL NOT be left blank
email: users email, will be the main way to log on. unique means that every cell in the table would not 
       contain any duplicates
passowrd: password would be up to 128 characters
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
