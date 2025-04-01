from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#this create the data base using SQLAlchemy
db = SQLAlchemy(app)

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

'''
app.before_first_response: means the first thing done is that the data base will create a table containing
the user's information, first name, last name, email, and a hashed password.
'''
with app.app_context():
    db.create_all()

'''
app.route: in this case when the URL directory "/add_user" is at the end, we check if there is an existing user
           if there is an exisiting user, the error message "Email is already in use" will be displayed. If the
           email is not being in use, the user's password gets hashed by the werkzeug's generate_password_hash. 
           the users first name, last name, email and the HASHED password gets stored in the data base
'''
@app.route("/add_user", methods = ["POST"])
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
app.route: "/users" will return every user's cell number, first name, last name, and email
'''
@app.route("/users", methods = ["GET"])
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
app.route: "/login" first thing that it does is filter through the email column to check if the email is in use
           if it returns an error saying that the email is not recognized, then checks the hashed password with the 
           stored hashed password.
'''
@app.route("/login", methods = ["POST"])
def login():
    data = request
    user_login = User.query.filter_by(email = data["email"]).first()
    if not User:
        return jsonify({"error": "This email is not recognized."}), 400
    if not check_password_hash(User.password_hash, data["password"]):
        return jsonify({"error": "Incorrect password."})
    return jsonify({"message": f"Welcome back"})



if __name__ == "__main__":
    app.run(debug = True)