"""Import packages."""
import os
import secrets
import stripe
from PIL import Image
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
)
from flask_login import login_user, current_user, logout_user, login_required
from online_store import app, db, login_manager
from online_store.models import User, Product, Cart
from online_store.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    AddToCartForm,
    RequestPassReset,
    ResetPasswordForm,
    ContactForm,
    RemoveFromCart,
)
from flask_mail import Message
from online_store import mail
from functools import wraps

########################################################################
#                   #Helper functions                                  #
########################################################################

# Define function to handle image uploads


def save_image(form_image, size, folder):
    """Save avatar upload to static."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(
        app.root_path, f"static/{folder}", image_filename
    )
    output_size = (size, size)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_filename


# Define a function that sends password reset email


def send_reset_email(user):
    """Send password reset email."""
    token = user.get_reset_token()
    msg = Message("Password Reset", recipients=[user.email])
    msg.body = f"""
                To reset your password, please click the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request, please ignore this email."""
    mail.send(msg)


# Define function that sends email to admin from contact form


def send_contact_email(message, email):
    """Send email to my address when someone submits the contact form."""
    admin = User.query.filter_by(email="unhumanartist@gmail.com").first()
    msg = Message("Contact Form Submission", recipients=[admin.email])
    msg.body = message + email
    mail.send(msg)


# Create decorator for routes that require admin role


def admin_required(func):
    """Decorate route function to check is user isadmin."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return login_manager.unauthorized()

    return wrapper


# Set product quantity when adding to cart


def set_product_quantity(product, quant_added):
    """Set quantity and make adj. to title when out of stock."""
    if product.quantity > 0:
        product.quantity -= int(quant_added)
        return product.quantity
    return product.quantity


# Helper function for executing adding items to cart & totalling prices


def update_cart_subtotal(cart):
    """Update cart subtotal when new items are added."""
    product_total = 0

    for product in cart.products:
        product_total += product.price * product.quant_in_cart

    cart.subtotal = product_total
    db.session.commit()
    return cart.subtotal


def add_to_cart_helper(quantity, product, cart):
    """
    Increment product quantity in cart and append new prod to cart.

    Call set product quantity on product.
    """
    cart.products.append(product)
    cart.products_quantity += quantity
    product.quant_in_cart += quantity
    db.session.commit()

    set_product_quantity(product, quantity)
    update_cart_subtotal(cart)
    return cart, product


def clear_cart_helper(cart):
    """Clear cart on checkout or when empty cart button is pushed."""
    for product in cart.products:
        product.quant_in_cart = 0
    db.session.delete(cart)
    db.session.commit()
    return


def remove_from_cart_helper(cart, product):
    """Adjust quantities when item is removed from cart."""
    cart.products.pop(cart.products.index(product))
    product.quantity += product.quant_in_cart
    product.quant_in_cart = 0
    cart.products_quantity -= 1
    return cart


########################################################################
#                   #Error Handling                                    #
########################################################################


@app.errorhandler(404)
def page_not_found(e):
    """Return custom 404 template."""
    print(e)
    return render_template("404.html")


########################################################################
#                   #Public Routes                                     #
########################################################################


@app.route("/")
def homepage():
    """Display homepage."""
    return render_template("home.html")


@app.route("/work")
def shop_paintings():
    """Render template for artwork/product page."""
    products = Product.query.all()
    for prod in products:
        print(prod)
    form = AddToCartForm()
    context = {"products": products, "form": form}
    return render_template("work.html", **context)


@app.route("/about")
def about():
    """Display about page."""
    return render_template("about.html")


@app.route("/contact")
def contact_me():
    """Provide contact form for user."""
    form = ContactForm()
    return render_template("contact.html", form=form)


@app.route("/contact_results", methods=["GET", "POST"])
def contact_results():
    """Redirects user to submission confirmation."""
    form = ContactForm()
    if form.validate_on_submit():
        message = form.message.data
        email = form.email.data
        send_contact_email(message, email)
    return render_template("contact_results.html")


########################################################################
#                   #Cart Routes                                       #
########################################################################


@app.route("/cart")
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


@app.route("/cart/<int:product_id>", methods=["GET", "POST"])
def cart(product_id):
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
            return redirect(url_for("user_cart"))
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
            return redirect(url_for("user_cart"))
    flash("You must be logged in to add items.")
    return redirect(url_for("login"))


@app.route("/clear-cart")
def clear_cart():
    """Clear user's cart."""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    clear_cart_helper(cart)
    flash("Nothing to see here.")
    return redirect(url_for("user_cart"))


@app.route("/cart/remove-item/<int:product_id>", methods=["GET", "POST"])
def remove_item_from_cart(product_id):
    """Remove individual product from cart."""
    form = RemoveFromCart()
    if form.validate_on_submit():
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        product = Product.query.get(product_id)
        remove_from_cart_helper(cart, product)
        db.session.commit()
        return redirect(url_for("user_cart"))
    return redirect(url_for("user_cart"))


########################################################################
#                   #Checkout Routes                                   #
########################################################################


@app.route("/create_session", methods=["POST"])
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
            success_url="http://localhost:5000/checkout_success",
            cancel_url="http://localhost:5000/checkout_cancel",
        )
        clear_cart_helper(cart)
        db.session.commit()
        return jsonify(id=checkout_session.id)
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/checkout_success")
def success():
    """Return success page after user checkout."""
    return render_template("success.html")


@app.route("/checkout_cancel")
def cancel():
    """Return cancel page if user cancels checkout."""
    return render_template("cancel.html")


########################################################################
#                   #User & Login routes                               #
########################################################################


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user."""
    if current_user.is_authenticated:
        redirect(url_for("homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("homepage"))
            )
        flash("Unable to log in. Please check email and password.")
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Sign up user."""
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        user.set_is_admin()
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created, you are now able to log in.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    """Show user account information."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_image(form.avatar.data, 125, "avatars")
            current_user.avatar = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.")
        return redirect(url_for("user"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    context = {"title": "User", "form": form}
    return render_template("user.html", **context)


@app.route("/user/delete-profile")
@login_required
def delete_user():
    """Allow user to delete their profile."""
    user = User.query.filter_by(id=current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash("Profile deleted successfully, we're sad to see you go!")
    return redirect(url_for("homepage"))


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Show route for requesting user password reset."""
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    form = RequestPassReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to reset your password.")
        return redirect(url_for("login"))
    context = {"title": "Request Password Reset", "form": form}
    return render_template("reset_request.html", **context)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Reset user password."""
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Token is invalid or expired")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been resett. You are now able to log in.")
        return redirect(url_for("login"))
    context = {"title": "Reset Password", "form": form}
    return render_template("reset_token.html", **context)


@app.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("homepage"))


########################################################################
#                   #Admin Routes                                      #
########################################################################


@app.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def admin():
    """Admin page where items can be added to db."""
    form = AddProductForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data, 500, "assets")
        new_product = Product(
            title=form.title.data,
            price=form.price.data,
            description=form.description.data,
            media=form.media.data,
            size=form.size.data,
            quantity=form.quantity.data,
            image=image_file,
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added, thank you!")
        return redirect(url_for("admin"))
    products = Product.query.order_by(Product.date_created).all()
    context = {"products": products, "title": "Admin", "form": form}
    return render_template("admin.html", **context)


@app.route("/admin-delete/<product_id>")
def delete_product(product_id):
    """Delete products from database."""
    try:
        product_to_delete = Product.query.filter_by(id=product_id).first()
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for("admin"))
    except (TypeError, ValueError):
        print("Something went wrong deleting this product.")
        return redirect(url_for("admin"))
