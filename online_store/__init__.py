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
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from online_store.users.routes import users
from online_store.main.routes import main
from online_store.cart.routes import cart
from online_store.admin.routes import admin
from online_store.checkout.routes import checkout
from online_store.errors.routes import error

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(cart, url_prefix="/cart")
app.register_blueprint(admin)
app.register_blueprint(checkout)
app.register_blueprint(error)

with app.app_context():
    db.create_all()
