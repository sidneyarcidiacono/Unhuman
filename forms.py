"""Import WTForms dependencies."""
from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    """Create class registration form for user sign-up."""

    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=8, max=20)])


class ProfileForm(RegistrationForm):
    """Create class Profile so users can add bio."""

    bio = StringField('Bio', [validators.Length(min=10, max=140)])


class LoginForm(Form):
    """Create login form."""

    username = StringField('Username')
    password = PasswordField('Password')
