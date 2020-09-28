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
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from online_store.models import User


class RegistrationForm(FlaskForm):
    """Create class registration form for user sign-up."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
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
    name = StringField("Name", validators=[DataRequired(), Length(max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    avatar = FileField(
        "Update Avatar", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Sign Up")

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
