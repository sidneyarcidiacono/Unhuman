"""Import packages."""
import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from online_store import app, db
from online_store.models import User, Product
from online_store.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    AddToCartForm,
)


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
    form = AddToCartForm()
    context = {"products": products, "form": form}
    return render_template("work.html", **context)


@app.route("/about")
def about():
    """Display about page."""
    return render_template("about.html")


@app.route("/cart")
@login_required
def user_cart():
    """Show user cart even after they've switched pages."""
    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", products=products)


@app.route("/cart/<int:product_id>", methods=["GET", "POST"])
def cart(product_id):
    """Show user's cart."""
    if current_user.is_authenticated:
        product = Product.query.get(product_id)
        product.user_id = current_user.id
        product.set_quantity()
        db.session.commit()
        flash("Added successfully")
        return redirect(url_for("user_cart"))
    flash("You must be logged in to add items.")
    return redirect(url_for("login"))


@app.route("/contact")
def contact_me():
    """Provide contact form for user."""
    return render_template("contact.html")


@app.route("/contact_results")
def contact_results():
    """Redirects user to submission confirmation."""
    return render_template("contact_results.html")


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
    print(current_user.avatar)
    form.username.data = current_user.username
    form.email.data = current_user.email
    context = {"title": "User", "form": form}
    return render_template("user.html", **context)


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
def admin():
    """Admin page where items can be added to db."""
    if current_user.is_admin():
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
            print(f"New product quan: {new_product.quantity}")
            db.session.add(new_product)
            db.session.commit()
            flash("Product added, thank you!")
            return redirect(url_for("admin"))
        products = Product.query.order_by(Product.date_created).all()
        context = {"products": products, "title": "Admin", "form": form}
        return render_template("admin.html", **context)
    flash("You are not authorized to access this route.")
    return redirect(url_for("login"))


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
