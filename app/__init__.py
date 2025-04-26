from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

'''
We import all the blueprints that we created in the blueprints folder.
This creates abstract routes that we can use in the app.
'''
from app.blueprints.api import api
from app.blueprints.main import main
from app.blueprints.htmx import htmx
from app.blueprints.api.auth import auth_blueprint
from app.blueprints.api.listings import listings

from .db import db  # Import db object from db.py
login_manager = LoginManager() #login 

'''
This is the main file that will run the app. It will create the app and set the config for the database.
'''
def create_app():

  app = Flask(__name__)

  # TODO: set config from environment variables
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
  app.config['SECRET_KEY'] = 'your-secret-key' #
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["TEMPLATES_AUTO_RELOAD"] = True

  db.init_app(app)

  '''
  app.before_first_response: means the first thing done is that the data base will create a table containing
  the user's information, first name, last name, email, and a hashed password.
  '''

  login_manager.init_app(app) #init extension

  from app.db import User #import here in case of circular imports

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
     
  with app.app_context():
      db.create_all()  # Ensure tables are created

  app.register_blueprint(main) # Main blueprint is routing for the views and templates
  app.register_blueprint(listings, url_prefix="/api")
  app.register_blueprint(api, url_prefix="/api") # API blueprint is routing for the API
  app.register_blueprint(htmx, url_prefix="/htmx") # HTMX blueprint is routing for the HTMX calls
  app.register_blueprint(auth_blueprint, url_prefix="/auth")

  return app