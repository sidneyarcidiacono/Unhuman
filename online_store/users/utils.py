"""Import modules & packages."""
import os
import secrets
from online_store import app
from PIL import Image
from online_store.models import User
from online_store.send_email import send_mail
from flask import url_for

# Define a function that sends password reset email


def send_reset_email(user):
    """Send password reset email."""
    token = user.get_reset_token()
    msg = f"""
                To reset your password, please click the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request, please ignore this email."""
    send_mail("Reset Password", msg, user.email)


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
