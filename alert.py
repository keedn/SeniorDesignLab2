
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import datetime as dt 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = os.environ.get("SENDGRID_API_KEY")
print("API key loaded:", bool(api_key))

# Get Current Time
# HH - Hour (0-12) = %I
# MM - Minute (0-59) = %M
# XX - AM or PM = %p
# Month - %m
# Day   - %d
# Year  - %Y

now = dt.datetime.now()
timestamp = now.strftime('%I:%M %p on %m/%d/%Y')
msgAlert = f"Critical Safety Event at {timestamp}"
print(msgAlert)

message = Mail(
    from_email="reliable.raccoon.zqiy@hidingmail.com",
    to_emails="reliable.raccoon.zqiy@hidingmail.com",
    subject="Electric Eye Interruption",
    plain_text_content = msgAlert)

try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    print("Status code:", response.status_code)
    print("Body:", response.body)
    print("Headers:", response.headers)
except Exception as e:
    print("Error:", str(e))


