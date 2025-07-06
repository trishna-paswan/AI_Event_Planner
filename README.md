# 🧠 AI Event Planner
  
An intelligent, all-in-one desktop event management system built with **Python & Tkinter**. This app combines the power of **AI**, **automation**, and a beautifully designed GUI to streamline planning for workshops, webinars, seminars, and more. 
 
---

## 🔥 Key Features 

🎯 **Event Creation & Calendar Integration**  
Plan events with a clean, intuitive calendar UI using `tkcalendar`. 

🧠 **AI-Powered Task Suggestions**  
Get context-aware task recommendations tailored to event types like workshops, webinars, etc.

🎤 **Smart Speaker Suggestions**  
Suggests speakers from a domain-based database (`speakers.csv`) with fuzzy matching (via `difflib`).

📉 **Budget Forecasting with Machine Learning**   
Predict expected budgets using `LinearRegression` from historical data.

💬 **WhatsApp & Email Reminders**  
Send automated event reminders to participants using Twilio & SMTP.

🛡️ **Secure Credential Management**   
Twilio credentials are loaded securely from `.env` using `python-dotenv`.

🌙 **Background Scheduler**  
Uses `APScheduler` to run jobs without blocking the GUI.

---
 
## 📂 Folder Structure

AI_Event_Planner/

│
├── data/

│ └── speakers.csv # Speaker database

├── .env # Secure credentials (excluded from Git)

├── ai_event_planner_gui.py # Main GUI application

├── requirements.txt # Project dependencies

└── README.md # You're reading it :)

## Create a .env File (Important)

TWILIO_ACCOUNT_SID=your_account_sid

TWILIO_AUTH_TOKEN=your_auth_token

## Run the Application

python3 ai_event_planner_gui.py

## 🗂️ Sample speakers.csv

name,expertise,email

Dr. Neha Verma,Artificial Intelligence,neha@example.com

Rohit Sharma,Cybersecurity,rohit@example.com

Asha Singh,Blockchain,asha@example.com

Vikram Das,Web Development,vikram@example.com

Priya Yadav,Data Science,priya@example.com

📝 You can add more speaker entries in the data/speakers.csv file.

## 👩‍💻 Developer
Trishna Kumari Paswan
