# File: src/note.py
import csv
import os

class NoteManager:
    def __init__(self):
        self.notes = []

    def load_notes(self, filepath):
        if not os.path.exists(filepath):
            return
        with open(filepath, newline='') as file:
            reader = csv.DictReader(file)
            self.notes = list(reader)

    def get_notes_by_patient_and_date(self, patient_id, date_str):
        result = []
        for note in self.notes:
            if note.get("Patient_ID") == patient_id and note.get("Visit_time") == date_str:
                result.append(note)
        return result

    def get_note_texts_by_patient_and_date(self, patient_id, date_str):
        notes = self.get_notes_by_patient_and_date(patient_id, date_str)
        return [note['Note_text'] for note in notes if 'Note_text' in note]

    def get_note_summary(self, patient_id, date_str):
        note_texts = self.get_note_texts_by_patient_and_date(patient_id, date_str)
        if not note_texts:
            return "No note found for given patient and date."
        return "\n---\n".join(note_texts)