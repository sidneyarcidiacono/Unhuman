import os
import smtplib
import http.client
import mimetypes

username = os.environ["MAIL_USERNAME"]
password = os.environ["MAIL_PASSWORD"]

print(f"Username: {username}")
print(f"Password: {password}")


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


# Send email using Trustifi for use with Heroku deployment


def send_email_trustifi(recipient_email, message, name, title):

    url = os.getenv("TRUSTIFI_URL") + "/api/i/v1/email"
    conn = http.client.HTTPSConnection("be.trustifi.com")

    payload = '{\n"from": {"email": "unhumanartist@gmail.com"},\n  "recipients": [{"email": "{{recipient_email}}", "name": "{{name}}"}}],\n  "lists": [],\n  "contacts": [],\n  "attachments": [],\n  "title": "{{title}}",\n  "html": "{{ message }}",\n  "methods": { \n    "postmark": false,\n    "secureSend": false,\n    "encryptContent": false,\n    "secureReply": false \n  }\n}'
    headers = {
        "x-trustifi-key": os.getenv("TRUSTIFI_KEY"),
        "x-trustifi-secret": os.getenv("TRUSTIFI_SECRET"),
        "Content-Type": "application/json",
    }

    conn.request("POST", "/api/i/v1/email", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(res)
    print(data.decode("utf-8"))
