"""Import WTForms dependencies."""
from wtforms import Form, StringField, BooleanField, validators


class RegistrationForm(Form):
    """Create class registration form for user sign-up."""

    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = StringField('Password', [validators.Length(min=8, max=20)])


class ProfileForm(RegistrationForm):
    """Create class Profile so users can add bio."""

    bio = StringField('Bio', [validators.Length(min=10, max=140)])
