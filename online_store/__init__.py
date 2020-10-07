"""Import packages."""
import os
import stripe
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from online_store.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mail = Mail(app)

stripe.api_key = os.getenv("STRIPE_SECRET")

# Define flask-login config variables & instantiate LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from online_store import routes

with app.app_context():
    db.create_all()
