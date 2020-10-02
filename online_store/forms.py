"""Import WTForms dependencies."""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    BooleanField,
    DecimalField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from online_store.models import User


class RegistrationForm(FlaskForm):
    """Create class registration form for user sign-up."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(max=20)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=7, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate that username is not already in use."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please try again.")

    def validate_email(self, email):
        """Validate that email is not already in use."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is already in use. Please try again."
            )


class UpdateAccountForm(FlaskForm):
    """Create class Profile so users can edit their profile."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    name = StringField("Name", validators=[Length(max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    avatar = FileField(
        "Update Avatar", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update Account")

    def validate_username(self, username):
        """Validate that username is not already in use."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please try again."
                )

    def validate_email(self, email):
        """Validate that email is not already in use."""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is already in use. Please try again."
                )


class LoginForm(FlaskForm):
    """Create login form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RequestPassReset(FlaskForm):
    """Create password reset request form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """Validate that the email is associated with a user."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account associated with this email, please sign up for an account."
            )


class ResetPasswordForm(FlaskForm):
    """Allow validated user to reset their password."""

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")


class AddProductForm(FlaskForm):
    """Create add product form."""

    title = StringField(
        "Title", validators=[DataRequired(), Length(min=2, max=30)]
    )
    price = DecimalField("Price", validators=[DataRequired()])
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=140)]
    )
    media = StringField(
        "Media", validators=[DataRequired(), Length(min=4, max=30)]
    )
    size = StringField(
        "Size", validators=[DataRequired(), Length(min=3, max=7)]
    )
    quantity = IntegerField("Quantity", validators=[NumberRange(max=150)])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Add Product")


class AddToCartForm(FlaskForm):
    """Create add to cart button."""

    quantity = IntegerField("Quantity", validators=[NumberRange(max=15)])
    submit = SubmitField("Add to Cart")


class ContactForm(FlaskForm):
    """Create form for sending contact email to admin."""

    name = StringField(
        "Your Name", validators=[DataRequired(), Length(min=2, max=40)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=2, max=140)]
    )
    submit = SubmitField("Send Message")
