import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Math Quiz")
root.geometry("800x600")
root.resizable(False, False)

# TEST Github alignment

# Background image
try:
    background = tk.PhotoImage(
        file="Colourful maths background.png"
    )

    bg_label = tk.Label(root, image=background)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

except:
    root.configure(bg="lightblue")


# Variables
score = 0
number = 0
difficulty = "Easy"
questions = []

# Main frame
frame = tk.Frame(root, bg="lightblue")
frame.place(relx=0.5, rely=0.5, anchor="center")


def clear_screen():
    for widget in frame.winfo_children():
        widget.destroy()


# Main menu
def menu():

    clear_screen()

    tk.Label(frame, text="Math Quiz",
             font=("Arial", 28, "bold"),
             bg="lightblue").pack(pady=20)

    tk.Label(frame, text="Select Difficulty",
             font=("Arial", 16),
             bg="lightblue").pack(pady=10)

    tk.Button(frame, text="Easy", width=20,
              command=lambda: start_game("Easy")).pack(pady=5)

    tk.Button(frame, text="Medium", width=20,
              command=lambda: start_game("Medium")).pack(pady=5)

    tk.Button(frame, text="Hard", width=20,
              command=lambda: start_game("Hard")).pack(pady=5)


# Create questions
def make_questions():

    global questions
    questions = []

    for i in range(10):

        if difficulty == "Easy":
            a = random.randint(1, 10)
            b = random.randint(1, 10)

        elif difficulty == "Medium":
            a = random.randint(10, 30)
            b = random.randint(1, 15)

        else:
            a = random.randint(20, 100)
            b = random.randint(2, 20)

        operation = random.choice(["+", "-", "*"])

        if operation == "+":
            answer = a + b

        elif operation == "-":
            answer = a - b

        else:
            answer = a * b

        choices = [answer]

        while len(choices) < 4:
            wrong = answer + random.randint(-10, 10)

            if wrong not in choices:
                choices.append(wrong)

        random.shuffle(choices)

        question = str(a) + " " + operation + " " + str(b) + " = ?"

        questions.append([question, answer, choices])


# Start game
def start_game(level):

    global score, number, difficulty

    difficulty = level
    score = 0
    number = 0

    make_questions()
    show_question()


# Display questions
def show_question():

    clear_screen()

    if number == 10:
        result()
        return

    question = questions[number]

    tk.Label(frame, text="Question " + str(number + 1) + " of 10",
             font=("Arial", 16, "bold"),
             bg="lightblue").pack(pady=10)

    tk.Label(frame, text=question[0],
             font=("Arial", 25, "bold"),
             bg="lightblue").pack(pady=20)

    feedback = tk.Label(frame, text="Choose your answer",
                        font=("Arial", 12),
                        bg="lightblue")
    feedback.pack(pady=10)

    buttons = []

    def check_answer(choice):

        global score

        for button in buttons:
            button.config(state="disabled")

        if choice == question[1]:
            score += 1
            feedback.config(text="Correct!", fg="green")

        else:
            feedback.config(
                text="Wrong! Answer: " + str(question[1]),
                fg="red"
            )

        next_button.pack(pady=15)

    for choice in question[2]:

        button = tk.Button(
            frame,
            text=str(choice),
            width=15,
            font=("Arial", 13),
            command=lambda x=choice: check_answer(x)
        )

        button.pack(pady=5)
        buttons.append(button)

    def next_question():

        global number

        number += 1
        show_question()

    next_button = tk.Button(
        frame,
        text="Next Question",
        width=18,
        command=next_question
    )


# Show final score
def result():

    clear_screen()

    tk.Label(frame, text="Quiz Finished!",
             font=("Arial", 26, "bold"),
             bg="lightblue").pack(pady=20)

    tk.Label(frame, text="Your Score: " + str(score) + "/10",
             font=("Arial", 22),
             bg="lightblue").pack(pady=20)

    if score >= 8:
        message = "Excellent work!"

    elif score >= 5:
        message = "Good job!"

    else:
        message = "Keep practising!"

    tk.Label(frame, text=message,
             font=("Arial", 16),
             bg="lightblue").pack(pady=10)

    tk.Button(frame, text="Play Again",
              width=20, command=menu).pack(pady=10)

    tk.Button(frame, text="Exit",
              width=20, command=root.destroy).pack(pady=5)


# Run program
menu()
root.mainloop()


