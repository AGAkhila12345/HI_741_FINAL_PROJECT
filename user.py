# File: src/user.py
import csv
from datetime import datetime
import os

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    @staticmethod
    def authenticate(username, password, credentials_path="data/credentials.csv"):
        try:
            with open(credentials_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        return User(username, row['role'])
            User.log_login(username, "FAILED")
            return None
        except FileNotFoundError:
            print("Error: credentials.csv not found.")
            return None

    @staticmethod
    def log_login(username, status, logfile="output/usage_log.csv"):
        os.makedirs("output", exist_ok=True)
        with open(logfile, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["username", "status", "login_time"])
            writer.writerow([username, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def log_action(self, action, logfile="output/usage_log.csv"):
        with open(logfile, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, f"ACTION: {action}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])