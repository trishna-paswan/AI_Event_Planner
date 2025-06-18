import os
import csv
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

USERS_CSV = "data/users.csv"
EVENTS_CSV = "data/events.csv"
SPEAKERS_CSV = "data/speakers.csv"

def load_users():
    if not os.path.exists(USERS_CSV):
        return []
    with open(USERS_CSV, newline='') as f:
        return list(csv.DictReader(f))

def save_user(username, password):
    users_exist = os.path.exists(USERS_CSV) and os.path.getsize(USERS_CSV) > 0
    with open(USERS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'password'])
        if not users_exist:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})

def authenticate_user(username, password):
    return any(u['username'] == username and u['password'] == password for u in load_users())

def load_events():
    events = []
    with open("data/events.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 7:
                events.append({
                    "event_name": row[0],
                    "date": row[1],
                    "time": row[2],
                    "topic": row[3],
                    "email": row[4],
                    "whatsapp": row[5],
                    "predicted_budget": row[6]
                })
    return events


def predict_budget(user_budget):
    # Dummy ML-style prediction — just add +/- 10-20% random fluctuation
    noise = random.uniform(-0.2, 0.2)
    return round(user_budget * (1 + noise), 2)

def save_event(name, date, time, topic, email, whatsapp, predicted_budget):
    events_exist = os.path.exists(EVENTS_CSV) and os.path.getsize(EVENTS_CSV) > 0
    with open(EVENTS_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'event', 'date', 'time', 'topic', 'email', 'whatsapp', 'budget'
        ])
        if not events_exist:
            writer.writeheader()
        writer.writerow({
            'event': name,
            'date': date,
            'time': time,
            'topic': topic,
            'email': email,
            'whatsapp': whatsapp,
            'budget': predicted_budget
        })

def find_matching_speakers(user_topic, csv_path=SPEAKERS_CSV):
    if not os.path.exists(csv_path):
        return []

    df = pd.read_csv(csv_path)
    if df.empty or 'topic' not in df.columns:
        return []

    topics = df["topic"].fillna("").tolist()
    names = df["name"].tolist()
    emails = df["email"].tolist()

    vectorizer = TfidfVectorizer().fit_transform([user_topic] + topics)
    similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    results = []
    for idx in similarities.argsort()[::-1][:3]:
        if similarities[idx] > 0.1:
            results.append({
                "name": names[idx],
                "topic": topics[idx],
                "email": emails[idx]
            })

    return results
