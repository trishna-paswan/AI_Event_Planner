# 3. twilio_reminder.py
from twilio.rest import Client
from dotenv import load_dotenv
import os


load_dotenv()  # Load .env file

def send_whatsapp_reminder(phone_number, event_title, event_date):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_whatsapp_number = 'whatsapp:+14155238886'
    
    if not account_sid or not auth_token:
        print("Twilio credentials not set.")
        return

    client = Client(account_sid, auth_token)
    message_body = f"Reminder: Your event '{event_title}' is scheduled for {event_date}."

    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=f'whatsapp:{phone_number}'
    )

    print(f"WhatsApp reminder sent: SID {message.sid}")

