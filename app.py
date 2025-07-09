from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# 📂 Ensure folders exist
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/music', exist_ok=True)

# Temporary in-memory storage
user_pages = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    message = request.form['message']
    username = name.lower().replace(" ", "-") + "-" + datetime.now().strftime("%Y%m%d%H%M")

    user_folder = f'static/uploads/{username}'
    photo_folder = os.path.join(user_folder, 'photos')
    os.makedirs(photo_folder, exist_ok=True)

    # Save message
    with open(os.path.join(user_folder, 'message.txt'), 'w') as f:
        f.write(message.strip())

    # Save photos
    if 'photos' in request.files:
        for photo in request.files.getlist('photos'):
            if photo.filename != '':
                photo.save(os.path.join(photo_folder, photo.filename))

    user_pages[username] = {'name': name}

    return redirect(url_for('page1', username=username))

@app.route('/hb/<username>/page1')
def page1(username):
    user = user_pages.get(username, {'name': 'Friend'})
    return render_template('page1.html', username=username, name=user['name'])

@app.route('/hb/<username>/page2')
def page2(username):
    user_folder = f'static/uploads/{username}'
    photo_folder = os.path.join(user_folder, 'photos')
    photos = [f"/{photo_folder}/{img}" for img in os.listdir(photo_folder)]
    user = user_pages.get(username, {'name': 'Friend'})
    return render_template('page2.html', photos=photos, name=user['name'], username=username)

@app.route('/hb/<username>/page3')
def page3(username):
    user = user_pages.get(username, {'name': 'Friend'})
    return render_template('page3.html', username=username, name=user['name'])

@app.route('/hb/<username>/page4')
def page4(username):
    user_folder = f'static/uploads/{username}'
    message_file = os.path.join(user_folder, 'message.txt')
    message = ""
    if os.path.exists(message_file):
        with open(message_file, 'r') as f:
            message = f.read()
    user = user_pages.get(username, {'name': 'Friend'})
    return render_template('page4.html', name=user['name'], message=message)

if __name__ == '__main__':
    app.run(debug=True)
