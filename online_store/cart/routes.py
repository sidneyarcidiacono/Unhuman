"""Import modules & packages."""
from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from online_store import db
from online_store.forms import RemoveFromCart, AddToCartForm
from online_store.models import Cart, Product
from online_store.cart.utils import (
    add_to_cart_helper,
    clear_cart_helper,
    remove_from_cart_helper,
)

cart = Blueprint("cart", __name__)


@cart.route("/")
@login_required
def user_cart():
    """Show user their cart."""
    form = RemoveFromCart()
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart is not None:
        context = {
            "products": cart.products,
            "quantity": cart.products_quantity,
            "subtotal": cart.subtotal,
            "form": form,
        }
        return render_template("cart.html", **context)
    return render_template("cart.html")


@cart.route("/<int:product_id>", methods=["GET", "POST"])
def show_cart(product_id):
    """Show user's cart."""
    form = AddToCartForm()
    if current_user.is_authenticated and form.validate_on_submit():
        quantity = form.quantity.data
        product = Product.query.get(product_id)
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart is not None:
            add_to_cart_helper(quantity, product, cart)
            db.session.commit()
            flash("Added successfully")
            return redirect(url_for("cart.user_cart"))
        else:
            cart = Cart(
                products=[],
                products_quantity=0,
                subtotal=0.0,
                user_id=current_user.id,
            )
            add_to_cart_helper(quantity, product, cart)
            db.session.add(cart)
            db.session.commit()
            flash("Added successfully")
            return redirect(url_for("cart.user_cart"))
    flash("You must be logged in to add items.")
    return redirect(url_for("users.login"))


@cart.route("/clear-cart")
def clear_cart():
    """Clear user's cart."""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    clear_cart_helper(cart)
    flash("Nothing to see here.")
    return redirect(url_for("cart.user_cart"))


@cart.route("/remove-item/<int:product_id>", methods=["GET", "POST"])
def remove_item_from_cart(product_id):
    """Remove individual product from cart."""
    form = RemoveFromCart()
    if form.validate_on_submit():
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        product = Product.query.get(product_id)
        remove_from_cart_helper(cart, product)
        db.session.commit()
        return redirect(url_for("cart.user_cart"))
    return redirect(url_for("cart.user_cart"))
