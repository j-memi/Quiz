import tkinter as tk


def show_frame(frame):
    frame.tkraise()


# Set up the main window
window = tk.Tk()
window.title("Quiz")
window.configure(background="white")
window.minsize(width=1000, height=800)
window.rowconfigure([0, 1], weight=1)
window.columnconfigure(0, weight=1)
window.state("zoomed")

# Set up different frames
title_frame = tk.Frame(window, bg="white")
load_quiz_frame = tk.Frame(window, bg="white")
quiz_frame = tk.Frame(window, bg="white")

for frame in (title_frame, load_quiz_frame, quiz_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# ---------- Code for Title Screen ----------
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

# ---------- Code for Load Quiz Screen ----------
# Heading text
heading = tk.Label(
    master=load_quiz_frame,
    text="Choose a quiz!",
    font=("Helvetica", 32),
    bg="white"
    )
heading.grid(row=0, column=0, padx=150, pady=100)
# Quiz Selector
load_quiz_frame.grid_columnconfigure(0, weight=1)
canvas_container = tk.Canvas(load_quiz_frame, height=480)
options = tk.Frame(canvas_container)
scrollbar = tk.Scrollbar(
    load_quiz_frame,
    orient="vertical",
    command=canvas_container.yview
    )
canvas_container.create_window(
    (0, 0),
    window=options,
    anchor="nw"
    )
quiz_list = [
    "This is a long quiz title. Testing text wrapping aaaaaa a a a a a a a a a"
    " a a a a a a a  a a a a a a a aa a a a a a a a a a a a a a a a a a a a a",
    "Quiz 2", "Caefaefaef", "JJJJJJJJJ",
    "()(*^&^%&%$#%$&^*}::><>?))", "item6", "item7", "item8", "item9",
    "item5", "item6", "item7", "item8", "item9",
    "item5", "item6", "item7", "item8", "item9"
          ]
for item in quiz_list:
    button = tk.Button(
        master=options,
        text=item,
        wraplength=1394,
        justify="left",
        font=("Helvetica", 20),
        bg="lightblue",
        activebackground="#5391b0",
        padx=50,
        width=87,
        command=lambda: show_frame(quiz_frame)
        )
    button.pack(expand="true")
options.update()
canvas_container.configure(
    yscrollcommand=scrollbar.set,
    scrollregion="0 0 0 %s" % options.winfo_height()
    )

canvas_container.grid(row=1, column=0, sticky="ew")
scrollbar.grid(row=1, column=1, sticky="ns")

load_quiz_frame.grid(row=0, column=0)

# Run mainloop
if __name__ == "__main__":
    show_frame(title_frame)
    window.mainloop()
