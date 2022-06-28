# Quiz Maker with simple GUI.

import json
import os
import random
import tkinter as tk
# Import search function from Regular Expressions
from re import search

import style


class quiz_app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Set up the tk window
        self.title("Quiz")
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.state("zoomed")

        # Main container
        container = tk.Frame(self)
        container.configure(bg=style.BACKGROUND_COLOR)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing frames to an array
        self.frames = {}

        for F in (
            title_frame,
            load_quiz_frame,
            create_edit_quiz_frame,
            create_quiz_frame,
            edit_quiz_frame,
            delete_quiz_frame,
            quiz_info_frame,
            quiz_frame,
            finish_frame
        ):
            # Create a frame for each frame in the array and grid it
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(title_frame)

    # Show the frame with the given frame name
    def show_frame(self, frame):
        frame = self.frames[frame]
        frame.tkraise()

    # Puts every file from dependencies//quizzes into global variable quiz_list
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


# ---------- Code for Title Screen ----------
class title_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        welcome = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        heading = tk.Label(
            master=welcome, text="Welcome!", font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
        )
        description = tk.Label(
            master=welcome,
            text="Create your own or load a quiz using the corresponding "
            "buttons below!",
            font=(style.DEFAULT_FONT, 24), bg=style.BACKGROUND_COLOR
            )
        buttons = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        create_button = tk.Button(
            master=buttons, text="Create/Edit Quiz", width=12,
            padx=90, pady=80,
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 40),
            command=lambda: controller.show_frame(create_edit_quiz_frame)
        )
        load_button = tk.Button(
            master=buttons, text="Load Quiz", width=12, padx=90, pady=80,
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 40),
            command=lambda: [
                quiz_app.get_quizzes(), controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, quiz_info_frame, controller
                    )
                ]
            )
        # Pack everything
        welcome.grid(row=0, column=0, sticky="ew", padx=18, pady=100)
        heading.pack()
        description.pack()
        create_button.grid(row=0, column=0, sticky="ew", padx=106, pady=50)
        load_button.grid(row=0, column=1, sticky="ew", padx=106, pady=50)
        buttons.grid(row=1, column=0, sticky="ew")


# ---------- Code for Load Quiz Screen ----------
class load_quiz_frame(tk.Frame):
    global quiz_list
    global questions
    global options
    global answers
    global score

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Heading
        heading = tk.Label(
            self, text="Select a quiz",
            font=(style.DEFAULT_FONT, 32), width=100, bg=style.BACKGROUND_COLOR
            )
        # Back button
        back_button = tk.Button(
            self, text="Back", width=18,
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: [
                controller.show_frame(title_frame),
                self.canvas_container.destroy(),
                self.scrollbar.destroy()
            ]
        )
        # Pack everything
        heading.grid(row=0, column=0, sticky="new", pady=60)
        load_quiz_frame.container = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        load_quiz_frame.container.grid(row=1, column=0, sticky="ns")
        back_button.grid(
            row=2, column=0,
            sticky="ew", padx=200, pady=50
            )

    def quiz_selector(self, frame, controller):
        # Set up canvas and scrollbar for the quiz selector
        self.canvas_container = tk.Canvas(
            self.container, width=900, height=480, bg="#DDDDDD"
            )
        options = tk.Frame(self.canvas_container)
        self.scrollbar = tk.Scrollbar(
            self.container,
            orient="vertical",
            command=self.canvas_container.yview
            )
        self.canvas_container.create_window(
            (0, 0),
            window=options,
            anchor="nw"
            )
        # Getting quiz titles and creating buttons for list
        for item in quiz_app.get_quizzes():
            button_border = tk.Frame(
                options, highlightthickness=1, highlightbackground="black"
                )
            button_no = quiz_list.index(item)
            button = tk.Button(
                master=button_border,
                text=item.replace(".json", "").replace("_", " ").title(),
                width=58, wraplength=900,
                font=(style.DEFAULT_FONT, 20),
                bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
                relief="flat",
                command=lambda button_no=button_no, title=item: [
                        self.load_quiz(
                            self, button_no, controller, randomize=True
                            ),
                        self.canvas_container.destroy(),
                        self.scrollbar.destroy(),
                        self.load_edit_quiz(self, frame, title, controller),
                        controller.show_frame(frame)
                    ]
            )
            button_border.pack(fill="x")
            button.pack(fill="x")

        # Updates the frame
        options.update()
        # Sets up the scrollbar for how many things are in the quiz selector
        self.canvas_container.configure(
            yscrollcommand=self.scrollbar.set,
            scrollregion="0 0 0 %s" % options.winfo_height()
            )
        # Pack canvas and scrollbar to center
        self.canvas_container.pack(side="left")
        self.scrollbar.pack(side="left", fill="y", anchor="e")

    def load_edit_quiz(self, frame, title, controller):
        # Calls different functions depending on which frame the quiz selector
        # buttons go to
        if frame == edit_quiz_frame:
            edit_quiz_frame.edit_quiz(
                edit_quiz_frame, title.replace(".json", ""), controller
                )  # Opens the selected quiz to be edited
        if frame == delete_quiz_frame:
            delete_quiz_frame.quiz_title = title  # Set class variable to title

    def load_quiz(self, quiz_no, controller, randomize=False):
        global questions, options, answers, score
        questions = []
        options = []
        answers = []
        score = 0
        try:
            # Load the selected quiz
            quiz_info = open(
                "dependencies//quizzes//{}".format(quiz_list[quiz_no]),
                "r"
                )
            quiz_info = json.load(quiz_info)
            quiz_info_frame.title_label.configure(
                text=quiz_info["title"].title()
                )
            quiz_info_frame.info_label.configure(
                text="Total {} questions".format(len(quiz_info["questions"]))
                )
            # Puts questions in random order
            if randomize:
                random.shuffle(quiz_info["questions"])
            # For each question shuffle options and append to the lists
            for i in range(len(quiz_info["questions"])):
                answer = (
                    quiz_info["questions"][i]["options"]
                    [quiz_info["questions"][i]["answer"]]
                )
                if randomize:
                    random.shuffle(quiz_info["questions"][i]["options"])
                answer = (
                    quiz_info["questions"][i]["options"].index(answer)
                    )
                questions.append(quiz_info["questions"][i]["question"])
                options.append(quiz_info["questions"][i]["options"])
                answers.append(answer)
        except FileNotFoundError:
            error = tk.Frame(quiz_app, bg=style.BACKGROUND_COLOR)
            error_label = tk.Label(
                master=error, text="Unable to load quiz.\nQuiz not found.",
                font=(style.DEFAULT_FONT, 32), bg=style.BACKGROUND_COLOR
                )
            back_button = tk.Button(
                master=error, text="Back to title screen", width=18,
                bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
                font=(style.DEFAULT_FONT, 40),
                command=lambda: [
                    controller.show_frame(title_frame),
                    error.destroy()
                    ]
                )
            # Pack everything
            error_label.place(relx=0.5, rely=0.4, anchor="center")
            back_button.place(relx=0.5, rely=0.6, anchor="center")
            error.grid(row=0, column=0, sticky="nsew")
        except json.decoder.JSONDecodeError:
            error = tk.Frame(quiz_app, bg=style.BACKGROUND_COLOR)
            error_label = tk.Label(
                master=error,
                text=(
                    "Unable to load quiz.\n"
                    "File is empty or not in JSON format."
                    ),
                font=(style.DEFAULT_FONT, 32), bg=style.BACKGROUND_COLOR
                )
            back_button = tk.Button(
                master=error, text="Back to title screen", width=18,
                bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
                font=(style.DEFAULT_FONT, 40),
                command=lambda: [
                    controller.show_frame(title_frame),
                    error.destroy()
                    ]
                )
            # Pack everything
            error_label.place(relx=0.5, rely=0.4, anchor="center")
            back_button.place(relx=0.5, rely=0.6, anchor="center")
            error.grid(row=0, column=0, sticky="nsew")


# ---------- Code for Quiz Info Screen ----------
class quiz_info_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)

        quiz_info_frame.title_label = tk.Label(
            self, text="title", wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 32), bg=style.BACKGROUND_COLOR
        )
        quiz_info_frame.info_label = tk.Label(
            self, text="info",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 24), bg=style.BACKGROUND_COLOR
        )
        start_button = tk.Button(
            self, text="Start",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.start_quiz(quiz_frame, controller)
        )
        back_button = tk.Button(
            self, text="Back",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: [
                controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, quiz_info_frame, controller)
            ]
        )
        # Pack everything
        spacer1 = tk.Label(self)
        spacer2 = tk.Label(self)
        spacer1.grid(row=0, column=0, sticky="ew", padx=100)
        spacer2.grid(row=0, column=2, sticky="ew", padx=100)
        quiz_info_frame.title_label.grid(row=0, column=1, sticky="ew", pady=60)
        quiz_info_frame.info_label.grid(row=1, column=1, sticky="ew", pady=60)
        start_button.grid(row=2, column=1, sticky="ew")
        back_button.grid(row=3, column=1, sticky="ew", pady=60)


# ---------- Code for Quiz Screen ----------
class quiz_frame(tk.Frame):
    global questions, options, answers, score

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        top_frame = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        options_frame = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        bottom_frame = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        # Widget Setup
        quiz_frame.question_label = tk.Label(
            master=top_frame, text="question", wraplength=1100,
            font=(style.DEFAULT_FONT, 32), bg=style.BACKGROUND_COLOR
        )
        title_button = tk.Button(
            master=top_frame, text="Back to Title",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: controller.show_frame(title_frame)
        )
        finish_button = tk.Button(
            master=top_frame, text="Finish Quiz",
            bd=0, bg="#ff3341", activebackground="#E0000F",
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.finish_quiz(self, controller)
        )
        quiz_frame.option1 = tk.Button(
            master=options_frame, text="option1", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 0)
        )
        quiz_frame.option2 = tk.Button(
            master=options_frame, text="option2", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 1)
        )
        quiz_frame.option3 = tk.Button(
            master=options_frame, text="option3", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 2)
        )
        quiz_frame.option4 = tk.Button(
            master=options_frame, text="option4", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 3)
        )
        quiz_frame.score_label = tk.Label(
            master=bottom_frame, text="Your score: 0",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 28), bg=style.BACKGROUND_COLOR
        )
        quiz_frame.skip_next_button = tk.Button(
            self, text="Skip", font=(style.DEFAULT_FONT, 18), width=10,
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: quiz_frame.next_question(self, controller)
        )
        # Pack everything
        top_frame.columnconfigure([0, 2], weight=1)
        top_frame.columnconfigure(1, weight=30)
        options_frame.columnconfigure([0, 1], weight=1, uniform="options")
        options_frame.rowconfigure([0, 1], weight=1)
        bottom_frame.columnconfigure(0, weight=1)

        title_button.grid(row=0, column=0, sticky="ew", padx=20, pady=80)
        quiz_frame.question_label.grid(row=0, column=1, sticky="ew")
        finish_button.grid(row=0, column=2, sticky="ew", padx=20)
        quiz_frame.option1.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10
            )
        quiz_frame.option2.grid(
            row=0, column=1, sticky="nsew", padx=10, pady=10
            )
        quiz_frame.option3.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10
            )
        quiz_frame.option4.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10
            )
        quiz_frame.score_label.grid(row=0, column=0, sticky="ew", pady=50)
        quiz_frame.skip_next_button.place(x=1350, y=745)
        top_frame.pack(side="top", fill="x", padx=20)
        options_frame.pack(fill="both", expand=True, padx=15)
        bottom_frame.pack(fill="x", padx=20)

    def start_quiz(self, controller):
        controller.show_frame(quiz_frame)
        quiz_frame.question_label.configure(text=questions[0])
        quiz_frame.option1.configure(
            text=options[0][0], bg=style.BLUE_BUTTON, state="normal"
            )
        quiz_frame.option2.configure(
            text=options[0][1], bg=style.BLUE_BUTTON, state="normal"
            )
        quiz_frame.option3.configure(
            text=options[0][2], bg=style.BLUE_BUTTON, state="normal"
            )
        quiz_frame.option4.configure(
            text=options[0][3], bg=style.BLUE_BUTTON, state="normal"
            )
        quiz_frame.skip_next_button.configure(text="Skip")
        quiz_frame.score_label.configure(text="Your Score: {}".format(score))

    def check_answer(self, answer):
        global score
        quiz_frame.option1.configure(state="disabled")
        quiz_frame.option2.configure(state="disabled")
        quiz_frame.option3.configure(state="disabled")
        quiz_frame.option4.configure(state="disabled")
        quiz_frame.skip_next_button.configure(text="Next")
        if answer == answers[0]:
            score += 1
            if answer == 0:
                quiz_frame.option1.configure(bg=style.GREEN_BUTTON)
            elif answer == 1:
                quiz_frame.option2.configure(bg=style.GREEN_BUTTON)
            elif answer == 2:
                quiz_frame.option3.configure(bg=style.GREEN_BUTTON)
            elif answer == 3:
                quiz_frame.option4.configure(bg=style.GREEN_BUTTON)
        else:
            if answer == 0:
                quiz_frame.option1.configure(bg=style.RED_BUTTON)
            elif answer == 1:
                quiz_frame.option2.configure(bg=style.RED_BUTTON)
            elif answer == 2:
                quiz_frame.option3.configure(bg=style.RED_BUTTON)
            elif answer == 3:
                quiz_frame.option4.configure(bg=style.RED_BUTTON)
            if answers[0] == 0:
                quiz_frame.option1.configure(bg=style.GREEN_BUTTON)
            elif answers[0] == 1:
                quiz_frame.option2.configure(bg=style.GREEN_BUTTON)
            elif answers[0] == 2:
                quiz_frame.option3.configure(bg=style.GREEN_BUTTON)
            elif answers[0] == 3:
                quiz_frame.option4.configure(bg=style.GREEN_BUTTON)
        quiz_frame.score_label.configure(text="Your Score: {}".format(score))
        quiz_frame.update(self)

    def next_question(self, controller):
        try:
            questions.pop(0)
            answers.pop(0)
            options.pop(0)
            quiz_frame.question_label.configure(text=questions[0])
            quiz_frame.option1.configure(
                text=options[0][0], bg=style.BLUE_BUTTON, state="normal"
                )
            quiz_frame.option2.configure(
                text=options[0][1], bg=style.BLUE_BUTTON, state="normal"
                )
            quiz_frame.option3.configure(
                text=options[0][2], bg=style.BLUE_BUTTON, state="normal"
                )
            quiz_frame.option4.configure(
                text=options[0][3], bg=style.BLUE_BUTTON, state="normal"
                )
            quiz_frame.skip_next_button.configure(text="Skip")
        except IndexError:
            quiz_frame.finish_quiz(quiz_frame, controller)

    def finish_quiz(self, controller):
        # Show finish frame and shows the score
        controller.show_frame(finish_frame)
        finish_frame.final_score_label.configure(
            text="Your Final Score is: {}\n Well Done :)".format(score)
            )


# ---------- Code for Finish Screen ----------
class finish_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        self.columnconfigure(0, weight=1)

        finish_frame.final_score_label = tk.Label(
            self, text="score", wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 32), bg=style.BACKGROUND_COLOR
        )
        title_button = tk.Button(
            self, text="Back to Title", font=(style.DEFAULT_FONT, 18),
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: controller.show_frame(title_frame)
        )
        # Pack everything
        finish_frame.final_score_label.grid(
            row=0, column=0, sticky="ew", pady=60
            )
        title_button.grid(row=1, column=0, sticky="ew", pady=60, padx=20)


# ---------- Code for Create/Edit Quiz Screen ----------
class create_edit_quiz_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)

        buttons_frame = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        title_button = tk.Button(
            self, text="Back to Title", font=(style.DEFAULT_FONT, 18),
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: controller.show_frame(title_frame)
        )
        create_button = tk.Button(
            master=buttons_frame, text="Create a new quiz!",
            bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
            font=(style.DEFAULT_FONT, 24), width=20,
            command=lambda: [
                controller.show_frame(create_quiz_frame),
                create_quiz_frame.title_entry.delete(0, tk.END),
                create_quiz_frame.rebind_return(controller)
            ]
        )
        edit_button = tk.Button(
            master=buttons_frame, text="Edit an existing quiz!",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 24), width=20,
            command=lambda: [
                controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, edit_quiz_frame, controller
                    )
            ]
        )
        delete_button = tk.Button(
            master=buttons_frame, text="Delete a quiz",
            bd=0, bg=style.RED_BUTTON, activebackground=style.ACTIVE_RED,
            font=(style.DEFAULT_FONT, 24), width=20,
            command=lambda: [
                controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, delete_quiz_frame, controller
                )
            ]
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
class create_quiz_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        self.columnconfigure(
            [0, 1, 2, 3], weight=1, uniform="create_quiz"
            )
        self.rowconfigure([0, 1, 2], weight=1)

        # Tkinter Widgets
        heading_label = tk.Label(
            self, text="Create a new quiz", font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
        )
        instructions_label = tk.Label(
            self, bg=style.BACKGROUND_COLOR,
            text=(
                "Maximum of 30 characters\nThe title cannot be empty\n"
                "Some characters are not allowed due to filename limitations\n"
                "THE TITLE CANNOT BE CHANGED LATER"
                ),
            font=(style.DEFAULT_FONT, 18), justify="center"
        )
        input_title_label = tk.Label(
            self, text="Quiz Title:", font=(style.DEFAULT_FONT, 18),
            bg=style.BACKGROUND_COLOR
        )
        create_quiz_frame.title_entry = tk.Entry(
            self, font=(style.DEFAULT_FONT, 18), state="normal"
        )
        create_quiz_frame.submit_button = tk.Button(
            self, font=(style.DEFAULT_FONT, 18), text="Submit", state="normal",
            bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
            command=lambda: create_quiz_frame.create_quiz(
                create_quiz_frame, controller
                )
        )
        create_quiz_frame.back_button = tk.Button(
            self, text="Back", font=(style.DEFAULT_FONT, 18),
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: controller.show_frame(create_edit_quiz_frame)
        )

        # Pack everything
        heading_label.grid(row=0, column=0, columnspan=4, sticky="ew", pady=20)
        instructions_label.grid(row=1, column=1, columnspan=2, sticky="ew")
        input_title_label.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        create_quiz_frame.title_entry.grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=20, pady=20
            )
        create_quiz_frame.submit_button.grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=20, pady=20
            )
        create_quiz_frame.back_button.grid(
            row=4, column=0, columnspan=4, sticky="ew", padx=50, pady=50
            )

    def create_quiz(self, controller):
        create_quiz_frame.title_entry.unbind("<Return>")
        # Get the title from user from the title entry box
        title = self.title_entry.get().lower().strip().replace(" ", "_")
        # Checks if the title is valid
        invalid_characters = r'\/|\<|\>|\:|\\|\?|\*|\||\"'
        if len(title) > 30 or title == "" or search(invalid_characters, title):
            # Display an indication that the title is invalid
            info_label = tk.Label(
                text="Invalid Quiz Title",
                bg=style.RED_BUTTON, font=(style.DEFAULT_FONT, 18),
                padx=10, pady=10
            )
            info_label.place(relx=0.5, rely=0.5, anchor="center")
            info_label.after(2000, lambda: info_label.destroy())
            self.rebind_return(controller)
            return None
        try:
            # Create new json file with the title
            open(
                "dependencies//quizzes//{title}.json".format(title=title), "x"
            )
            # Open the new json file and write the title to it
            with open(
                "dependencies//quizzes//{title}.json".format(title=title), "w"
            ) as f:
                json.dump({
                    "title": title,
                    "questions": [
                        {
                            "question": "Enter question here",
                            "options": [
                                "Enter option 1 here", "Enter option 2 here",
                                "Enter option 3 here", "Enter option 4 here"
                                ],
                            "answer": 0
                        }
                    ]
                    }, f, indent=4)
            # Show the edit quiz frame
            edit_quiz_frame.edit_quiz(edit_quiz_frame, title, controller)
            controller.show_frame(edit_quiz_frame)
        except FileExistsError:
            # Show error message if file already exists with buttons to
            # overwrite or edit the quiz with the same name
            self.title_entry.configure(state="disabled")
            create_quiz_frame.submit_button.configure(state="disabled")
            create_quiz_frame.back_button.configure(state="disabled")
            self.error_label = tk.Label(
                text="Quiz with this title already exists.",
                font=(style.DEFAULT_FONT, 40), bg=style.RED_BUTTON,
            )
            # Edits the existing quiz without creating new quiz
            self.edit_quiz_button = tk.Button(
                text="Edit the quiz", font=(style.DEFAULT_FONT, 18), width=15,
                bd=0, bg=style.GREEN_BUTTON, padx=10, pady=10,
                command=lambda: [
                    edit_quiz_frame.edit_quiz(
                        edit_quiz_frame, title, controller
                        ),
                    controller.show_frame(edit_quiz_frame),
                    self.destroy_error_label(self)
                ]
            )
            # Delete and create new quiz with same name
            self.overwrite_quiz_button = tk.Button(
                text="Overwrite the quiz", font=(style.DEFAULT_FONT, 18),
                width=15, bd=0, bg=style.RED_BUTTON, padx=10, pady=10,
                command=lambda: [
                    os.remove(
                        "dependencies//quizzes//{title}.json"
                        .format(title=title)
                        ),
                    create_quiz_frame.create_quiz(
                        create_quiz_frame, controller
                        ),
                    self.destroy_error_label(self),
                    edit_quiz_frame.edit_quiz(
                        edit_quiz_frame, title, controller
                        ),
                    controller.show_frame(edit_quiz_frame)
                ]
            )
            # Removes error label and allows user to enter new title
            self.cancel_button = tk.Button(
                text="Cancel", font=(style.DEFAULT_FONT, 18), width=15,
                bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
                padx=10, pady=10,
                command=lambda: [
                    self.destroy_error_label(self),
                    self.rebind_return(controller)
                    ]
            )
            # Pack error label and buttons
            self.error_label.place(relx=0.5, rely=0.5, anchor="center")
            self.edit_quiz_button.place(relx=0.3, rely=0.6, anchor="center")
            self.overwrite_quiz_button.place(
                relx=0.5, rely=0.6, anchor="center"
                )
            self.cancel_button.place(relx=0.7, rely=0.6, anchor="center")

    def destroy_error_label(self):
        self.error_label.destroy()
        self.edit_quiz_button.destroy()
        self.overwrite_quiz_button.destroy()
        self.cancel_button.destroy()
        self.title_entry.configure(state="normal")
        create_quiz_frame.submit_button.configure(state="normal")
        create_quiz_frame.back_button.configure(state="normal")

    def rebind_return(controller):
        create_quiz_frame.title_entry.bind(
            "<Return>", lambda e: create_quiz_frame.create_quiz(
                create_quiz_frame, controller
                )
        )


# ---------- Code for Edit Quiz Screen ----------
class edit_quiz_frame(tk.Frame):
    question_no = 0
    title = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        self.columnconfigure([0, 1, 2, 3], uniform="edit_quiz")
        self.columnconfigure([0, 3], weight=1)
        self.columnconfigure([1, 2], weight=2)
        self.rowconfigure([0, 1, 2, 3, 4], weight=1)
        # Page layout
        text_attributes = {
            "font": f"{style.DEFAULT_FONT} 18",
            "justify": "center"
            }
        self.back_button = tk.Button(
            self, text="Back", font=(style.DEFAULT_FONT, 18),
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: controller.show_frame(create_edit_quiz_frame)
        )
        edit_quiz_frame.question_label = tk.Label(
            self, bg=style.BACKGROUND_COLOR, **text_attributes
        )
        edit_quiz_frame.question_entry = tk.Entry(self, **text_attributes)
        edit_quiz_frame.question_entry.insert(0, "Enter question here")
        edit_quiz_frame.option1_entry = tk.Entry(self, **text_attributes)
        edit_quiz_frame.option1_entry.insert(0, "Enter option 1 here")
        edit_quiz_frame.option2_entry = tk.Entry(self, **text_attributes)
        edit_quiz_frame.option2_entry.insert(0, "Enter option 2 here")
        edit_quiz_frame.option3_entry = tk.Entry(self, **text_attributes)
        edit_quiz_frame.option3_entry.insert(0, "Enter option 3 here")
        edit_quiz_frame.option4_entry = tk.Entry(self, **text_attributes)
        edit_quiz_frame.option4_entry.insert(0, "Enter option 4 here")
        edit_quiz_frame.correct_option_entry = tk.Entry(
            self, **text_attributes
            )
        edit_quiz_frame.correct_option_entry.insert(
            0, "Enter correct option here. 1, 2, 3, 4"
            )
        self.correct_label = tk.Label(
            self, text="Correct option box:\n1, 2, 3 or 4",
            **text_attributes, bg=style.BACKGROUND_COLOR
        )
        self.option1_label = tk.Label(
            self, text="Option 1 box -",
            **text_attributes, bg=style.BACKGROUND_COLOR
        )
        self.option2_label = tk.Label(
            self, text="- Option 2 box",
            **text_attributes, bg=style.BACKGROUND_COLOR
        )
        self.option3_label = tk.Label(
            self, text="Option 3 box -",
            **text_attributes, bg=style.BACKGROUND_COLOR
        )
        self.option4_label = tk.Label(
            self, text="- Option 4 box",
            **text_attributes, bg=style.BACKGROUND_COLOR
        )
        edit_quiz_frame.save_button = tk.Button(
            self, text="Save", **text_attributes,
            bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
            command=lambda: self.submit_question()
        )
        edit_quiz_frame.next_button = tk.Button(
            self, text="Next Question", **text_attributes
        )
        edit_quiz_frame.previous_button = tk.Button(
            self, text="Previous Question", **text_attributes,
            bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: self.show_question(self.question_no-1)
        )
        # Pack everything
        self.back_button.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        edit_quiz_frame.question_entry.grid(
            row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=20
            )
        edit_quiz_frame.question_label.grid(
            row=0, column=3, sticky="ew", padx=20, pady=20
            )
        self.option1_label.grid(row=1, column=0, sticky="ew")
        self.option2_label.grid(row=1, column=3, sticky="ew")
        self.option3_label.grid(row=2, column=0, sticky="ew")
        self.option4_label.grid(row=2, column=3, sticky="ew")
        edit_quiz_frame.option1_entry.grid(
            row=1, column=1, sticky="nsew", padx=3, pady=3
            )
        edit_quiz_frame.option2_entry.grid(
            row=1, column=2, sticky="nsew", padx=3, pady=3
            )
        edit_quiz_frame.option3_entry.grid(
            row=2, column=1, sticky="nsew", padx=3, pady=3
            )
        edit_quiz_frame.option4_entry.grid(
            row=2, column=2, sticky="nsew", padx=3, pady=3
            )
        edit_quiz_frame.correct_option_entry.grid(
            row=3, column=1, columnspan=2, sticky="nsew", padx=3, pady=3
        )
        edit_quiz_frame.save_button.grid(
            row=4, column=1, columnspan=2, sticky="ew"
            )
        self.correct_label.grid(row=3, column=0, sticky="ew", padx=20, pady=20)
        edit_quiz_frame.next_button.grid(
            row=4, column=3, sticky="ew", padx=15, pady=10, ipady=5
            )
        edit_quiz_frame.previous_button.grid(
            row=4, column=0, sticky="ew", padx=15, pady=10, ipady=5
            )

    def edit_quiz(self, title, controller):
        global questions, options, answers
        # Updates the class variables
        self.title = title
        self.question_no = 0
        # Loads selected quiz
        quiz_list = quiz_app.get_quizzes()
        quiz_no = quiz_list.index("{title}.json".format(title=title))
        load_quiz_frame.load_quiz(
            load_quiz_frame,
            quiz_no,
            controller
            )
        self.show_question(self, self.question_no)

    def show_question(self, question_no):
        # Change class variable to the passed in argument question_no
        self.question_no = question_no
        # Show the corresponding question and options
        edit_quiz_frame.question_label.configure(
            text="Question {question_no}".format(question_no=question_no+1)
            )
        edit_quiz_frame.question_entry.delete(0, "end")
        edit_quiz_frame.question_entry.insert(0, questions[question_no])
        edit_quiz_frame.option1_entry.delete(0, "end")
        edit_quiz_frame.option1_entry.insert(0, options[question_no][0])
        edit_quiz_frame.option2_entry.delete(0, "end")
        edit_quiz_frame.option2_entry.insert(0, options[question_no][1])
        edit_quiz_frame.option3_entry.delete(0, "end")
        edit_quiz_frame.option3_entry.insert(0, options[question_no][2])
        edit_quiz_frame.option4_entry.delete(0, "end")
        edit_quiz_frame.option4_entry.insert(0, options[question_no][3])
        edit_quiz_frame.correct_option_entry.delete(0, "end")
        edit_quiz_frame.correct_option_entry.insert(0, answers[question_no]+1)
        # Disable previous and next buttons if at the start or end of the quiz
        if question_no == 0:
            edit_quiz_frame.previous_button.configure(state="disabled")
        else:
            edit_quiz_frame.previous_button.configure(state="normal")
        if question_no == len(questions)-1:
            edit_quiz_frame.next_button.configure(
                text="New Question",
                bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
                command=lambda: [
                    edit_quiz_frame.new_question(self),
                    edit_quiz_frame.show_question(self, self.question_no+1)
                    ]
                )
        else:
            edit_quiz_frame.next_button.configure(
                text="Next Question",
                bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
                command=lambda: (
                    edit_quiz_frame.show_question(self, self.question_no+1)
                    )
            )

    def submit_question(self):
        global questions, options, answers
        # Update the questions, options, and answers lists
        questions[self.question_no] = edit_quiz_frame.question_entry.get()
        options[self.question_no] = [
            edit_quiz_frame.option1_entry.get(),
            edit_quiz_frame.option2_entry.get(),
            edit_quiz_frame.option3_entry.get(),
            edit_quiz_frame.option4_entry.get()
            ]
        answer = edit_quiz_frame.correct_option_entry.get()
        if answer not in ["1", "2", "3", "4"]:
            # Display an indication that the question answer is invalid
            info_label = tk.Label(
                text="Invalid Correct Option. Use 1, 2, 3, or 4",
                bg=style.RED_BUTTON, font=(style.DEFAULT_FONT, 18),
                padx=10, pady=10
            )
            info_label.place(relx=0.5, rely=0.5, anchor="center")
            info_label.after(2000, lambda: info_label.destroy())
            return None
        answers[self.question_no] = int(answer)-1
        # Calls dump_quiz function to update the quiz
        self.dump_quiz(questions, options, answers)
        # Display an indication that the question has been updated
        info_label = tk.Label(
            text="Question updated", bg=style.GREEN_BUTTON,
            font=(style.DEFAULT_FONT, 18),
            padx=10, pady=10
        )
        info_label.place(relx=0.5, rely=0.5, anchor="center")
        info_label.after(1000, lambda: info_label.destroy())

    def new_question(self):
        global questions, options, answers
        # Append a new question to the json file
        questions.append("Enter question here")
        options.append([
            "Enter option 1 here", "Enter option 2 here",
            "Enter option 3 here", "Enter option 4 here"
            ])
        answers.append(0)
        # Dump the new question to the json file
        edit_quiz_frame.dump_quiz(self, questions, options, answers)

    def dump_quiz(self, questions, options, answers):
        # Format data in json format
        data = {
            "title": self.title.replace("_", " "),
            "questions": [],
        }
        for i in range(len(questions)):
            question_dict = {}
            question_dict["question"] = questions[i]
            question_dict["options"] = options[i]
            question_dict["answer"] = answers[i]
            data["questions"].append(question_dict)
        # Dump to json file
        path = "dependencies//quizzes//{title}.json".format(title=self.title)
        with open(path, "w") as f:
            f.seek(0)  # Rewinds file to the start
            json.dump(
                data,
                f,
                ensure_ascii=True,
                indent=4
            )
            f.truncate()  # Deletes extra data


class delete_quiz_frame(tk.Frame):
    quiz_title = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        # Widget Setup
        label = tk.Label(
            self, text="ARE YOU SURE YOU WANT TO DELETE THIS QUIZ?",
            font=(style.DEFAULT_FONT, 22), bg=style.BACKGROUND_COLOR
        )
        yes_button = tk.Button(
            self, text="Yes", font=(style.DEFAULT_FONT, 18), width=15,
            bd=0, bg=style.RED_BUTTON, activebackground=style.ACTIVE_RED,
            command=lambda: [
                os.remove(
                    "dependencies//quizzes//{title}"
                    .format(title=self.quiz_title)
                ),
                controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, delete_quiz_frame, controller
                ),
                self.deleted_message()
            ]
        )
        no_button = tk.Button(
            self, text="Cancel", font=(style.DEFAULT_FONT, 18), width=15,
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            command=lambda: [
                controller.show_frame(load_quiz_frame),
                load_quiz_frame.quiz_selector(
                    load_quiz_frame, delete_quiz_frame, controller
                )
            ]
        )
        # Pack everything
        label.pack(fill="x", pady=150)
        yes_button.pack(pady=20)
        no_button.pack()

    def deleted_message(self):
        # Deleted message (Message to user that the quiz has been deleted)
        self.deleted_label = tk.Label(
            text="Quiz successfully deleted", font=(style.DEFAULT_FONT, 20),
            bg=style.GREEN_BUTTON
        )
        self.deleted_label.place(relx=0.5, rely=0.5, anchor="center"),
        self.deleted_label.after(
            2000, lambda: self.deleted_label.destroy()
            )


# Run mainloop
if __name__ == "__main__":
    app = quiz_app()
    app.mainloop()
