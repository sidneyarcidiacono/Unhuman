import os
import smtplib
import http.client
import mimetypes


def send_mail(subject, message, receiver="unhumanartist@gmail.com"):
    username = os.environ["MAIL_USERNAME"]
    password = os.environ["MAIL_PASSWORD"]

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)

        # Start tls for security
        s.starttls()

        s.login(username, password)
    except Exception as e:
        print("FAILED TO LOGIN, CHECK YOUR CREDENTIALS")

    # def send(self, receiver, message, subject=""):
    """Send email in the format

    {subject}
    Hi {receiver},
    {message}
    Returns False if any mail raises error"""

    message = f"""
    Subject: {subject}

    {message}
    """

    is_fail = False

    s.sendmail(
        username,
        receiver,
        message,
    )
    s.quit()

    return is_fail


if __name__ == "__main__":
    send_mail("Test", Test, "unhumanartist@gmail.com")
