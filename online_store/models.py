"""Import packages."""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from online_store import db, login_manager, app
from flask_login import UserMixin
from passlib.hash import sha256_crypt

# Set load user function that flask_login expects


@login_manager.user_loader
def load_user(id):
    """Define user callback for user_loader function."""
    return User.query.get(id)


########################################################################
#                   #db.Model classes                                  #
########################################################################


class Product(db.Model):
    """Define product class."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, default=1)
    description = db.Column(db.String(200), nullable=False)
    media = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        """Specify return val when printing Product."""
        return "<Product %r>" % self.id


class User(UserMixin, db.Model):
    """Define user class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=True)
    avatar = db.Column(db.String(30), nullable=False, default="default.jpg")
    orders = db.relationship("Product", backref="user", lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def is_authenticated(self):
        """Return true when called after verifying login."""
        return True

    def set_password(self, pass_one, pass_conf, name, email):
        """Return new user from User class."""
        self.password = sha256_crypt.hash(pass_one)

    def check_password(self, password):
        """Verify hashed password and inputted password."""
        return sha256_crypt.verify(password, self.password)
