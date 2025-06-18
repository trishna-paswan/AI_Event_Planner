from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from utils import load_events
from mail_utils import send_email
from whatsapp_utils import send_whatsapp

scheduler = BackgroundScheduler()

def schedule_reminders():
    events = load_events()  # Load from CSV
    for event in events:
        name = event['event_name']
        date_str = event['date']
        email = event['email']
        whatsapp = event['whatsapp']

        try:
            run_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            scheduler.add_job(send_email, 'date', run_date=run_time, args=[email, name])
            scheduler.add_job(send_whatsapp, 'date', run_date=run_time, args=[whatsapp, name])
            print(f"Scheduled reminders for {name} on {run_time}")
        except Exception as e:
            print(f"Error scheduling event: {name}, {e}")

def start_scheduler():
    schedule_reminders()
    scheduler.start()
