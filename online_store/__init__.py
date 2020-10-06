"""Import packages."""
import os
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import boto3

s3 = boto3.resource("s3")

from boto3 import S3Connection

s3 = S3Connection(
    os.environ["SECRET_KEY"],
    os.environ["SQLALCHEMY_DATABASE_URI"],
    os.environ["MAIL_DEFAULT_SENDER"],
    os.environ["MAIL_PASSWORD"],
    os.environ["MAIL_USERNAME"],
    os.environ["STRIPE_SECRET"],
)


app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail(app)

stripe.api_key = S3Connection(os.environ["STRIPE_PUBLIC_KEY"])

# Define flask-login config variables & instantiate LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from online_store import routes

with app.app_context():
    db.create_all()
