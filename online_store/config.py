"""Import dependencies."""
import os
from dotenv import load_dotenv


class Config(object):
    DEBUG = False
    TESTING = False
    # SECRET_KEY = os.environ["SECRET_KEY"]
    # SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TTL = True
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False

    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLISHABLE")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
