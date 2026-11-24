
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv, os

BG, NAVY, BLUE, WHITE = "#F1F5FB", "#243B67", "#4969D8", "#FFFFFF"
GREY, GREEN, RED = "#718096", "#16A085", "#E05252"
FILE = "studentMarks.txt"
students = []

# FILE HANDLING
def load_students():
    global students
    students = []
    if not os.path.exists(FILE):
        save_students()
        return
    try:
        with open(FILE, newline="") as f:
            rows = list(csv.reader(f))[1:]
        for r in rows:
            if len(r) == 5:
                code, c1, c2, c3, exam = r
                name = "Student " + code
            elif len(r) == 6:
                code, name, c1, c2, c3, exam = r
            else:
                continue
            students.append(dict(code=code, name=name,
                c1=int(c1), c2=int(c2), c3=int(c3), exam=int(exam)))
    except (ValueError, OSError):
        messagebox.showerror("File Error", "Check studentMarks.txt format.")

def save_students():
    with open(FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([len(students)])
        for s in students:
            w.writerow([s[k] for k in ("code","name","c1","c2","c3","exam")])

# CALCULATIONS
def coursework(s): return s["c1"] + s["c2"] + s["c3"]
def total(s): return coursework(s) + s["exam"]
def percentage(s): return total(s) / 160 * 100

def grade(s):
    p = percentage(s)
    return "A" if p >= 70 else "B" if p >= 60 else "C" if p >= 50 else "D" if p >= 40 else "F"

def find_student(code):
    return next((s for s in students if s["code"] == code), None)

# MAIN WINDOW
root = tk.Tk()
root.title("Student Management System")
root.geometry("1200x750")
root.minsize(950, 600)
root.configure(bg=BG)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=WHITE, foreground=NAVY,
                fieldbackground=WHITE, rowheight=35, font=("Arial", 10))
style.configure("Treeview.Heading", background=NAVY, foreground=WHITE,
                font=("Arial", 10, "bold"), padding=10)
style.map("Treeview", background=[("selected", BLUE)],
          foreground=[("selected", WHITE)])

# SIDEBAR
sidebar = tk.Frame(root, bg=NAVY, width=220)
sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
sidebar.grid_propagate(False)

tk.Label(sidebar, text="🎓 STUDENT HUB", font=("Arial",17,"bold"),
         bg=NAVY, fg=WHITE).pack(pady=(35,45))

# TOP BAR
top = tk.Frame(root, bg=WHITE, height=65)
top.grid(row=0, column=1, sticky="ew")
top.grid_propagate(False)

tk.Label(top, text="STUDENT MANAGEMENT SYSTEM",
         font=("Arial",14,"bold"), fg=NAVY, bg=WHITE).pack(side="left", padx=25, pady=20)
tk.Label(top, text="Academic Portal", fg=GREY,
         bg=WHITE).pack(side="right", padx=25)

# MAIN CONTENT
main = tk.Frame(root, bg=BG)
main.grid(row=1, column=1, sticky="nsew", padx=25, pady=20)
main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(3, weight=1)

tk.Label(main, text="Dashboard", font=("Arial",25,"bold"),
         fg=NAVY, bg=BG).grid(row=0, column=0, sticky="w")
tk.Label(main, text="Manage student records and academic performance.",
         fg=GREY, bg=BG).grid(row=1, column=0, sticky="w", pady=(5,20))

# STATISTICS
stats = tk.Frame(main, bg=BG)
stats.grid(row=2, column=0, sticky="ew", pady=(0,20))
for i in range(3):
    stats.grid_columnconfigure(i, weight=1)

def make_stat(i, title, colour):
    card = tk.Frame(stats, bg=WHITE, padx=18, pady=15,
                    highlightbackground="#DCE5F2", highlightthickness=1)
    card.grid(row=0, column=i, sticky="ew", padx=7)
    tk.Label(card, text=title, fg=GREY, bg=WHITE).pack(anchor="w")
    value = tk.Label(card, text="0", font=("Arial",22,"bold"),
                     fg=colour, bg=WHITE)
    value.pack(anchor="w", pady=(7,0))
    return value

total_value = make_stat(0, "TOTAL STUDENTS", BLUE)
average_value = make_stat(1, "CLASS AVERAGE", GREEN)
highest_value = make_stat(2, "HIGHEST MARK", RED)

# RECORDS PANEL
panel = tk.Frame(main, bg=WHITE, padx=20, pady=20)
panel.grid(row=3, column=0, sticky="nsew")
panel.grid_columnconfigure(0, weight=1)
panel.grid_rowconfigure(1, weight=1)

tk.Label(panel, text="📋 STUDENT RECORDS", font=("Arial",15,"bold"),
         fg=NAVY, bg=WHITE).grid(row=0, column=0, sticky="w", pady=(0,15))

frame = tk.Frame(panel, bg=WHITE)
frame.grid(row=1, column=0, sticky="nsew")
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

columns = ("code","name","c1","c2","c3","exam","total","percentage","grade")
headings = ("Student Code","Name","Course 1","Course 2","Course 3",
            "Exam","Total","Percentage","Grade")

tree = ttk.Treeview(frame, columns=columns, show="headings")
for c, h in zip(columns, headings):
    tree.heading(c, text=h)
    tree.column(c, anchor="center", width=100)
tree.column("name", width=150)
tree.grid(row=0, column=0, sticky="nsew")

scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scroll.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=scroll.set)

# DISPLAY AND STATISTICS
def update_stats():
    n = len(students)
    total_value.config(text=str(n))
    average_value.config(text=f"{sum(map(percentage,students))/n:.2f}%" if n else "0%")
    highest_value.config(text=f"{max(map(percentage,students)):.2f}%" if n else "0%")

def refresh_table(data=None):
    tree.delete(*tree.get_children())
    for s in students if data is None else data:
        tree.insert("", "end", values=(
            s["code"], s["name"], s["c1"], s["c2"], s["c3"],
            s["exam"], total(s), f"{percentage(s):.2f}%", grade(s)))
    update_stats()

def display_students():
    refresh_table()
    messagebox.showinfo("Student Records", f"Displaying {len(students)} student records.")

# SEARCH
def view_individual():
    code = simpledialog.askstring("Search Student", "Enter student code:")
    if code is None: return
    s = find_student(code.strip())
    if s: refresh_table([s])
    else: messagebox.showerror("Not Found", "Student code does not exist.")

# HIGHEST AND LOWEST
def show_student(highest=True):
    if not students:
        messagebox.showwarning("Empty", "No students available.")
        return
    s = (max if highest else min)(students, key=percentage)
    refresh_table([s])
    messagebox.showinfo("Student Result",
        f"Name: {s['name']}\nCode: {s['code']}\n"
        f"Percentage: {percentage(s):.2f}%\nGrade: {grade(s)}")

def sort_students():
    if students:
        refresh_table(sorted(students, key=percentage, reverse=True))
    else:
        messagebox.showwarning("Empty", "No records to sort.")

# ADD AND UPDATE
def student_form(existing=None):
    win = tk.Toplevel(root)
    win.title("Student Details")
    win.geometry("390x480")
    win.configure(bg=WHITE)
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    tk.Label(win, text="Student Information", font=("Arial",19,"bold"),
             fg=NAVY, bg=WHITE).pack(pady=20)

    fields = [("Student Code","code"),("Student Name","name"),
              ("Course 1 (/20)","c1"),("Course 2 (/20)","c2"),
              ("Course 3 (/20)","c3"),("Exam (/100)","exam")]
    entries = {}

    for label, key in fields:
        tk.Label(win, text=label, font=("Arial",10,"bold"),
                 fg=NAVY, bg=WHITE).pack(anchor="w", padx=35)
        e = tk.Entry(win, font=("Arial",11), relief="solid", bd=1)
        e.pack(fill="x", padx=35, pady=(4,10))
        if existing: e.insert(0, str(existing[key]))
        entries[key] = e

    def save_form():
        try:
            code, name = entries["code"].get().strip(), entries["name"].get().strip()
            if not code.isdigit() or not 1000 <= int(code) <= 9999:
                raise ValueError("Code must be between 1000 and 9999.")
            if not name: raise ValueError("Enter a student name.")

            marks = {k:int(entries[k].get()) for k in ("c1","c2","c3","exam")}
            if any(not 0 <= marks[k] <= 20 for k in ("c1","c2","c3")):
                raise ValueError("Course marks must be 0 to 20.")
            if not 0 <= marks["exam"] <= 100:
                raise ValueError("Exam mark must be 0 to 100.")
            if any(s["code"] == code and s is not existing for s in students):
                raise ValueError("This student code already exists.")

            record = {"code":code, "name":name, **marks}
            if existing: existing.update(record)
            else: students.append(record)

            save_students()
            refresh_table()
            win.destroy()
            messagebox.showinfo("Success", "Student record saved successfully!")
        except ValueError as e:
            messagebox.showerror("Invalid Information", str(e))

    tk.Button(win, text="SAVE STUDENT", font=("Arial",11,"bold"),
              bg=BLUE, fg=WHITE, activebackground=NAVY,
              relief="flat", cursor="hand2", command=save_form).pack(
                  fill="x", padx=35, pady=15)

def add_student():
    student_form()

def update_student():
    selected = tree.selection()
    code = str(tree.item(selected[0])["values"][0]) if selected else simpledialog.askstring(
        "Update Student", "Enter student code:")
    if code is None: return
    s = find_student(code.strip())
    if s: student_form(s)
    else: messagebox.showerror("Not Found", "Student not found.")

# DELETE
def delete_student():
    selected = tree.selection()
    code = str(tree.item(selected[0])["values"][0]) if selected else simpledialog.askstring(
        "Delete Student", "Enter student code:")
    if code is None: return
    s = find_student(code.strip())
    if not s:
        messagebox.showerror("Not Found", "Student not found.")
    elif messagebox.askyesno("Confirm Delete", f"Delete {s['name']}?"):
        students.remove(s)
        save_students()
        refresh_table()
        messagebox.showinfo("Deleted", "Student record deleted successfully.")

# MENU
def menu_button(text, command, colour=BLUE):
    return tk.Button(sidebar, text=text, font=("Arial",11,"bold"),
        bg=NAVY, fg=WHITE, activebackground=colour, activeforeground=WHITE,
        relief="flat", anchor="w", padx=22, pady=13,
        cursor="hand2", command=command)

menu_items = [
    ("🏠  Dashboard", lambda:refresh_table()),
    ("📋  View All", display_students),
    ("🔍  Search Student", view_individual),
    ("🏆  Highest Student", lambda:show_student(True)),
    ("📉  Lowest Student", lambda:show_student(False)),
    ("↕️  Sort Records", sort_students),
    ("➕  Add Student", add_student),
    ("✏️  Update Student", update_student),
    ("🗑  Delete Student", delete_student)
]

for text, command in menu_items:
    menu_button(text, command).pack(fill="x", pady=2)

menu_button("✖  Exit", root.destroy, RED).pack(side="bottom", fill="x", pady=20)

# START
load_students()
refresh_table()
root.mainloop()