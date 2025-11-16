Result Management System:- 
A Python Tkinter-based GUI application to add, update, delete, and search student results.
Grades are calculated automatically based on marks.

✅ Features :-
Add student record

Update marks

Delete record

Search student by Roll No
Auto-grade calculation (A/B/C/F)
MySQL database integration
Modern & colorful UI

✅ Requirements
Install this before running the project:
Python 3.8+
MySQL Server
mysql-connector-python library

✅ Step 1 — Install required Python package

Open PowerShell/CMD inside your project folder:

pip install mysql-connector-python

✅ Step 2 — Create Database in MySQL
Open MySQL (Workbench / Command line) and run:

CREATE DATABASE result_management;

USE result_management;

CREATE TABLE students (
    roll_no VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    subject VARCHAR(100),
    marks INT
);

✅ Step 3 — Update database credentials
Open db_connection.py and update:

user="your_user_name"
password="your_pssword"
(Change to your actual MySQL username & password)

✅ Step 4 — Run the Project
From your terminal:

python result.py
The GUI window will open.

✅ How to Use the App
Enter Roll No, Name, Subject, Marks
Click Add → saves the student
Click Update → changes marks
Click Delete → removes record
Click Search → shows student & grade
All records appear in the table on the right

✅ Grade Calculation Logic
A → marks ≥ 90
B → marks ≥ 75
C → marks ≥ 60
F → marks < 60

✅ Project File Structure
Project Folder/
│── result.py
│── db_connection.py
│── README.md
