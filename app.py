from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify 
import csv  
import os

from utils import predict_budget, save_event, find_matching_speakers, load_events
from reminders import start_scheduler

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # change to a secure key
 
# Ensure data folder and user CSV exist
os.makedirs('data', exist_ok=True)
USERS_CSV = "data/users.csv"
if not os.path.exists(USERS_CSV):
    with open(USERS_CSV, 'w', newline='') as f:
        csv.writer(f).writerow(["username", "password", "email"])

def login_user(username, password):
    with open(USERS_CSV, mode="r") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0] == username and row[1] == password:
                return row[2]
    return None

def register_user(username, password, email):
    with open(USERS_CSV, mode="a", newline="") as f:
        csv.writer(f).writerow([username, password, email])
    return True

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        email = login_user(uname, pwd)
        if email:
            session['username'] = uname
            session['email'] = email
            return redirect(url_for('dashboard'))
        flash("Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        register_user(uname, pwd, email)
        flash("Registered successfully! Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect('/login')
    return render_template("dashboard.html", username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if not session.get('username'):
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['event_name']
        date = request.form['date']
        time = request.form['time']
        topic = request.form['topic']
        budget = float(request.form['budget'])
        email = request.form['email']
        whatsapp = request.form['whatsapp']

        predicted_budget = predict_budget(budget)
        save_event(name, date, time, topic, email, whatsapp, predicted_budget)

        flash(f"Event '{name}' scheduled with predicted budget ₹{predicted_budget:.2f}!")
        return redirect('/dashboard')

    return render_template('add_event.html')

@app.route('/speakers', methods=['GET', 'POST'])
def speakers():
    if not session.get('username'):
        return redirect('/login')

    matched_speakers = []
    searched = False
    input_topic = ""

    if request.method == 'POST':
        input_topic = request.form['topic']
        matched_speakers = find_matching_speakers(input_topic)
        searched = True

    return render_template("speakers.html", matched_speakers=matched_speakers, searched=searched, input_topic=input_topic)

@app.route("/calendar")
def calendar():
    if not session.get('username'):
        return redirect('/login')
    return render_template("calendar.html")

@app.route("/events")
def api_events():
    events = load_events()
    calendar_data = [
        {"title": event["event_name"], "start": event["date"]}

        for event in events
    ]
    return jsonify(calendar_data)

@app.route('/view_events')
def view_events():
    if not session.get('username'):
        return redirect('/login')

    events = load_events()
    return render_template("events.html", events=events)


if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)
