"""Package & module import."""
import stripe
from flask import Blueprint, jsonify, render_template
from flask_login import current_user
from online_store import db
from online_store.models import Cart
from online_store.cart.utils import clear_cart_helper

checkout = Blueprint("checkout", __name__)


@checkout.route("/create_session", methods=["POST"])
def create_checkout_session():
    """Send user to stripe checkout."""
    try:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        name = "".join([product.title for product in cart.products])
        price = cart.subtotal
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price * 100),
                        "product_data": {
                            "name": f"{name}",
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://www.unhumanart.com/checkout_success",
            cancel_url="https://www.unhumanart.com/checkout_cancel",
        )
        clear_cart_helper(cart)
        db.session.commit()
        return jsonify(id=checkout_session.id)
    except Exception as e:
        return jsonify(error=str(e)), 403


@checkout.route("/checkout_success")
def success():
    """Return success page after user checkout."""
    return render_template("success.html")


@checkout.route("/checkout_cancel")
def cancel():
    """Return cancel page if user cancels checkout."""
    return render_template("cancel.html")
