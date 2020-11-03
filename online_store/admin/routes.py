"""Module & package import."""
from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required
from online_store import db
from online_store.forms import AddProductForm
from online_store.admin.utils import admin_required
from online_store.users.utils import save_image
from online_store.models import Product

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def show_admin():
    """Admin page where items can be added to db."""
    form = AddProductForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data, 1200, "assets")
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
        return redirect(url_for("admin.show_admin"))
    products = Product.query.order_by(Product.date_created).all()
    context = {"products": products, "title": "Admin", "form": form}
    return render_template("admin.html", **context)


@admin.route("/admin-delete/<product_id>")
def delete_product(product_id):
    """Delete products from database."""
    try:
        product_to_delete = Product.query.filter_by(id=product_id).first()
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for("admin.show_admin"))
    except (TypeError, ValueError):
        print("Something went wrong deleting this product.")
        return redirect(url_for("admin.show_admin"))
