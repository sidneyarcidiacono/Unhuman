"""Import modules & packages."""
from online_store.models import User
from online_store.send_email import send_mail

# Define function that sends email to admin from contact form


def send_contact_email(message, email, name):
    """Send email to my address when someone submits the contact form."""
    admin = User.query.filter_by(email="unhumanartist@gmail.com").first()
    recipient_email = admin.email
    msg = message + f"Sender email: {email}"
    send_mail("Contact Form Submission", msg, recipient_email)
