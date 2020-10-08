import os
import smtplib
import http.client
import mimetypes

username = os.environ["MAIL_USERNAME"]
password = os.environ["MAIL_PASSWORD"]


def send_mail(subject, message, receiver="unhumanartist@gmail.com"):

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)

        # s.ehlo()

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

    is_fail = False

    s.sendmail(
        username,
        receiver,
        message,
    )
    s.quit()

    return is_fail


if __name__ == "__main__":
    send_mail("Test", "Test", "unhumanartist@gmail.com")


# Send email using Trustifi for use with Heroku deployment


# def send_email_trustifi(recipient_email, message, name, title):
#
#     url = os.getenv("TRUSTIFI_URL") + "/api/i/v1/email"
#     conn = http.client.HTTPSConnection("be.trustifi.com")
#
#     payload = '{\n"from": {"email": "unhumanartist@gmail.com"},\n  "recipients": [{"email": "{{recipient_email}}", "name": "{{name}}"}}],\n  "lists": [],\n  "contacts": [],\n  "attachments": [],\n  "title": "{{title}}",\n  "html": "{{ message }}",\n  "methods": { \n    "postmark": false,\n    "secureSend": false,\n    "encryptContent": false,\n    "secureReply": false \n  }\n}'
#     headers = {
#         "x-trustifi-key": os.getenv("TRUSTIFI_KEY"),
#         "x-trustifi-secret": os.getenv("TRUSTIFI_SECRET"),
#         "Content-Type": "application/json",
#     }
#
#     conn.request("POST", "/api/i/v1/email", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(res)
#     print(data.decode("utf-8"))
