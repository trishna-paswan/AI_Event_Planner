import smtplib
from email.mime.text import MIMEText

def send_email(to_email, event_name):
    msg = MIMEText(f"Reminder: Your event '{event_name}' is scheduled soon!")
    msg['Subject'] = f"Event Reminder: {event_name}"
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login("your_email@gmail.com", "your_app_password")
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
