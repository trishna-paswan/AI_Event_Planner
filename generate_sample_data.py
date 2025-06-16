import os
import csv

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Sample data for users.csv
users_data = [
    ["username", "password", "email"],
    ["trishna123", "pass123", "trishna@example.com"],
    ["admin", "admin123", "admin@example.com"]
]

# Sample data for budget_data.csv
budget_data = [
    ["participants", "duration", "budget"],
    [50, 1, 20000],
    [100, 2, 45000],
    [150, 3, 70000],
    [200, 4, 95000],
    [250, 5, 120000]
]

# Sample data for speakers.csv
speakers_data = [
    ["name", "expertise", "email"],
    ["Dr. Ananya Singh", "Artificial Intelligence", "ananya.ai@example.com"],
    ["Mr. Rajeev Mehta", "Blockchain", "rajeev.blockchain@example.com"],
    ["Ms. Priya Das", "Data Science", "priya.ds@example.com"],
    ["Prof. Arun Sharma", "Quantum Computing", "arun.qc@example.com"],
    ["Dr. Nisha Verma", "Machine Learning", "nisha.ml@example.com"]
]

# Sample data for events.csv (can start empty or with one example)
events_data = [
    ["username", "event_name", "event_type", "date", "budget", "whatsapp", "task1", "task2", "task3"],
    ["trishna123", "AI Webinar", "Webinar", "2025-07-01", "25000", "+919876543210", "Create registration form", "Conduct dry run", "Email reminder to attendees"]
]

# File save function
def save_csv(file_path, data):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Create all CSVs
save_csv("data/users.csv", users_data)
save_csv("data/budget_data.csv", budget_data)
save_csv("data/speakers.csv", speakers_data)
save_csv("data/events.csv", events_data)

print("✅ Sample data files generated in the 'data' folder.")
