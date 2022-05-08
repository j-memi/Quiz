import tkinter as tk


def show_frame(frame):
    frame.tkraise()


# Set up the main window
window = tk.Tk()
window.title("Quiz")
window.configure(background="white")
window.rowconfigure([0, 1], weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')

# Set up different frames
title_frame = tk.Frame(window, bg="white")
load_quiz_frame = tk.Frame(window, bg="white")
quiz_frame = tk.Frame(window, bg="white")

for frame in (title_frame, load_quiz_frame, quiz_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Code for Title Screen
welcome = tk.Frame(title_frame, bg="white")
welcome.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=18,
    pady=100
    )
label = tk.Label(
    master=welcome,
    text="Welcome!",
    font=("Helvetica", 32),
    bg="white"
)
label.pack()
label = tk.Label(
    master=welcome,
    text="Create your own or load a quiz using the corresponding "
    "buttons below!",
    font=("Helvetica", 24),
    bg="white"
    )
label.pack()
buttons = tk.Frame(title_frame, bg="white")
create_button = tk.Button(
    master=buttons,
    text="Create Quiz",
    width=12,
    padx=90,
    pady=80,
    bd=0, bg="lightblue",
    activebackground="#5391b0",
    font=("Helvetica", 40),
    command=lambda: show_frame(load_quiz_frame)
)
create_button.grid(row=0, column=0, sticky="ew", padx=106, pady=50)
load_button = tk.Button(
    master=buttons,
    text="Load Quiz",
    width=12,
    padx=90,
    pady=80,
    bd=0,
    bg="lightblue",
    activebackground="#5391b0",
    font=("Helvetica", 40),
    command=lambda: show_frame(load_quiz_frame)
    )
load_button.grid(row=0, column=1, sticky="ew", padx=106, pady=50)
buttons.grid(row=1, column=0, sticky="ew")
show_frame(title_frame)

# Run mainloop
if __name__ == '__main__':
    window.mainloop()
