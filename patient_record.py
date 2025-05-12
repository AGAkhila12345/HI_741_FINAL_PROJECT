#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import hashlib
from datetime import datetime


# In[ ]:


class Patient_record:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_frame = self.load_data(file_path)

    @staticmethod
    def load_data(file_path):
        try:
            return pd.read_csv(file_path, parse_dates=['Visit_time'])
        except FileNotFoundError:
            print("Patient information not found")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error reading patient data: {e}")
            return pd.DataFrame()

    def add_patient_record(self, patient_information):
        patient_information['Visit_time'] = pd.to_datetime(
            patient_information['Visit_time'])
        patient_id = str(patient_information['Patient_ID'])

        new_record = pd.DataFrame([patient_information]) #new patient record
        self.data_frame = pd.concat(
            [self.data_frame, new_record], ignore_index=True)
        self.data_frame.to_csv(self.file_path, index=False) #save changes

    def delete_patient_record(self, patient_id):
        patient_id = str(patient_id)
        if patient_id in self.data_frame['Patient_ID'].astype(str).values:
            self.data_frame = self.data_frame[self.data_frame['Patient_ID'].astype(
                str) != patient_id]
            print(f"Deleted records for patient ID {patient_id}")
            self.data_frame.to_csv(self.file_path, index=False)
            return True
        else:
            print("Patient ID not found; No records were deleted.")
            return False

    def retrieve_visit(self, patient_id):
        patient_id = str(patient_id)
        results = self.data_frame[self.data_frame['Patient_ID'].astype(
            str) == patient_id]
        if not results.empty:
            return results
        else:
            print("Patient ID not found")
            return pd.DataFrame()

    def count_visits(self, date):
        try:
            target_date = pd.to_datetime(date).date()
            self.data_frame['Visit_time'] = pd.to_datetime(
                self.data_frame['Visit_time'])
            count = (
                self.data_frame['Visit_time'].dt.date == target_date).sum()
            print(f"Total visits on {date}: {count}")
            return count
        except ValueError:
            print("Invalid date format; Please use MM-DD-YYYY")

    def generate_statistics(self):
        print("Generating key data insights for management...")
        self.data_frame['Visit_time'] = pd.to_datetime(
            self.data_frame['Visit_time'])

        #visits over time (year-month)
        visits_over_time = self.data_frame['Visit_time'].dt.to_period(
            'M').value_counts().sort_index()
        visits_over_time.plot(kind='line', title='Visits over time (year-month)')
        plt.xlabel('Trend over the years')
        plt.ylabel('Number of visits')
        plt.show()

        #visits by department
        self.data_frame['Visit_department'].value_counts().plot(
            kind='bar', title='Visits by department')
        plt.xlabel('Department')
        plt.ylabel('Number of visits')
        plt.show()

        #visits by various insurances
        self.data_frame['Insurance'].value_counts().plot(
            kind='pie', title='Visits by various insurances', autopct='%1.1f%%')
        plt.ylabel('')
        plt.show()

        #breakdown by race & gender
        self.data_frame.groupby(['Race', 'Gender']).size().unstack().plot(
            kind='bar', stacked=True, title='Breakdown by age and gender')
        plt.xlabel('Race')
        plt.ylabel('Number of visits')
        plt.show()

        #patient age distribution
        mean_age = self.data_frame['Age'].mean() #mean of patient age
        median_age = self.data_frame['Age'].median() #median of patient age
 
        self.data_frame['Age'].plot(
            kind='hist', bins=20, title='Patient Age Distribution', edgecolor='black')
        plt.axvline(mean_age, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_age:.1f}')
        plt.axvline(median_age, color='blue', linestyle='dashed', linewidth=2, label=f'Median: {median_age:.1f}')

        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

        #analysis on complaints
        top_complaints = self.data_frame['Chief_complaint'].value_counts().head(
            10)
        top_complaints.plot(kind='bar', title='Top 10 Complaints')
        plt.xlabel('Top Complaints')
        plt.ylabel('Number of records')
        plt.show()

        #visits by day of the week
        self.data_frame['day_of_week'] = self.data_frame['Visit_time'].dt.day_name()
        visits_by_day = self.data_frame['day_of_week'].value_counts()
        visits_by_day.plot(kind='bar', title='Visits by day of the week')
        plt.xlabel('Day of the week')
        plt.ylabel('Number of visits')
        plt.show()

