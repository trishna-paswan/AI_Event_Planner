# ai_event_planner_gui.py with safe date handling and scheduler fix
import os
import csv
import smtplib
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import Calendar, DateEntry
from email.message import EmailMessage
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from difflib import get_close_matches
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from dateutil import parser

load_dotenv()

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Utility Functions

def show_speaker_suggestions(topic):
    results = find_speakers(topic)
    suggestion_window = Toplevel()
    suggestion_window.title("🎤 Suggested Speakers")
    suggestion_window.geometry("500x300")
    Label(suggestion_window, text=f"Topic: {topic}", font=("Arial", 12, "bold")).pack(pady=10)
    listbox = Listbox(suggestion_window, width=80, height=10)
    listbox.pack(padx=10, pady=10)
    for result in results:
        listbox.insert(END, result)

def register_user(username, password, email):
    with open("data/users.csv", mode="a", newline="") as f:
        csv.writer(f).writerow([username, password, email])
    return True

def login_user(username, password):
    try:
        with open("data/users.csv", mode="r") as f:
            for row in csv.reader(f):
                if len(row) >= 3 and row[0] == username and row[1] == password:
                    return row[2]
    except FileNotFoundError:
        pass
    return None

def suggest_tasks(event_type):
    suggestions = {
        "Tech Talk": ["Book keynote speaker", "Design posters", "Test AV setup", "Networking session"],
        "Workshop": ["Finalize topic", "Arrange kits", "Distribute certificates", "Feedback"],
        "Hackathon": ["Set problem", "Organize sponsors", "Form judging panel", "Mentoring sessions"],
        "Webinar": ["Create form", "Dry run", "Email reminder", "Share recording"]
    }
    return suggestions.get(event_type, ["Brainstorm", "Plan logistics", "Execute", "Evaluate"])

def save_event(username, name, event_type, date, tasks, budget, whatsapp):
    with open("data/events.csv", mode="a", newline="") as f:
        csv.writer(f).writerow([username, name, event_type, date, budget, whatsapp] + tasks)

def load_events(username):
    events = []
    try:
        with open("data/events.csv", mode="r") as f:
            for row in csv.reader(f):
                if row[0] == username:
                    events.append(row)
    except FileNotFoundError:
        pass
    return events

def predict_budget(event_type, participants, duration):
    try:
        df = pd.read_csv("data/budget_data.csv")
        X = df[["participants", "duration"]]
        y = df["budget"]
        model = LinearRegression().fit(X, y)
        prediction = model.predict([[participants, duration]])
        return round(prediction[0], 2)
    except Exception as e:
        print("Prediction Error:", e)
        return "Estimation Failed"

def send_email_reminder(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = "youremail@example.com"
        msg['To'] = to_email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("youremail@example.com", "yourpassword")
            smtp.send_message(msg)
    except:
        pass

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

def find_speakers(topic):
    try:
        df = pd.read_csv("data/speakers.csv")
        matches = []
        for _, row in df.iterrows():
            if topic.lower() in row['expertise'].lower() or get_close_matches(topic.lower(), [row['expertise'].lower()]):
                matches.append(f"{row['name']} | Expertise: {row['expertise']} | Contact: {row['email']}")
        return matches if matches else ["No relevant speakers found"]
    except:
        return ["Speaker database unavailable"]

scheduler = BackgroundScheduler()
scheduler.start()

class EventPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI_Event_Planner")
        self.username = ""
        self.email = ""
        self.build_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_login(self):
        self.clear_window()
        Label(self.root, text="Login or Register", font=('Arial', 16)).pack(pady=10)
        Label(self.root, text="Username: ").pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()
        Label(self.root, text="Password: ").pack()
        self.password_entry = Entry(self.root, show='*')
        self.password_entry.pack()
        Label(self.root, text="Email (for register only):").pack()
        self.email_entry = Entry(self.root)
        self.email_entry.pack()
        Button(self.root, text="Login", command=self.handle_login).pack(pady=5)
        Button(self.root, text="Register", command=self.handle_register).pack()

    def handle_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        email = login_user(user, pwd)
        if email:
            self.username = user
            self.email = email
            self.schedule_whatsapp_jobs()
            self.build_menu()
        else:
            messagebox.showerror("Error", "Login failed.")

    def handle_register(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        email = self.email_entry.get()
        register_user(user, pwd, email)
        messagebox.showinfo("Success", "Registered successfully.")

    def build_menu(self):
        self.clear_window()
        Label(self.root, text=f"Welcome, {self.username}", font=('Arial', 14)).pack(pady=10)
        Button(self.root, text="Add Event", width=20, command=self.add_event).pack(pady=5)
        Button(self.root, text="View Events", width=20, command=self.view_events).pack(pady=5)
        Button(self.root, text="Calendar View", width=20, command=self.show_calendar).pack(pady=5)
        Button(self.root, text="Suggest Tasks", width=20, command=self.suggest_task_ui).pack(pady=5)
        Button(self.root, text="Find Speakers", width=20, command=self.speaker_ui).pack(pady=5)
        Button(self.root, text="Logout", width=20, command=self.build_login).pack(pady=5)

    def add_event(self):
        self.clear_window()
        Label(self.root, text="Add New Event", font=('Arial', 14)).pack(pady=10)
        name_entry = Entry(self.root)
        type_entry = Entry(self.root)
        participants_entry = Entry(self.root)
        duration_entry = Entry(self.root)
        date_entry = DateEntry(self.root, date_pattern='dd/mm/yyyy')
        whatsapp_entry = Entry(self.root)

        for label, widget in zip([
            "Event Name:", "Event Type:", "Participants:",
            "Duration (days):", "Event Date:", "WhatsApp Number (+countrycode):"
        ], [name_entry, type_entry, participants_entry, duration_entry, date_entry, whatsapp_entry]):
            Label(self.root, text=label).pack()
            widget.pack()

        def save():
            try:
                name = name_entry.get()
                etype = type_entry.get()
                date = date_entry.get()
                number = whatsapp_entry.get()
                participants = int(participants_entry.get())
                duration = int(duration_entry.get())
                budget = predict_budget(etype, participants, duration)
                tasks = suggest_tasks(etype)
                save_event(self.username, name, etype, date, tasks, budget, number)
                send_email_reminder(self.email, f"Event Reminder: {name}", f"Reminder for your event '{name}' on {date}")
                if number:
                    send_whatsapp_reminder(number, f"Reminder: '{name}' event is scheduled on {date}.")
                messagebox.showinfo("Saved", f"Event saved! Budget: ₹{budget}")
                self.schedule_whatsapp_jobs()
                self.build_menu()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save event: {str(e)}")

        Button(self.root, text="Save Event", command=save).pack(pady=10)
        Button(self.root, text="Back", command=self.build_menu).pack()

    def schedule_whatsapp_jobs(self):
        scheduler.remove_all_jobs()
        events = load_events(self.username)
        for ev in events:
            try:
                name = ev[1]
                date_str = ev[3]
                number = ev[5]
                event_dt = parser.parse(date_str, dayfirst=True)
                reminder_dt = event_dt - timedelta(days=1)
                if reminder_dt > datetime.now():
                    print(f"Scheduling WhatsApp for {name} on {reminder_dt}")
                    scheduler.add_job(
                        send_whatsapp_reminder,
                        'date',
                        run_date=reminder_dt,
                        args=[number, f"Reminder: '{name}' is scheduled on {date_str}"]
                    )
            except Exception as e:
                print("Scheduler Error:", e)

    def view_events(self):
        self.clear_window()
        Label(self.root, text="Your Events", font=('Arial', 14)).pack(pady=10)
        events = load_events(self.username)
        if not events:
            Label(self.root, text="No events found.").pack()
        for event in events:
            Label(self.root, text=f"{event[1]} - {event[3]} | Type: {event[2]} | Budget: ₹{event[4]}").pack()
        Button(self.root, text="Back", command=self.build_menu).pack(pady=10)

    def show_calendar(self):
        self.clear_window()
        Label(self.root, text="Event Calendar", font=('Arial', 14)).pack(pady=10)
        cal = Calendar(self.root, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)
        events = load_events(self.username)
        Label(self.root, text="Events on selected date will appear in terminal.").pack()

        def show_selected():
            selected_date = cal.get_date()
            print(f"Events on {selected_date}:")
            for ev in events:
                if ev[3] == selected_date:
                    print(f"- {ev[1]} ({ev[2]}) | Budget: ₹{ev[4]}")

        Button(self.root, text="Show Events", command=show_selected).pack(pady=5)
        Button(self.root, text="Back", command=self.build_menu).pack(pady=10)

    def suggest_task_ui(self):
        self.clear_window()
        Label(self.root, text="Suggest Tasks", font=('Arial', 14)).pack(pady=10)
        type_entry = Entry(self.root)
        Label(self.root, text="Enter Event Type:").pack()
        type_entry.pack()

        def suggest():
            event_type = type_entry.get()
            tasks = suggest_tasks(event_type)
            messagebox.showinfo("Suggested Tasks", "\n".join(tasks))

        Button(self.root, text="Suggest", command=suggest).pack(pady=10)
        Button(self.root, text="Back", command=self.build_menu).pack()

    def speaker_ui(self):
        self.clear_window()
        Label(self.root, text="Find Speakers", font=('Arial', 14)).pack(pady=10)
        topic_entry = Entry(self.root)
        Label(self.root, text="Enter Topic:").pack()
        topic_entry.pack()

        def search():
            topic = topic_entry.get()
            speakers = find_speakers(topic)
            messagebox.showinfo("Speakers Found", "\n".join(speakers))

        Button(self.root, text="Search", command=search).pack(pady=10)
        Button(self.root, text="Back", command=self.build_menu).pack()

if __name__ == "__main__":
    root = Tk()
    app = EventPlannerApp(root)
    root.geometry("400x600")
    root.mainloop()
