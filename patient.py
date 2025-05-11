# File: src/patient.py
import csv
import os
import random
import string
from datetime import datetime

class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.visits = []

    def add_visit(self, visit_data):
        self.visits.append(visit_data)

    def get_latest_visit(self):
        if not self.visits:
            return None
        return sorted(self.visits, key=lambda x: x['Visit_time'], reverse=True)[0]

    def get_visits_on_date(self, date_str):
        return [v for v in self.visits if v['Visit_time'] == date_str]

    def to_dict_list(self):
        return self.visits


class PatientManager:
    def __init__(self):
        self.patients = {}

    def load_patients(self, filepath):
        if not os.path.exists(filepath):
            return
        with open(filepath, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pid = row['Patient_ID']
                if pid not in self.patients:
                    self.patients[pid] = Patient(pid)
                self.patients[pid].add_visit(row)

    def save_patients(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        all_visits = [visit for p in self.patients.values() for visit in p.to_dict_list()]
        if not all_visits:
            return
        with open(filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=all_visits[0].keys())
            writer.writeheader()
            writer.writerows(all_visits)

    def add_or_update_patient(self, data):
        pid = data['Patient_ID']
        if pid not in self.patients:
            self.patients[pid] = Patient(pid)
        self.patients[pid].add_visit(data)

    def remove_patient(self, patient_id):
        return self.patients.pop(patient_id, None)

    def retrieve_latest_patient_info(self, patient_id):
        if patient_id not in self.patients:
            return None
        return self.patients[patient_id].get_latest_visit()

    def count_visits_on_date(self, date_str):
        count = 0
        for patient in self.patients.values():
            count += len(patient.get_visits_on_date(date_str))
        return count

    @staticmethod
    def generate_unique_visit_id(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
