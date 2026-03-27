# alert.py (Debug Version)
import os
import datetime as dt 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import CONFIG # Make sure your key is in CONFIG.py
def send_emergency_email():
    api_key = CONFIG.SENDGRID_API_KEY
    print("API key loaded:", bool(api_key))

    now = dt.datetime.now()
    timestamp = now.strftime('%I:%M %p on %m/%d/%Y')
    msgAlert = f"Critical Safety Event at {timestamp}"

    # IMPORTANT: This MUST be the email you clicked "Verify" on in SendGrid
    FROM_EMAIL = "from_email" 

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails="to_email",
        subject="Electric Eye Interruption",
        plain_text_content=msgAlert)

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("Success! Status code:", response.status_code)
    except Exception as e:
        print("\n--- ERROR DETAIL ---")
        print("Status Code:", e.to_dict.get('status_code') if hasattr(e, 'to_dict') else "N/A")
        # This line below is the most important for debugging 403s
        print("Reason:", e.body if hasattr(e, 'body') else str(e)) 
        print("--------------------\n")
