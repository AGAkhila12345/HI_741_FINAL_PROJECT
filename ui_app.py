# File: src/ui_app.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from src.user import User
from src.patient import PatientManager
from src.note import NoteManager
import datetime

class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("HI741 Clinical Data Warehouse")
        self.user = None
        self.patient_mgr = PatientManager()
        self.note_mgr = NoteManager()
        self.patient_mgr.load_patients("data/patient_data.csv")
        self.note_mgr.load_notes("data/notes.csv")

    def run(self):
        self.show_login_screen()
        self.window.mainloop()

    def show_login_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Username:").pack()
        username_entry = tk.Entry(self.window)
        username_entry.pack()

        tk.Label(self.window, text="Password:").pack()
        password_entry = tk.Entry(self.window, show="*")
        password_entry.pack()

        def try_login():
            username = username_entry.get()
            password = password_entry.get()
            user = User.authenticate(username, password)
            if user:
                self.user = user
                User.log_login(user.username, "SUCCESS")
                self.show_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        tk.Button(self.window, text="Login", command=try_login).pack()

    def show_menu(self):
        self.clear_window()
        role = self.user.role
        options = []

        if role in ["nurse", "clinician"]:
            options = [
                ("Retrieve Patient", self.retrieve_patient),
                ("Add Patient", self.add_patient),
                ("Remove Patient", self.remove_patient),
                ("Count Visits", self.count_visits),
                ("View Note", self.view_note),
                ("Exit", self.window.quit)
            ]
        elif role == "admin":
            options = [("Count Visits", self.count_visits), ("Exit", self.window.quit)]
        elif role == "management":
            options = [("Generate Key Statistics", self.generate_statistics), ("Exit", self.window.quit)]

        for label, command in options:
            tk.Button(self.window, text=label, width=30, command=command).pack(pady=2)

    def retrieve_patient(self):
        pid = simpledialog.askstring("Retrieve", "Enter Patient ID:")
        if pid:
            visit = self.patient_mgr.retrieve_latest_patient_info(pid)
            if visit:
                info = "\n".join([f"{k}: {v}" for k, v in visit.items()])
                messagebox.showinfo("Latest Visit", info)
                self.user.log_action("retrieve_patient")
            else:
                messagebox.showwarning("Not Found", "Patient not found.")

    def add_patient(self):
        fields = ["Patient_ID", "Visit_time", "Visit_department", "Gender", "Race", "Age", "Ethnicity",
                  "Insurance", "Zip_code", "Chief_complaint", "Note_ID", "Note_type"]
        data = {}
        for field in fields:
            data[field] = simpledialog.askstring("Add Patient", f"Enter {field}:")
            if not data[field]:
                return
        data["Visit_ID"] = self.patient_mgr.generate_unique_visit_id()
        self.patient_mgr.add_or_update_patient(data)
        self.patient_mgr.save_patients("output/updated_patient_data.csv")
        messagebox.showinfo("Added", "Patient visit added successfully.")
        self.user.log_action("add_patient")

    def remove_patient(self):
        pid = simpledialog.askstring("Remove", "Enter Patient ID to remove:")
        if self.patient_mgr.remove_patient(pid):
            self.patient_mgr.save_patients("output/updated_patient_data.csv")
            messagebox.showinfo("Removed", "Patient removed successfully.")
            self.user.log_action("remove_patient")
        else:
            messagebox.showwarning("Not Found", "Patient ID not found.")

    def count_visits(self):
        date = simpledialog.askstring("Count", "Enter date (YYYY-MM-DD):")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            count = self.patient_mgr.count_visits_on_date(date)
            messagebox.showinfo("Count", f"Visits on {date}: {count}")
            self.user.log_action("count_visits")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date format.")

    def view_note(self):
        pid = simpledialog.askstring("Note", "Enter Patient ID:")
        date = simpledialog.askstring("Note", "Enter Date (YYYY-MM-DD):")
        summary = self.note_mgr.get_note_summary(pid, date)
        messagebox.showinfo("Notes", summary)
        self.user.log_action("view_note")

    def generate_statistics(self):
        messagebox.showinfo("Statistics", "Graphing and stats to be added.")
        self.user.log_action("generate_statistics")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
