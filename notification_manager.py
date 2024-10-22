import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

# Load environment variables from .env file
load_dotenv()

# Fetch necessary phone numbers and tokens
TWILIO_VERIFIED_NUMBER = os.environ.get("ENV_TWILIO_WHATSAPP")
TWILIO_WHATSAPP_NUMBER = os.environ.get("ENV_WHATSAPP_PHONE")
TWILIO_SID = os.environ.get("ENV_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("ENV_TWILIO_AUTH_TOKEN")
EMAIL_PROVIDER_SMTP_ADDRESS = os.environ.get("ENV_SMTP")
MY_EMAIL = os.environ.get("ENV_EMAIL")
MY_EMAIL_PASSWORD = os.environ.get("ENV_PASSWORD")

class NotificationManager:
    def __init__(self):
        self.smtp_address = EMAIL_PROVIDER_SMTP_ADDRESS
        self.email = MY_EMAIL
        self.email_password = MY_EMAIL_PASSWORD
        self.twilio_verified_number = TWILIO_VERIFIED_NUMBER
        self.whatsapp_number = TWILIO_WHATSAPP_NUMBER
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        try:
            self.connection = smtplib.SMTP(self.smtp_address, 587)  # Ensure the port is correct
            self.connection.starttls()  # Start TLS
            self.connection.login(self.email, self.email_password)
        except Exception as e:
            print(f"Failed to connect to email server: {e}")

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{self.twilio_verified_number}'
        )
        print(message.sid)

    def send_emails(self, email_list, email_body):
        with self.connection:
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )

