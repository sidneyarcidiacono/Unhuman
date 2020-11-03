"""Module & package import."""
from flask import Blueprint, render_template

error = Blueprint("error", __name__)


@error.errorhandler(404)
def show404(err):
    """Show 404 page."""
    return render_template("404.html")
