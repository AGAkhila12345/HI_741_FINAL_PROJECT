import pandas as pd
from datetime import datetime

class ClinicalNoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self._load_notes()

    def _load_notes(self):
        try:
            df = pd.read_csv(self.file_path)
            notes_dict = {}
            for index, row in df.iterrows():
                note_id = row['Note_ID']
                if note_id not in notes_dict:
                    notes_dict[note_id] = []
                notes_dict[note_id].append(row.to_dict())
            return notes_dict
        except FileNotFoundError:
            print(f"Clinical notes file '{self.file_path}' not found.")
            return {}
        except Exception as e:
            print(f"Error reading clinical notes file: {e}")
            return {}

    def view_note(self, patient_records, patient_id, note_date_str):
        try:
            note_date = datetime.strptime(note_date_str, '%Y-%m-%d').date()
            patient_visits = patient_records.retrieve_visit(patient_id)
            if not patient_visits.empty:
                found_note = False
                for index, visit in patient_visits.iterrows():
                    visit_time = pd.to_datetime(visit['Visit_time']).date()
                    if visit_time == note_date and 'Note_ID' in visit and visit['Note_ID'] in self.notes:
                        print(f"\nClinical Note for Patient ID '{patient_id}' on {note_date_str}:")
                        for key, value in self.notes[visit['Note_ID']][0].items():
                            print(f"  {key}: {value}")
                        found_note = True
                        break  # Assuming one note per visit on a given date
                if not found_note:
                    print(f"No clinical note found for Patient ID '{patient_id}' on {note_date_str}.")
            else:
                print(f"Patient ID '{patient_id}' not found.")
        except ValueError:
            print("Invalid date format. Please use%Y-%m-%d.")