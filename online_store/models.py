"""Import packages."""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from online_store import db, login_manager, app
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from sqlalchemy.orm import backref

# Set load user function to use flask-login


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
    price = db.Column(db.Numeric(scale=2), default=0, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    media = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    quant_in_cart = db.Column(db.Integer, default=0)
    image = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    carts = db.relationship("Cart", secondary="product_cart_link")

    def __repr__(self):
        """Specify return val when printing Product."""
        return f"{self.title}, ${self.price}"

    def __str__(self):
        """Specify return when showing Product."""
        return f"{self.title}, ${self.price}"


class ProductCartLink(db.Model):
    """Joining table for product and cart."""

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product = db.relationship(
        "Product", backref=backref("link", cascade="all, delete-orphan")
    )
    cart = db.relationship(
        "Cart", backref=backref("link", cascade="all, delete-orphan")
    )


class Cart(db.Model):
    """Create class Cart that holds items."""

    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship("Product", secondary="product_cart_link")
    products_quantity = db.Column(db.Integer, default=1, nullable=False)
    subtotal = db.Column(db.Float, default=0, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(UserMixin, db.Model):
    """Define user class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    avatar = db.Column(
        db.String(30),
        nullable=False,
        default="lucifer.jpeg",
    )
    cart = db.relationship(
        "Cart", cascade="all, delete", backref="user", lazy=True
    )
    date_created = db.Column(db.DateTime, default=datetime.now)

    def is_authenticated(self):
        """Return true when called after verifying login."""
        return True

    def set_password(self, password):
        """Return new user from User class."""
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        """Verify hashed password and inputted password."""
        return sha256_crypt.verify(password, self.password)

    def set_is_admin(self):
        """Set user to admin."""
        if self.email == "unhumanartist@gmail.com":
            self.is_admin = True

    def get_reset_token(self, expires_sec=900):
        """Enable 'forgot password' functionality."""
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        """Verify that the user enters the correct pass reset token."""
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
