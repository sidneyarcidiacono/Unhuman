"""Import modules & packages."""
from flask import Blueprint, render_template
from online_store.models import Product
from online_store.forms import AddToCartForm, ContactForm
from online_store.main.utils import send_contact_email

main = Blueprint("main", __name__)


@main.route("/")
def homepage():
    """Display homepage."""
    return render_template("home.html")


@main.route("/work")
def shop_paintings():
    """Render template for artwork/product page."""
    products = Product.query.all()
    for prod in products:
        print(prod)
    form = AddToCartForm()
    context = {"products": products, "form": form}
    return render_template("work.html", **context)


@main.route("/about")
def about():
    """Display about page."""
    return render_template("about.html")


@main.route("/contact")
def contact_me():
    """Provide contact form for user."""
    form = ContactForm()
    return render_template("contact.html", form=form)


@main.route("/contact_results", methods=["GET", "POST"])
def contact_results():
    """Redirects user to submission confirmation."""
    form = ContactForm()
    if form.validate_on_submit():
        message = form.message.data
        email = form.email.data
        name = form.name.data
        send_contact_email(message, email, name)
    return render_template("contact_results.html")
