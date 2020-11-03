"""Import modules & packages."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from flask_login import login_user, current_user, logout_user, login_required
from online_store import db
from online_store.models import User
from online_store.forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
    RequestPassReset,
    ResetPasswordForm,
)
from online_store.users.utils import send_reset_email, save_image

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Login user."""
    if current_user.is_authenticated:
        redirect(url_for("main.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.homepage"))
            )
        flash("Unable to log in. Please check email and password.")
    return render_template("login.html", title="Login", form=form)


@users.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/user", methods=["GET", "POST"])
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
        return redirect(url_for("users.user"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    context = {"title": "User", "form": form}
    return render_template("user.html", **context)


@users.route("/user/delete-profile")
@login_required
def delete_user():
    """Allow user to delete their profile."""
    user = User.query.filter_by(id=current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash("Profile deleted successfully, we're sad to see you go!")
    return redirect(url_for("main.homepage"))


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Show route for requesting user password reset."""
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = RequestPassReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to reset your password.")
        return redirect(url_for("users.login"))
    context = {"title": "Request Password Reset", "form": form}
    return render_template("reset_request.html", **context)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Reset user password."""
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Token is invalid or expired")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been resett. You are now able to log in.")
        return redirect(url_for("users.login"))
    context = {"title": "Reset Password", "form": form}
    return render_template("reset_token.html", **context)


@users.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("main.homepage"))
