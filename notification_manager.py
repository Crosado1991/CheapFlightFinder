import os
import smtplib
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_VERIFIED_NUMBER = os.getenv("ENV_TWILIO_WHATSAPP")
TWILIO_WHATSAPP_NUMBER = os.getenv("ENV_WHATSAPP_PHONE")
TWILIO_SID = os.getenv("ENV_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("ENV_TWILIO_AUTH_TOKEN")
EMAIL_PROVIDER_SMTP_ADDRESS = os.getenv("ENV_SMTP")
MY_EMAIL = os.getenv("ENV_EMAIL")
MY_EMAIL_PASSWORD = os.getenv("ENV_PASSWORD")

class NotificationManager:
    def __init__(self):
        self.smtp_address = EMAIL_PROVIDER_SMTP_ADDRESS
        self.email = MY_EMAIL
        self.email_password = MY_EMAIL_PASSWORD
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            body=message_body,
            to=f'whatsapp:{TWILIO_VERIFIED_NUMBER}'
        )
        print(f"WhatsApp message sent: {message.sid}")

    def send_emails(self, email_list, email_body):
        with smtplib.SMTP(self.smtp_address, 587) as connection:
            connection.starttls()
            connection.login(self.email, self.email_password)
            for email in email_list:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:Low Flight Price Alert!\n\n{email_body}"
                )
