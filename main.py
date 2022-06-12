import tkinter as tk
import os
import json
import random
import style


def show_frame(frame):
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()


def get_quizzes():
    global quiz_list
    try:
        quiz_info = os.listdir("dependencies//quizzes")
        quiz_list = []
        for i in range(len(quiz_info)):
            quiz_list.append(quiz_info[i])
        quiz_list.sort()
        return quiz_list
    except FileNotFoundError:
        print("File not found")
        quiz_list = []
        return quiz_list
    except json.decoder.JSONDecodeError:
        print("File is not in JSON format")
        quiz_list = []
        return quiz_list


def load_quiz(quiz_no):
    global quiz_list
    global questions
    global options
    global answers
    global score
    questions = []
    options = []
    answers = []
    score = 0
    print(quiz_no)
    print(quiz_list)
    try:
        # Load the selected quiz
        quiz_info = open(
            "dependencies//quizzes//{}".format(quiz_list[quiz_no]),
            "r"
            )
        quiz_info = json.load(quiz_info)

        # Loads quiz info
        title_label.configure(text=quiz_info["title"])
        info_label.configure(
            text="{} questions".format(len(quiz_info["questions"]))
        )
        # questions in random order
        random.shuffle(quiz_info["questions"])
        # For each question shuffle options and append to the lists
        for i in range(len(quiz_info["questions"])):
            answer = (
                quiz_info["questions"][i]["options"]
                [quiz_info["questions"][i]["answer"]]
            )
            random.shuffle(quiz_info["questions"][i]["options"])
            answer = (
                quiz_info["questions"][i]["options"].index(answer)
                )
            questions.append(quiz_info["questions"][i]["question"])
            options.append(quiz_info["questions"][i]["options"])
            answers.append(answer)
        show_frame(quiz_info_frame)
    except FileNotFoundError:
        error = tk.Frame(window, bg=style.BACKGROUND_COLOR)
        error_label = tk.Label(
            master=error,
            text="Unable to load quiz.\nQuiz not found.",
            font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
            )
        back_button = tk.Button(
            master=error,
            text="Back to title screen",
            width=18,
            bd=0, bg=style.BLUE_BUTTON,
            activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 40),
            command=lambda: [show_frame(title_frame), error.destroy()]
            )
        # Pack everything
        error_label.place(relx=0.5, rely=0.5, anchor="center")
        back_button.place(relx=0.5, rely=0.7, anchor="center")
        error.grid(row=0, column=0, sticky="nsew")
    except json.decoder.JSONDecodeError:
        error = tk.Frame(window, bg=style.BACKGROUND_COLOR)
        error_label = tk.Label(
            master=error,
            text="Unable to load quiz.\nFile is empty or not in JSON format.",
            font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
            )
        back_button = tk.Button(
            master=error,
            text="Back to title screen",
            width=18,
            bd=0, bg=style.BLUE_BUTTON,
            activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 40),
            command=lambda: [show_frame(title_frame), error.destroy()]
            )
        # Pack everything
        error_label.place(relx=0.5, rely=0.4, anchor="center")
        back_button.place(relx=0.5, rely=0.6, anchor="center")
        error.grid(row=0, column=0, sticky="nsew")


def check_answer(answer):
    global score
    option1.configure(state="disabled")
    option2.configure(state="disabled")
    option3.configure(state="disabled")
    option4.configure(state="disabled")
    skip_next_button.configure(text="Next")
    if answer == answers[0]:
        score += 1
        if answer == 0:
            option1.configure(bg=style.GREEN_BUTTON)
        elif answer == 1:
            option2.configure(bg=style.GREEN_BUTTON)
        elif answer == 2:
            option3.configure(bg=style.GREEN_BUTTON)
        elif answer == 3:
            option4.configure(bg=style.GREEN_BUTTON)
    else:
        if answer == 0:
            option1.configure(bg=style.RED_BUTTON)
        elif answer == 1:
            option2.configure(bg=style.RED_BUTTON)
        elif answer == 2:
            option3.configure(bg=style.RED_BUTTON)
        elif answer == 3:
            option4.configure(bg=style.RED_BUTTON)
        if answers[0] == 0:
            option1.configure(bg=style.GREEN_BUTTON)
        elif answers[0] == 1:
            option2.configure(bg=style.GREEN_BUTTON)
        elif answers[0] == 2:
            option3.configure(bg=style.GREEN_BUTTON)
        elif answers[0] == 3:
            option4.configure(bg=style.GREEN_BUTTON)
    score_label.configure(text="Your Score: {}".format(score))
    quiz_frame.update()


def start_quiz():
    show_frame(quiz_frame)
    question_label.configure(text=questions[0])
    option3.configure(
        text=options[0][2], bg=style.BLUE_BUTTON, state="normal"
        )
    option1.configure(
        text=options[0][0], bg=style.BLUE_BUTTON, state="normal"
        )
    option2.configure(
        text=options[0][1], bg=style.BLUE_BUTTON, state="normal"
        )
    option4.configure(
        text=options[0][3], bg=style.BLUE_BUTTON, state="normal"
        )
    skip_next_button.configure(text="Skip")
    score_label.configure(text="Your Score: {}".format(score))


def next_question():
    try:
        questions.pop(0)
        answers.pop(0)
        options.pop(0)
        question_label.configure(text=questions[0])
        option1.configure(
            text=options[0][0], bg=style.BLUE_BUTTON, state="normal"
            )
        option2.configure(
            text=options[0][1], bg=style.BLUE_BUTTON, state="normal"
            )
        option3.configure(
            text=options[0][2], bg=style.BLUE_BUTTON, state="normal"
            )
        option4.configure(
            text=options[0][3], bg=style.BLUE_BUTTON, state="normal"
            )
        skip_next_button.configure(text="Skip")
    except IndexError:
        finish_quiz()


def finish_quiz():
    # Show finish frame and shows the score
    show_frame(finish_frame)
    final_score_label.configure(text="Your Final Score is: {}!".format(score))


def create_quiz():
    # Get the title from user from the title entry box
    title = title_entry.get().lower().replace(" ", "_")
    print(title)
    try:
        # Create new json file with the title
        open(
            "dependencies//quizzes//{title}.json".format(title=title), "x"
        )
    except FileExistsError:
        # Show error message if file already exists with buttons to overwrite
        # or edit the quiz with the same name
        title_entry.configure(state="disabled")
        submit_button.configure(state="disabled")
        error_label = tk.Label(
            text="Quiz with this title already exists.",
            font=(style.DEFAULT_FONT, 40),
            bg=style.RED_BUTTON,
        )
        # Edits the existing quiz without creating new quiz
        edit_quiz_button = tk.Button(
            text="Edit the quiz",
            font=(style.DEFAULT_FONT, 18),
            width=15,
            bd=0, bg=style.GREEN_BUTTON,
            padx=10, pady=10,
            command=lambda: edit_quiz(title)
        )
        # Delete and create new quiz with same name
        overwrite_quiz_button = tk.Button(
            text="Overwrite the quiz",
            font=(style.DEFAULT_FONT, 18),
            width=15,
            bd=0, bg=style.RED_BUTTON,
            padx=10, pady=10,
            command=lambda: [
                os.remove(
                    "dependencie//quizzes//{title}.json".format(title=title)
                    ),
                open(
                    "dependencies//quizzes//{title}.json".format(title=title),
                    "x"
                    ),
                edit_quiz(title)
            ]
        )
        # Removes error label and allows user to enter new title
        cancel_button = tk.Button(
            text="Cancel",
            font=(style.DEFAULT_FONT, 18),
            width=15,
            bd=0, bg=style.BLUE_BUTTON,
            padx=10, pady=10,
            command=lambda: [
                error_label.destroy(),
                edit_quiz_button.destroy(),
                overwrite_quiz_button.destroy(),
                cancel_button.destroy(),
                title_entry.configure(state="normal"),
                submit_button.configure(state="normal")
            ]
        )
        # Pack error label and buttons
        error_label.place(relx=0.5, rely=0.5, anchor="center")
        edit_quiz_button.place(relx=0.3, rely=0.6, anchor="center")
        overwrite_quiz_button.place(relx=0.5, rely=0.6, anchor="center")
        cancel_button.place(relx=0.7, rely=0.6, anchor="center")


# Set up the main window
window = tk.Tk()
window.title("Quiz")
window.resizable(False, False)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state("zoomed")

# Set up different frames
title_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
load_quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
create_edit_quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
create_quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
edit_quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
delete_quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
quiz_info_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
quiz_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
finish_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)

# ---------- Code for Title Screen ----------
welcome = tk.Frame(title_frame, bg=style.BACKGROUND_COLOR)
heading = tk.Label(
    master=welcome,
    text="Welcome!",
    font=(style.DEFAULT_FONT, 32),
    bg=style.BACKGROUND_COLOR
)
description = tk.Label(
    master=welcome,
    text="Create your own or load a quiz using the corresponding "
    "buttons below!",
    font=(style.DEFAULT_FONT, 24),
    bg=style.BACKGROUND_COLOR
    )
buttons = tk.Frame(title_frame, bg=style.BACKGROUND_COLOR)
create_button = tk.Button(
    master=buttons,
    text="Create/Edit Quiz",
    width=12,
    padx=90,
    pady=80,
    bd=0, bg=style.BLUE_BUTTON,
    activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 40),
    command=lambda: show_frame(create_edit_quiz_frame)
)
load_button = tk.Button(
    master=buttons,
    text="Load Quiz",
    width=12,
    padx=90,
    pady=80,
    bd=0,
    bg=style.BLUE_BUTTON,
    activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 40),
    command=lambda: show_frame(load_quiz_frame)
    )
# Pack everything
welcome.grid(row=0, column=0, sticky="ew", padx=18, pady=100)
heading.pack()
description.pack()
create_button.grid(row=0, column=0, sticky="ew", padx=106, pady=50)
load_button.grid(row=0, column=1, sticky="ew", padx=106, pady=50)
buttons.grid(row=1, column=0, sticky="ew")

# ---------- Code for Load Quiz Screen ----------
quiz_titles = get_quizzes()
quiz_no = []
# Heading text
heading = tk.Label(
    master=load_quiz_frame,
    text="Choose a quiz!",
    font=(style.DEFAULT_FONT, 32),
    width=100,
    bg=style.BACKGROUND_COLOR
    )
# Quiz Selector
load_quiz_frame.columnconfigure([0, 3], weight=5)
load_quiz_frame.columnconfigure(1, weight=100)
load_quiz_frame.columnconfigure(2, weight=1)
canvas_container = tk.Canvas(
    load_quiz_frame, width=900, height=480, bg="#DDDDDD"
    )
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
# Getting quiz titles and creating buttons for list
for item in quiz_titles:
    button_border = tk.Frame(
        options, highlightthickness=1, highlightbackground="black"
        )
    button_no = quiz_titles.index(item)
    button = tk.Button(
        master=button_border,
        text=item.replace(".json", "").replace("_", " ").title(),
        width=58,
        wraplength=900,
        font=(style.DEFAULT_FONT, 20),
        bd=0, bg=style.BLUE_BUTTON,
        activebackground=style.ACTIVE_BLUE,
        relief="flat",
        command=lambda button_no=button_no: load_quiz(button_no)
    )
    button_border.pack(fill="x")
    button.pack(fill="x")

options.update()
canvas_container.configure(
    yscrollcommand=scrollbar.set,
    scrollregion="0 0 0 %s" % options.winfo_height()
    )
# Back button
back_button = tk.Button(
    master=load_quiz_frame,
    text="Back",
    width=18,
    bd=0, bg=style.BLUE_BUTTON,
    activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(title_frame)
)
# Pack everything
spacer1 = tk.Label(load_quiz_frame)
spacer2 = tk.Label(load_quiz_frame)
spacer1.grid(row=0, column=0, sticky="ew", padx=180)
spacer2.grid(row=0, column=3, sticky="ew", padx=180)
heading.grid(row=0, column=1, columnspan=2, sticky="ew", pady=60)
canvas_container.grid(row=1, column=1, sticky="ew")
scrollbar.grid(row=1, column=2, sticky="ns")
back_button.grid(
    row=2, column=1, columnspan=2,
    sticky="ew", padx=200, pady=50
    )
load_quiz_frame.grid(row=0, column=0)

# ---------- Code for Quiz Info Screen ----------
title_label = tk.Label(
    master=quiz_info_frame,
    text="title",
    wraplength=1100, width=45,
    font=(style.DEFAULT_FONT, 32),
    bg=style.BACKGROUND_COLOR
)
info_label = tk.Label(
    master=quiz_info_frame,
    text="info",
    wraplength=1100, width=45,
    font=(style.DEFAULT_FONT, 24),
    bg=style.BACKGROUND_COLOR
)
start_button = tk.Button(
    master=quiz_info_frame,
    text="Start",
    bd=0,
    bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: start_quiz()
)
back_button = tk.Button(
    master=quiz_info_frame,
    text="Back",
    bd=0,
    bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(load_quiz_frame)
)
# Pack everything
spacer1 = tk.Label(quiz_info_frame)
spacer2 = tk.Label(quiz_info_frame)
spacer1.grid(row=0, column=0, sticky="ew", padx=100)
spacer2.grid(row=0, column=2, sticky="ew", padx=100)
title_label.grid(row=0, column=1, sticky="ew", pady=60)
info_label.grid(row=1, column=1, sticky="ew", pady=60)
start_button.grid(row=2, column=1, sticky="ew")
back_button.grid(row=3, column=1, sticky="ew", pady=60)

# ---------- Code for Quiz Screen ----------
top_frame = tk.Frame(quiz_frame, bg=style.BACKGROUND_COLOR)
options_frame = tk.Frame(quiz_frame, bg=style.BACKGROUND_COLOR)
bottom_frame = tk.Frame(quiz_frame, bg=style.BACKGROUND_COLOR)
question_label = tk.Label(
    master=top_frame,
    text="question",
    wraplength=1100,
    font=(style.DEFAULT_FONT, 32),
    bg=style.BACKGROUND_COLOR
)
title_button = tk.Button(
    master=top_frame,
    text="Back to Title",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(title_frame)
)
finish_button = tk.Button(
    master=top_frame,
    text="Finish Quiz",
    bd=0, bg="#ff3341", activebackground="#E0000F",
    font=(style.DEFAULT_FONT, 18),
    command=lambda: finish_quiz()
)
option1 = tk.Button(
    master=options_frame,
    text="option1", anchor="center",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: check_answer(0)
)
option2 = tk.Button(
    master=options_frame,
    text="option2", anchor="center",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: check_answer(1)
)
option3 = tk.Button(
    master=options_frame,
    text="option3", anchor="center",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: check_answer(2)
)
option4 = tk.Button(
    master=options_frame,
    text="option4", anchor="center",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: check_answer(3)
)
score_label = tk.Label(
    master=bottom_frame,
    text="Your score: 0",
    wraplength=1100, width=45,
    font=(style.DEFAULT_FONT, 28),
    bg=style.BACKGROUND_COLOR
)
skip_next_button = tk.Button(
    master=quiz_frame,
    text="Skip",
    font=(style.DEFAULT_FONT, 18),
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    width=10,
    command=lambda: next_question()
)

# Pack everything
top_frame.columnconfigure([0, 2], weight=1)
top_frame.columnconfigure(1, weight=30)
options_frame.columnconfigure([0, 1], weight=1, uniform="options")
options_frame.rowconfigure([0, 1], weight=1)
bottom_frame.columnconfigure(0, weight=1)

title_button.grid(row=0, column=0, sticky="ew", padx=20, pady=80)
question_label.grid(row=0, column=1, sticky="ew")
finish_button.grid(row=0, column=2, sticky="ew", padx=20)
option1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
option2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
option3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
option4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
score_label.grid(row=0, column=0, sticky="ew", pady=50)
skip_next_button.place(x=1350, y=745)
top_frame.pack(side="top", fill="x", padx=20)
options_frame.pack(fill="both", expand=True, padx=15)
bottom_frame.pack(fill="x", padx=20)

# ---------- Code for Finish Screen ----------
finish_frame.columnconfigure(0, weight=1)
final_score_label = tk.Label(
    master=finish_frame,
    text="score",
    wraplength=1100, width=45,
    font=(style.DEFAULT_FONT, 32),
    bg=style.BACKGROUND_COLOR
)
title_button = tk.Button(
    master=finish_frame,
    text="Back to Title",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(title_frame)
)
# Pack everything
final_score_label.grid(row=0, column=0, sticky="ew", pady=60)
title_button.grid(row=1, column=0, sticky="ew", pady=60, padx=20)

# ---------- Code for Create/Edit Quiz Screen ----------
buttons_frame = tk.Frame(create_edit_quiz_frame, bg=style.BACKGROUND_COLOR)
title_button = tk.Button(
    master=create_edit_quiz_frame,
    text="Back to Title",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(title_frame)
)
create_button = tk.Button(
    master=buttons_frame,
    text="Create a new quiz!",
    bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
    font=(style.DEFAULT_FONT, 24),
    width=20,
    command=lambda: [
        show_frame(create_quiz_frame),
        title_entry.config(state="normal"),
        title_entry.delete(0, "end"),
        submit_button.config(state="normal")
        ]
)
edit_button = tk.Button(
    master=buttons_frame,
    text="Edit an existing quiz!",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 24),
    width=20,
    command=lambda: show_frame(edit_quiz_frame)
)
delete_button = tk.Button(
    master=buttons_frame,
    text="Delete a quiz",
    bd=0, bg=style.RED_BUTTON, activebackground=style.ACTIVE_RED,
    font=(style.DEFAULT_FONT, 24),
    width=20,
    command=lambda: show_frame(delete_quiz_frame)
)
# Pack everything
buttons_frame.columnconfigure([0, 1, 2], weight=1)
buttons_frame.rowconfigure(0, weight=1)

create_button.grid(row=0, column=0, sticky="nsew", padx=30, pady=200)
edit_button.grid(row=0, column=1, sticky="nsew", padx=30, pady=200)
delete_button.grid(row=0, column=2, sticky="nsew", padx=30, pady=200)
buttons_frame.pack(fill="both", expand="TRUE", padx=20)
title_button.pack(side="bottom", fill="x", padx=50, pady=50)

# ---------- Code for Create Quiz Screen ----------
create_quiz_frame.columnconfigure(
    [0, 1, 2, 3], weight=1, uniform="create_quiz"
    )
create_quiz_frame.rowconfigure(0, weight=1)
input_title_label = tk.Label(
    master=create_quiz_frame,
    text="Quiz Title:",
    font=(style.DEFAULT_FONT, 18),
    bg=style.BACKGROUND_COLOR
)
title_entry = tk.Entry(
    master=create_quiz_frame,
    font=(style.DEFAULT_FONT, 18)
)
submit_button = tk.Button(
    master=create_quiz_frame,
    font=(style.DEFAULT_FONT, 18),
    text="Submit",
    bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
    command=lambda: create_quiz()
)
back_button = tk.Button(
    master=create_quiz_frame,
    text="Back",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(create_edit_quiz_frame)
)

# Pack everything
input_title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
title_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=20, pady=20)
submit_button.grid(
    row=1, column=1, columnspan=2, sticky="ew", padx=20, pady=20
    )
back_button.grid(row=2, column=0, columnspan=4, sticky="ew", padx=50, pady=50)

# ---------- Code for Unavailable Feature Screen ----------
unavailable_frame = tk.Frame(window, bg=style.BACKGROUND_COLOR)
unavailable_frame.columnconfigure(0, weight=1)
unavailable_label = tk.Label(
    master=unavailable_frame,
    text="Sorry this feature is unavailable right now. Look out for updates!",
    wraplength=1100, width=45,
    font=(style.DEFAULT_FONT, 32),
    bg=style.BACKGROUND_COLOR
)
title_button = tk.Button(
    master=unavailable_frame,
    text="Back to Title",
    bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
    font=(style.DEFAULT_FONT, 18),
    command=lambda: show_frame(title_frame)
)
# Pack everything=
unavailable_label.grid(row=0, column=0, sticky="ew", pady=60)
title_button.grid(row=1, column=0, sticky="ew", pady=60, padx=20)

# Run mainloop
if __name__ == "__main__":
    show_frame(title_frame)
    window.mainloop()
