**HI 741 Spring 2025 Final Project ---- CLINICAL DATA WAREHOUSE UI**

             This project is a Tkinter-based python application designed for a local hospital's clinical data warehouse system. It provides a user-friendly graphical interface that allows hospital staff to manage patient records, access clinical notes, generate key statistics, and track software usage _ all based on their role (admin, nurse, clinician, or management).
   
   1.**Features**: 
-Secure Login: with role-based access (admin, nurse, clinician, management)
-Role-Specific Menu Options : with restricted access to PHI
-#Retrieve, Add, and Remove Patients
-View Clinical Notes by patient ID and Date
-Count Patient Visits on a specified date
-Generate key Statistics using graphs (for admin/management)
-Track User Activity: Logs usernames, role, login time, actions performed, and Failed login attempts.
-Data Persistence: Changes are saved to patient and usage files.

   2.**Technologies used** :
   Python 3.9+
   Tkinter  (for UI)
   Pandas
   Matplotlib
   CSV(for data handling)
   **Folder Structure**
 -main.py               #Entry point of the application
 -login.py              #Handles login logic
 -patient.py            #patient data management logic
 -stats.py              #key statistics and Graphs
 -ui.py                 #Tkinter-based GUI application
 -credentials.csv       #sample login credentials
 -patient.csv           #patient visit data
 -clinical_notes.csv    #clinical note data 
 -usage_log.csv         #user activity log
 -UML_Diagram.pgn       #class Structure visualization
 -requirements.txt      #list of required packages
 - README.md            #Project documentation(this file)

 **Output files**
 patient.csv updated with any changes made(add/remove)
 usage_log.csv track login time, role , action, and failed login attempts.

**UML Diagram**
Class relationships 
attributes and methods
UI structure

**Usage**
-Make sure you have the necessary files in the same directory.
-Run the 'ui.py' file using python: 
-The application window will open, prompting you to enter your username and password.
-After successful authentication, the main.menu will be displayed based in your user role.
-Navigate through the available options using the buttons and follow the prompts to perform various actions.
-The 'usage_log.csv' file will be updated with user actions and timestamps.

**Note**
-The 'PA3_credentials.csv' file should contain the username and password pairs, separated by a comma, with one pair per line (e.g., 'username1,'password1')'
- The 'PA3_patient.csv' file should have the following column headers: 'Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Race', 'Gender', 'Ethnicity', 'Age', 'Zip_code', 'Insurance', 'Chief_complaint', 'Note_ID', 'Note_type'.

Made by AKHILA AMUDALA GANESH. 

   
