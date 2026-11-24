import tkinter as tk
from tkinter import messagebox
import random
import os

# Load jokes
def load_jokes():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "randomJokes.txt")

    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        jokes = []
        for i in range(0, len(lines) - 1, 2):
            jokes.append((lines[i], lines[i + 1]))

        return jokes

    except FileNotFoundError:
        messagebox.showerror("Error", "randomJokes.txt was not found!")
        return []

# Tell a joke
def tell_joke():
    global current_joke

    if not jokes:
        messagebox.showerror("Error", "No jokes available!")
        return

    current_joke = random.choice(jokes)

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="Click Show Punchline to reveal!")

# Show punchline
def show_punchline():
    if current_joke is None:
        messagebox.showinfo("Wait!", "Please select a joke first!")
    else:
        punchline_label.config(text=current_joke[1])

# Quit application
def quit_app():
    window.destroy()

# Main window
window = tk.Tk()
window.title("Alexa Joke Assistant")
window.geometry("550x450")
window.config(bg="#202A44")
window.resizable(False, False)

current_joke = None
jokes = load_jokes()

# Heading
tk.Label(
    window,
    text="😂 Alexa Joke Assistant",
    font=("Arial", 24, "bold"),
    bg="#202A44",
    fg="white"
).pack(pady=25)

# Instructions
tk.Label(
    window,
    text="Ready for a laugh? Click the button below!",
    font=("Arial", 12),
    bg="#202A44",
    fg="white"
).pack(pady=5)

# Joke setup
setup_label = tk.Label(
    window,
    text="Your joke will appear here!",
    font=("Arial", 16, "bold"),
    bg="#202A44",
    fg="#FFD166",
    wraplength=480
)
setup_label.pack(pady=25)

# Punchline
punchline_label = tk.Label(
    window,
    text="",
    font=("Arial", 14),
    bg="#202A44",
    fg="#06D6A0",
    wraplength=480
)
punchline_label.pack(pady=10)

# Buttons
tk.Button(
    window,
    text="Alexa tell me a Joke",
    font=("Arial", 12, "bold"),
    bg="#118AB2",
    fg="white",
    width=25,
    command=tell_joke
).pack(pady=7)

tk.Button(
    window,
    text="Show Punchline",
    font=("Arial", 12, "bold"),
    bg="#06D6A0",
    fg="black",
    width=25,
    command=show_punchline
).pack(pady=7)

tk.Button(
    window,
    text="Next Joke",
    font=("Arial", 12, "bold"),
    bg="#FFD166",
    fg="black",
    width=25,
    command=tell_joke
).pack(pady=7)

tk.Button(
    window,
    text="Quit",
    font=("Arial", 12, "bold"),
    bg="#EF476F",
    fg="white",
    width=25,
    command=quit_app
).pack(pady=7)

window.mainloop()

