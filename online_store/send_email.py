import os
import smtplib

username = os.environ["MAIL_USERNAME"]
password = os.environ["MAIL_PASSWORD"]


class SendMail:
    """Sends email to admin or user."""

    def __init__(self):
        """Initialize username and password for gmail account."""
        self.username = username
        self.password = password

        try:
            self.s = smtplib.SMTP("smtp.gmail.com", 587)

            self.s.ehlo()

            # Start tls for security
            self.s.starttls()

            self.s.login(self.username, self.password)
        except Exception as e:
            print("FAILED TO LOGIN, CHECK YOUR CREDENTIALS")

        def send(self, receiver, message, subject=""):
            """Send email in the format

            {subject}
            Hi {receiver},
            {message}
            Returns False if any mail raises error"""

            is_fail = False

            message = f"""\
            Subject: {subject}

            Hi {receiver},

            {message}
            """
            if self.s.sendmail(self.username, receiver, message) != {}:
                is_fail = True

            return is_fail
