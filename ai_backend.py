# ai_backend.py

import os
import csv
import smtplib
from email.message import EmailMessage
from sklearn.linear_model import LinearRegression
import pandas as pd
from difflib import get_close_matches
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file for Twilio & Email
load_dotenv()

# Ensure data folder exists
def ensure_data_folder():
    os.makedirs("data", exist_ok=True)


# ----------------------------
# USER AUTHENTICATION
# ----------------------------

def register_user(username, password, email):
    with open("data/users.csv", mode="a", newline="") as file:
        csv.writer(file).writerow([username, password, email])
    return True

def login_user(username, password):
    try:
        with open("data/users.csv", mode="r") as file:
            for row in csv.reader(file):
                if len(row) >= 3 and row[0] == username and row[1] == password:
                    return row[2]  # return user's email
    except FileNotFoundError:
        return None
    return None


# ----------------------------
# TASK SUGGESTIONS
# ----------------------------

def suggest_tasks(event_type):
    task_dict = {
        "Tech Talk": ["Book keynote speaker", "Design promotional posters", "Test audio-visual setup", "Schedule networking session"],
        "Workshop": ["Finalize workshop topic", "Arrange venue & kits", "Distribute certificates", "Collect participant feedback"],
        "Hackathon": ["Set problem statement", "Organize sponsors & prizes", "Form judging panel", "Plan team mentoring sessions"],
        "Webinar": ["Create registration form", "Conduct dry run", "Email reminder to attendees", "Share recording post-session"]
    }
    return task_dict.get(event_type, ["Brainstorm idea", "Plan logistics", "Execute event", "Evaluate outcome"])


# ----------------------------
# BUDGET PREDICTION USING ML
# ----------------------------

def predict_budget(event_type, participants, duration):
    try:
        df = pd.read_csv("data/budget_data.csv")
        X = df[["participants", "duration"]]
        y = df["budget"]
        model = LinearRegression().fit(X, y)

        input_data = pd.DataFrame([[participants, duration]], columns=["participants", "duration"])
        predicted_budget = model.predict(input_data)
        return round(predicted_budget[0], 2)
    except Exception as e:
        print("Budget Prediction Error:", e)
        return "Estimation Failed"


# ----------------------------
# EVENT DATA HANDLING
# ----------------------------

def save_event(username, name, event_type, date, tasks, budget, whatsapp):
    with open("data/events.csv", mode="a", newline="") as file:
        csv.writer(file).writerow([username, name, event_type, date, budget, whatsapp] + tasks)

def load_events(username):
    events = []
    try:
        with open("data/events.csv", mode="r") as file:
            for row in csv.reader(file):
                if row[0] == username:
                    events.append(row)
    except FileNotFoundError:
        pass
    return events


# ----------------------------
# SPEAKER SUGGESTION
# ----------------------------

def find_speakers(topic):
    try:
        df = pd.read_csv("data/speakers.csv")
        matches = []
        for _, row in df.iterrows():
            if topic.lower() in row['expertise'].lower() or get_close_matches(topic.lower(), [row['expertise'].lower()]):
                matches.append(f"{row['name']} | Expertise: {row['expertise']} | Contact: {row['email']}")
        return matches if matches else ["No relevant speakers found"]
    except Exception as e:
        print("Speaker Search Error:", e)
        return ["Speaker database unavailable"]


# ----------------------------
# EMAIL REMINDER
# ----------------------------

def send_email_reminder(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv("EMAIL_ID")  # from .env
        msg['To'] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_ID"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
    except Exception as e:
        print("Email Error:", e)


# ----------------------------
# WHATSAPP REMINDER
# ----------------------------

def send_whatsapp_reminder(to_number, body):
    try:
        account_sid = os.getenv("TWILIO_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=body,
            from_='whatsapp:+14155238886',
            to='whatsapp:' + to_number
        )
    except Exception as e:
        print("WhatsApp Error:", e)

