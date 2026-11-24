import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os

# ==========================================================
# COLOURS
# ==========================================================

BG = "#F1F5FB"
NAVY = "#243B67"
BLUE = "#4969D8"
WHITE = "#FFFFFF"
GREY = "#718096"
GREEN = "#16A085"
RED = "#E05252"

FILE = "studentMarks.txt"

students = []


# ==========================================================
# FILE HANDLING
# ==========================================================

def load_students():
    global students
    students = []

    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            f.write("0\n")
        return

    try:
        with open(FILE, "r", newline="") as f:
            lines = list(csv.reader(f))

        if not lines:
            return

        for row in lines[1:]:
            if not row:
                continue

            if len(row) == 6:
                code, name, c1, c2, c3, exam = row
            elif len(row) == 5:
                code, c1, c2, c3, exam = row
                name = "Student " + code
            else:
                continue

            students.append({
                "code": code,
                "name": name,
                "c1": int(c1),
                "c2": int(c2),
                "c3": int(c3),
                "exam": int(exam)
            })

    except (ValueError, OSError):
        messagebox.showerror(
            "File Error",
            "Could not read studentMarks.txt. Check the file format."
        )


def save_students():
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([len(students)])

        for s in students:
            writer.writerow([
                s["code"], s["name"],
                s["c1"], s["c2"], s["c3"], s["exam"]
            ])


# ==========================================================
# CALCULATIONS
# ==========================================================

def coursework(s):
    return s["c1"] + s["c2"] + s["c3"]


def total(s):
    return coursework(s) + s["exam"]


def percentage(s):
    return total(s) / 160 * 100


def grade(s):
    p = percentage(s)

    if p >= 70:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C"
    elif p >= 40:
        return "D"
    return "F"


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("1200x750")
root.minsize(950, 600)
root.configure(bg=BG)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=NAVY,
    rowheight=35,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Arial", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", BLUE)],
    foreground=[("selected", WHITE)]
)


# ==========================================================
# SIDEBAR
# ==========================================================

sidebar = tk.Frame(root, bg=NAVY, width=220)
sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
sidebar.grid_propagate(False)

tk.Label(
    sidebar,
    text="🎓 STUDENT HUB",
    font=("Arial", 17, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(35, 45))


# ==========================================================
# MAIN CONTENT
# ==========================================================

main = tk.Frame(root, bg=BG)
main.grid(row=1, column=1, sticky="nsew", padx=25, pady=20)

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(3, weight=1)


# Top bar

top = tk.Frame(root, bg=WHITE, height=65)
top.grid(row=0, column=1, sticky="ew")
top.grid_propagate(False)

tk.Label(
    top,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 14, "bold"),
    fg=NAVY,
    bg=WHITE
).pack(side="left", padx=25, pady=20)

tk.Label(
    top,
    text="Academic Portal",
    font=("Arial", 10),
    fg=GREY,
    bg=WHITE
).pack(side="right", padx=25)


# Heading

tk.Label(
    main,
    text="Dashboard",
    font=("Arial", 25, "bold"),
    fg=NAVY,
    bg=BG
).grid(row=0, column=0, sticky="w")

tk.Label(
    main,
    text="Manage student records and academic performance.",
    font=("Arial", 11),
    fg=GREY,
    bg=BG
).grid(row=1, column=0, sticky="w", pady=(5, 20))


# ==========================================================
# STATISTICS CARDS
# ==========================================================

stats = tk.Frame(main, bg=BG)
stats.grid(row=2, column=0, sticky="ew", pady=(0, 20))

for i in range(3):
    stats.grid_columnconfigure(i, weight=1)


def make_stat(column, title, colour):
    card = tk.Frame(
        stats,
        bg=WHITE,
        padx=18,
        pady=15,
        highlightbackground="#DCE5F2",
        highlightthickness=1
    )
    card.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=7
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 10),
        fg=GREY,
        bg=WHITE
    ).pack(anchor="w")

    value = tk.Label(
        card,
        text="0",
        font=("Arial", 22, "bold"),
        fg=colour,
        bg=WHITE
    )
    value.pack(anchor="w", pady=(7, 0))

    return value


total_value = make_stat(0, "TOTAL STUDENTS", BLUE)
average_value = make_stat(1, "CLASS AVERAGE", GREEN)
highest_value = make_stat(2, "HIGHEST MARK", RED)


# ==========================================================
# STUDENT RECORDS PANEL
# ==============================================================

results_card = tk.Frame(
    main,
    bg=WHITE,
    padx=20,
    pady=20
)

results_card.grid(row=3, column=0, sticky="nsew")

results_card.grid_columnconfigure(0, weight=1)
results_card.grid_rowconfigure(1, weight=1)

tk.Label(
    results_card,
    text="📋 STUDENT RECORDS",
    font=("Arial", 15, "bold"),
    fg=NAVY,
    bg=WHITE
).grid(row=0, column=0, sticky="w", pady=(0, 15))


# ==========================================================
# TABLE
# ==========================================================

table_frame = tk.Frame(results_card, bg=WHITE)
table_frame.grid(row=1, column=0, sticky="nsew")

table_frame.grid_columnconfigure(0, weight=1)
table_frame.grid_rowconfigure(0, weight=1)

columns = (
    "code", "name", "c1", "c2", "c3",
    "exam", "total", "percentage", "grade"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

headings = {
    "code": "Student Code",
    "name": "Name",
    "c1": "Course 1",
    "c2": "Course 2",
    "c3": "Course 3",
    "exam": "Exam",
    "total": "Total",
    "percentage": "Percentage",
    "grade": "Grade"
}

for col in columns:
    tree.heading(col, text=headings[col])
    tree.column(col, anchor="center", width=100)

tree.column("name", width=150)

tree.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

scrollbar.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)


# ==========================================================
# DISPLAY FUNCTIONS
# ==========================================================

def refresh_table(data=None):
    tree.delete(*tree.get_children())

    if data is None:
        data = students

    for s in data:
        tree.insert("", "end", values=(
            s["code"],
            s["name"],
            s["c1"],
            s["c2"],
            s["c3"],
            s["exam"],
            total(s),
            f"{percentage(s):.2f}%",
            grade(s)
        ))

    update_stats()


def update_stats():
    count = len(students)

    total_value.config(text=str(count))

    if count:
        avg = sum(percentage(s) for s in students) / count
        highest = max(percentage(s) for s in students)

        average_value.config(text=f"{avg:.2f}%")
        highest_value.config(text=f"{highest:.2f}%")
    else:
        average_value.config(text="0%")
        highest_value.config(text="0%")


def display_students():
    refresh_table()
    messagebox.showinfo(
        "Student Records",
        f"Displaying {len(students)} student records."
    )


# ==========================================================
# SEARCH STUDENT
# ==========================================================

def find_student(code):
    for s in students:
        if s["code"] == code:
            return s
    return None


def view_individual():
    code = simpledialog.askstring(
        "Search Student",
        "Enter student code:"
    )

    if code is None:
        return

    student = find_student(code.strip())

    if student:
        refresh_table([student])
    else:
        messagebox.showerror(
            "Not Found",
            "Student code does not exist."
        )


# ==========================================================
# HIGHEST AND LOWEST
# ==========================================================

def highest_student():
    if not students:
        messagebox.showwarning("Empty", "No students available.")
        return

    s = max(students, key=percentage)
    refresh_table([s])

    messagebox.showinfo(
        "Highest Student",
        f"Name: {s['name']}\n"
        f"Code: {s['code']}\n"
        f"Percentage: {percentage(s):.2f}%\n"
        f"Grade: {grade(s)}"
    )


def lowest_student():
    if not students:
        messagebox.showwarning("Empty", "No students available.")
        return

    s = min(students, key=percentage)
    refresh_table([s])

    messagebox.showinfo(
        "Lowest Student",
        f"Name: {s['name']}\n"
        f"Code: {s['code']}\n"
        f"Percentage: {percentage(s):.2f}%\n"
        f"Grade: {grade(s)}"
    )


# ==========================================================
# SORT STUDENTS
# ==========================================================

def sort_students():
    if not students:
        messagebox.showwarning("Empty", "No records to sort.")
        return

    ordered = sorted(
        students,
        key=percentage,
        reverse=True
    )

    refresh_table(ordered)


# ==========================================================
# ADD / UPDATE STUDENT FORM
# ==========================================================

def student_form(existing=None):

    window = tk.Toplevel(root)
    window.title("Student Details")
    window.geometry("390x480")
    window.configure(bg=WHITE)
    window.resizable(False, False)
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="Student Information",
        font=("Arial", 19, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack(pady=20)

    fields = [
        ("Student Code", "code"),
        ("Student Name", "name"),
        ("Course 1 (/20)", "c1"),
        ("Course 2 (/20)", "c2"),
        ("Course 3 (/20)", "c3"),
        ("Exam (/100)", "exam")
    ]

    entries = {}

    for label, key in fields:
        tk.Label(
            window,
            text=label,
            font=("Arial", 10, "bold"),
            fg=NAVY,
            bg=WHITE
        ).pack(anchor="w", padx=35)

        entry = tk.Entry(
            window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        entry.pack(fill="x", padx=35, pady=(4, 10))

        if existing:
            entry.insert(0, str(existing[key]))

        entries[key] = entry

    def save_form():
        try:
            code = entries["code"].get().strip()
            name = entries["name"].get().strip()

            if not code.isdigit() or not 1000 <= int(code) <= 9999:
                raise ValueError("Code must be between 1000 and 9999.")

            if not name:
                raise ValueError("Enter a student name.")

            marks = {
                "c1": int(entries["c1"].get()),
                "c2": int(entries["c2"].get()),
                "c3": int(entries["c3"].get()),
                "exam": int(entries["exam"].get())
            }

            for key in ("c1", "c2", "c3"):
                if not 0 <= marks[key] <= 20:
                    raise ValueError("Course marks must be 0 to 20.")

            if not 0 <= marks["exam"] <= 100:
                raise ValueError("Exam mark must be 0 to 100.")

            if any(
                s["code"] == code and s is not existing
                for s in students
            ):
                raise ValueError("This student code already exists.")

            record = {
                "code": code,
                "name": name,
                **marks
            }

            if existing:
                existing.update(record)
            else:
                students.append(record)

            save_students()
            refresh_table()
            window.destroy()

            messagebox.showinfo(
                "Success",
                "Student record saved successfully!"
            )

        except ValueError as error:
            messagebox.showerror("Invalid Information", str(error))

    tk.Button(
        window,
        text="SAVE STUDENT",
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=save_form
    ).pack(fill="x", padx=35, pady=15)


# ==========================================================
# ADD STUDENT
# ==========================================================

def add_student():
    student_form()


# ==========================================================
# UPDATE STUDENT
# ==========================================================

def update_student():
    selected = tree.selection()

    if selected:
        code = str(tree.item(selected[0])["values"][0])
    else:
        code = simpledialog.askstring(
            "Update Student",
            "Enter student code:"
        )

    if code is None:
        return

    student = find_student(code.strip())

    if student:
        student_form(student)
    else:
        messagebox.showerror("Not Found", "Student not found.")


# ==========================================================
# DELETE STUDENT
# ==========================================================

def delete_student():
    selected = tree.selection()

    if selected:
        code = str(tree.item(selected[0])["values"][0])
    else:
        code = simpledialog.askstring(
            "Delete Student",
            "Enter student code:"
        )

    if code is None:
        return

    student = find_student(code.strip())

    if not student:
        messagebox.showerror("Not Found", "Student not found.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete {student['name']}?"
    )

    if confirm:
        students.remove(student)
        save_students()
        refresh_table()

        messagebox.showinfo(
            "Deleted",
            "Student record deleted successfully."
        )


# ==========================================================
# MENU BUTTONS
# ==========================================================

def menu_button(text, command, colour=BLUE):
    return tk.Button(
        sidebar,
        text=text,
        font=("Arial", 11, "bold"),
        bg=NAVY,
        fg=WHITE,
        activebackground=colour,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=22,
        pady=13,
        cursor="hand2",
        command=command
    )


menu_items = [
    ("🏠  Dashboard", lambda: refresh_table()),
    ("📋  View All", display_students),
    ("🔍  Search Student", view_individual),
    ("🏆  Highest Student", highest_student),
    ("📉  Lowest Student", lowest_student),
    ("↕️  Sort Records", sort_students),
    ("➕  Add Student", add_student),
    ("✏️  Update Student", update_student),
    ("🗑  Delete Student", delete_student)
]

for text, command in menu_items:
    menu_button(text, command).pack(fill="x", pady=2)


# Exit button

menu_button(
    "✖  Exit",
    root.destroy,
    RED
).pack(side="bottom", fill="x", pady=20)


# ==========================================================
# START PROGRAM
# ==========================================================

load_students()
refresh_table()

root.mainloop()


