import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
from datetime import datetime
import os
import csv
from authentication import authenticate_user, load_credentials
from patient_record import Patient_record


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to Hospital Data Management System!")
        self.geometry("1200x600")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.credentials_file = os.path.join(BASE_DIR, "PA3_credentials.csv")
        self.patients_file = os.path.join(BASE_DIR, "PA3_data.csv")
        self.user = None
        self.patient_records = None
        self.usage_notes_file = os.path.join(BASE_DIR, "PA3_Notes.csv")
        self.create_usage_notes_file()
        self.setup_ui()

    def create_usage_notes_file(self):
        if not os.path.exists(self.usage_notes_file):
            with open(self.usage_notes_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Username", "Role", "Action", "Timestamp"])

    def log_usage(self, action):
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        with open(self.usage_notes_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.user.username, self.user.role, action, timestamp])

    def log_usage_invalid_login(self, action):
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        with open(self.usage_notes_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Invalid User", "No Role", action, timestamp])

    def setup_ui(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user = authenticate_user(self.credentials_file, username, password)

        if self.user is None:
            messagebox.showerror("Error", "Invalid credentials")
            self.log_usage_invalid_login("Login Unsuccessful")
        else:
            self.patient_records = Patient_record(self.patients_file)
            self.log_usage("Login Successful")
            self.show_menu()

    def show_menu(self):
        self.login_frame.pack_forget()
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(fill="both", expand=True)

        if self.user.role == "management":
            tk.Button(self.menu_frame, text="Generate Key Statistics",
                      command=self.generate_key_statistics).pack(pady=10)
        elif self.user.role == "admin":
            tk.Button(self.menu_frame, text="Count Visits",
                      command=self.count_visits).pack(pady=10)
        elif self.user.role in ["nurse", "clinician"]:
            tk.Button(self.menu_frame, text="Retrieve Patient",
                      command=self.retrieve_patient).pack(pady=10)
            tk.Button(self.menu_frame, text="Add Patient",
                      command=self.add_patient_window).pack(pady=10)
            tk.Button(self.menu_frame, text="Remove Patient",
                      command=self.remove_patient).pack(pady=10)
            tk.Button(self.menu_frame, text="Count Visits",
                      command=self.count_visits).pack(pady=10)
        else:
            messagebox.showerror("Error", "User Unauthorized")

        tk.Button(self.menu_frame, text="Logout", command=self.logout).pack(pady=10)

    def generate_key_statistics(self):
        self.patient_records.generate_statistics()
        self.log_usage("Generate Statistics")

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        if patient_id:
            visits = self.patient_records.retrieve_visit(patient_id)
            if not visits.empty:
                result_window = tk.Toplevel(self)
                result_window.title(f"Patient Visits for ID {patient_id}")
                tk.Label(result_window, text=visits.to_string()).pack()
            else:
                messagebox.showerror("Error", "Patient not found")
        self.log_usage("Retrieve Patient")

    def add_patient_window(self):
        window = tk.Toplevel(self)
        window.title("Add Patient")
        tk.Label(window, text="Enter Patient Information:").pack()

        fields = ["Patient_ID", "Visit_ID", "Visit_time", "Visit_department", "Race", "Gender",
                  "Ethnicity", "Age", "Zip_code", "Insurance", "Chief_complaint", "Note_ID", "Note_type"]

        entries = {}
        for field in fields:
            frame = tk.Frame(window)
            frame.pack()
            tk.Label(frame, text=field).pack(side="left")
            entry = tk.Entry(frame)
            entry.pack(side="right")
            entries[field] = entry

        def add_patient_wrapper():
            self.add_patient(entries)
            window.withdraw()

        tk.Button(window, text="Add", command=add_patient_wrapper).pack()

    def add_patient(self, entries):
        patient_info = {}
        for field, entry in entries.items():
            value = entry.get()
            if not value:
                messagebox.showerror("Error", f"Please enter {field}.")
                return
            patient_info[field] = value

        self.patient_records.add_patient_record(patient_info)
        messagebox.showinfo("Success", "Patient added successfully")
        self.log_usage("Add Patient")

    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID:")
        if patient_id:
            if self.patient_records.delete_patient_record(patient_id):
                messagebox.showinfo("Info", "Patient removed successfully")
            else:
                messagebox.showerror("Error", "Patient not found")
        self.log_usage("Remove Patient")

    def count_visits(self):
        date_str = simpledialog.askstring("Count Visits", "Enter the date (MM/DD/YYYY):")
        if date_str:
            try:
                date = datetime.strptime(date_str, "%m/%d/%Y").date()
                total_visits = self.patient_records.count_visits(date)
                messagebox.showinfo("Visits Count", f"Total visits on {date_str}: {total_visits}")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use MM/DD/YYYY")
        self.log_usage("Count Visits")

    def logout(self):
        self.menu_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.user = None


if __name__ == "__main__":
    app = Application()
    app.mainloop()
