from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# 📂 Ensure folders exist
os.makedirs('static/uploads', exist_ok=True)

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

    # 💌 Save message
    with open(os.path.join(user_folder, 'message.txt'), 'w') as f:
        f.write(message.strip())

    # 💾 Save name
    with open(os.path.join(user_folder, 'name.txt'), 'w') as f:
        f.write(name.strip())

    # 📸 Save photos
    if 'photos' in request.files:
        for photo in request.files.getlist('photos'):
            if photo.filename != '':
                photo.save(os.path.join(photo_folder, photo.filename))

    # 🎉 Generate shareable link
    share_link = url_for('page1', username=username, _external=True)
    return render_template('share.html', link=share_link, name=name)

def load_user_data(username):
    """📦 Load saved user name and message from disk"""
    user_folder = f'static/uploads/{username}'
    name_file = os.path.join(user_folder, 'name.txt')
    message_file = os.path.join(user_folder, 'message.txt')
    name = "Friend"
    message = ""
    if os.path.exists(name_file):
        with open(name_file, 'r') as f:
            name = f.read()
    if os.path.exists(message_file):
        with open(message_file, 'r') as f:
            message = f.read()
    return name, message

@app.route('/hb/<username>/page1')
def page1(username):
    name, _ = load_user_data(username)
    return render_template('page1.html', username=username, name=name)

@app.route('/hb/<username>/page2')
def page2(username):
    user_folder = f'static/uploads/{username}'
    photo_folder = os.path.join(user_folder, 'photos')
    photos = [f"/{photo_folder}/{img}" for img in os.listdir(photo_folder)]
    name, _ = load_user_data(username)
    return render_template('page2.html', photos=photos, name=name, username=username)

@app.route('/hb/<username>/page3')
def page3(username):
    name, _ = load_user_data(username)
    return render_template('page3.html', username=username, name=name)

@app.route('/hb/<username>/page4')
def page4(username):
    name, message = load_user_data(username)
    return render_template('page4.html', name=name, message=message)

@app.route('/hb/<username>/share')
def share(username):
    user_folder = f'static/uploads/{username}'
    message_file = os.path.join(user_folder, 'message.txt')
    message = ""
    if os.path.exists(message_file):
        with open(message_file, 'r') as f:
            message = f.read()
    user = index.get(username, {'name': 'Friend'})
    share_link = url_for('page1', username=username, _external=True)
    return render_template('share.html', name=user['name'], message=message, link=share_link)


if __name__ == '__main__':
    app.run(debug=True)
