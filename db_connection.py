import mysql.connector

def connect():
    """
    Establishes connection to the MySQL database (result_management).
    
    NOTE: Remember to change 'root' and 'root' to your actual MySQL username and password.
    """
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",          # Change to your MySQL username
            password="Sql2004",      # Change to your MySQL password
            database="result_management"
        )
        return con
    except mysql.connector.Error as e:
        print("Database Connection Error:", e)
        return None

def calculate_grade(marks):
    """
    Calculates the grade based on the provided marks.
    A >= 90, B >= 75, C >= 60, F < 60.
    """
    try:
        # Safely convert marks to an integer
        marks = int(marks)
    except ValueError:
        # If marks cannot be converted (e.g., if it's empty or text), return 'F'
        return 'F' 

    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    else:
        return 'F'