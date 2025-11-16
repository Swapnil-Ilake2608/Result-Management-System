import tkinter as tk
from tkinter import ttk, messagebox
# Import the backend logic from the subdirectory
from Result_Management_System.db_connection import connect, calculate_grade 

# Global entry variables (defined later in the GUI setup)
roll_no = None
name = None
subject = None
marks = None
student_table = None

# --- Database Functions (CRUD Operations) ---

def add_student():
    if not (roll_no.get() and name.get() and subject.get() and marks.get()):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        con = connect()
        if con is None:
            messagebox.showerror("Connection Error", "Could not connect to the database.")
            return

        cur = con.cursor()
        cur.execute("INSERT INTO students (roll_no, name, subject, marks) VALUES (%s, %s, %s, %s)",
                    (roll_no.get(), name.get(), subject.get(), marks.get()))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Student record added successfully!")
        clear_fields()
        fetch_data()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to add record: {str(e)}")

def fetch_data():
    con = connect()
    if con is None: return
    cur = con.cursor()
    cur.execute("SELECT roll_no, name, subject, marks FROM students")
    rows = cur.fetchall()
    student_table.delete(*student_table.get_children())
    for row in rows:
        marks_value = row[3]
        grade = calculate_grade(marks_value)
        student_table.insert("", tk.END, values=(row[0], row[1], row[2], marks_value, grade))
    con.close()

def update_student():
    if not (roll_no.get() and marks.get()):
        messagebox.showerror("Error", "Roll No and Marks required to update.")
        return
    try:
        con = connect()
        if con is None: return
        cur = con.cursor()
        cur.execute("UPDATE students SET marks = %s WHERE roll_no=%s", 
                    (marks.get(), roll_no.get()))
        con.commit()
        con.close()
        messagebox.showinfo("Updated", "Marks updated successfully!")
        clear_fields()
        fetch_data()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to update record: {str(e)}")

def delete_student():
    if not roll_no.get():
        messagebox.showerror("Error", "Enter Roll No to delete.")
        return
    try:
        con = connect()
        if con is None: return
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE roll_no=%s", (roll_no.get(),))
        con.commit()
        con.close()
        messagebox.showinfo("Deleted", "Student record deleted.")
        clear_fields()
        fetch_data()
    except Exception as e:
         messagebox.showerror("Database Error", f"Failed to delete record: {str(e)}")

def search_student():
    if not roll_no.get():
        messagebox.showerror("Error", "Enter Roll No to search.")
        return
    try:
        con = connect()
        if con is None: return
        cur = con.cursor()
        cur.execute("SELECT roll_no, name, subject, marks FROM students WHERE roll_no = %s", (roll_no.get(),))
        row = cur.fetchone()
        if row:
            clear_fields()
            roll_no.insert(0, row[0])
            name.insert(0, row[1])
            subject.insert(0, row[2])
            marks.insert(0, row[3])
            grade = calculate_grade(row[3])
            messagebox.showinfo("Result", f"Found record for {row[1]}. Grade: {grade}")
        else:
            messagebox.showwarning("Not Found", "No record found!")
        con.close()
    except Exception as e:
         messagebox.showerror("Database Error", f"Failed to search: {str(e)}")

def clear_fields():
    roll_no.delete(0, tk.END)
    name.delete(0, tk.END)
    subject.delete(0, tk.END)
    marks.delete(0, tk.END)

# --- GUI Setup (Removed green border, colorful theme retained) ---

root = tk.Tk()
root.title("Result Management System")
root.geometry("1000x620")
root.configure(bg="#FFF8F0")

style = ttk.Style(root)
try:
    style.theme_use('clam')
except Exception:
    pass

ACCENT = '#ff6b6b'
SECOND = '#ffd93d'
CARD_BG = '#ffffff'
TEXT = '#222222'
SUB = '#6b6b6b'

style.configure('Header.TLabel', font=('Segoe UI', 20, 'bold'), foreground='white', background=ACCENT)
style.configure('SubHeader.TLabel', font=('Segoe UI', 10), foreground=SUB, background='#FFF8F0')
style.configure('TEntry', padding=6)
style.configure('TButton', padding=6, font=('Segoe UI', 10))
style.configure('Accent.TButton', background=ACCENT, foreground='white', font=('Segoe UI', 10, 'bold'))
style.configure('Treeview', font=('Segoe UI', 10), rowheight=28, background='#FFF', fieldbackground='#FFF')
style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background=SECOND, foreground=TEXT)

header = tk.Frame(root, bg=ACCENT)
header.pack(fill=tk.X)
ttk.Label(header, text=' Result Management System ', style='Header.TLabel').pack(padx=10, pady=12)
ttk.Label(root, text='Add / Update / Delete student results — grade is calculated automatically.', style='SubHeader.TLabel').pack(pady=(8, 6))

content = ttk.Frame(root, padding=(12, 12, 12, 12))
content.pack(fill=tk.BOTH, expand=True)

content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)

left = ttk.Frame(content)
left.grid(row=0, column=0, sticky='nsew', padx=(0, 12), pady=6)

# Removed green border (no PANEL background)
form_card = tk.LabelFrame(left, text=' Student Details ', bg=CARD_BG, bd=1, relief=tk.RIDGE, padx=12, pady=12, fg=TEXT)
form_card.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

lbl_roll = ttk.Label(form_card, text='Roll No')
lbl_roll.grid(row=0, column=0, sticky='w', pady=6)
roll_no = ttk.Entry(form_card, width=30)
roll_no.grid(row=0, column=1, pady=6, padx=8)

lbl_name = ttk.Label(form_card, text='Name')
lbl_name.grid(row=1, column=0, sticky='w', pady=6)
name = ttk.Entry(form_card, width=30)
name.grid(row=1, column=1, pady=6, padx=8)

lbl_subject = ttk.Label(form_card, text='Subject')
lbl_subject.grid(row=2, column=0, sticky='w', pady=6)
subject = ttk.Entry(form_card, width=30)
subject.grid(row=2, column=1, pady=6, padx=8)

lbl_marks = ttk.Label(form_card, text='Marks')
lbl_marks.grid(row=3, column=0, sticky='w', pady=6)
marks = ttk.Entry(form_card, width=30)
marks.grid(row=3, column=1, pady=6, padx=8)

btns = ttk.Frame(form_card)
btns.grid(row=4, column=0, columnspan=2, pady=(12, 0))

ttk.Button(btns, text='➕ Add', style='Accent.TButton', command=add_student).grid(row=0, column=0, padx=6)
ttk.Button(btns, text='✏️ Update', style='Accent.TButton', command=update_student).grid(row=0, column=1, padx=6)
ttk.Button(btns, text='🗑️ Delete', style='Accent.TButton', command=delete_student).grid(row=0, column=2, padx=6)
ttk.Button(btns, text='🔎 Search', style='Accent.TButton', command=search_student).grid(row=0, column=3, padx=6)
ttk.Button(btns, text='Clear', command=clear_fields).grid(row=0, column=4, padx=6)

right = ttk.Frame(content)
right.grid(row=0, column=1, sticky='nsew', pady=6)
right.columnconfigure(0, weight=1)
right.rowconfigure(0, weight=1)

table_card = tk.LabelFrame(right, text=' Records ', bg=CARD_BG, bd=1, relief=tk.RIDGE, padx=8, pady=8, fg=TEXT)
table_card.grid(row=0, column=0, sticky='nsew', padx=6, pady=6)

scroll_y = ttk.Scrollbar(table_card, orient=tk.VERTICAL)
scroll_x = ttk.Scrollbar(table_card, orient=tk.HORIZONTAL)

student_table = ttk.Treeview(table_card, columns=("Roll No", "Name", "Subject", "Marks", "Grade"),
                             show='headings', yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.config(command=student_table.yview)
scroll_x.config(command=student_table.xview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

for col in ("Roll No", "Name", "Subject", "Marks", "Grade"):
    student_table.heading(col, text=col)
    student_table.column(col, anchor=tk.CENTER, width=120, minwidth=80)
student_table.pack(fill=tk.BOTH, expand=True)

status = tk.Label(root, text='Ready', anchor='w', bg='#E8F6EF', fg=TEXT, padx=6)
status.pack(side=tk.BOTTOM, fill=tk.X)

def set_status(msg):
    status.config(text=msg)

fetch_data()
root.mainloop()
