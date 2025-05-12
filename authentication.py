import csv

#user authentication
def authenticate_user(credentials_file, username, password):
    try:
        with open(credentials_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password: #verifying the username and password
                    from user import User  #importing user information
                    return User(username, row['role'])
    except FileNotFoundError:
        print("Credentials file not found")
    except Exception as e:
        print(f"Error reading credentials file: {e}")
    return None

#loading credentials
def load_credentials(filename):
    credentials = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials[row['username']] = {'password': row['password'], 'role': row['role']}
    return credentials
