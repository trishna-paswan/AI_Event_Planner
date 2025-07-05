# 1. app.py 
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Event
from twilio_reminder import send_whatsapp_reminder
from face_recognition_utils import verify_face
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return render_template('login.html', success=True)  # triggers confetti
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image = request.files['face']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filepath)
        user = User(username=username, password=password, face_image=image.filename)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    events = Event.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', events=events)

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        event = Event(title=title, date=date, description=description, user_id=session['user_id'])
        db.session.add(event)
        db.session.commit()
        send_whatsapp_reminder('+91XXXXXXXXXX', title, date)  # Replace with dynamic phone number
        return redirect(url_for('dashboard'))
    return render_template('add_event.html')

@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    events = Event.query.filter_by(user_id=session['user_id']).all()
    return render_template('calendar.html', events=events)

@app.route('/verify-face', methods=['POST'])
def verify_face_route():
    uploaded = request.files['face']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded.filename)
    uploaded.save(filepath)
    is_valid = verify_face(session['user_id'], filepath)
    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)
