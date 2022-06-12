import tkinter as tk
import os
import json
import random
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
            # edit_quiz_frame,
            # delete_quiz_frame,
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
        buttons = tk.Frame(self, bg=style.BACKGROUND_COLOR)
        create_button = tk.Button(
            master=buttons,
            text="Create/Edit Quiz",
            width=12,
            padx=90,
            pady=80,
            bd=0, bg=style.BLUE_BUTTON,
            activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 40),
            command=lambda: controller.show_frame(create_edit_quiz_frame)
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
            command=lambda: [
                quiz_app.get_quizzes(), controller.show_frame(load_quiz_frame)
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
        # Heading text
        heading = tk.Label(
            self,
            text="Choose a quiz!",
            font=(style.DEFAULT_FONT, 32),
            width=100,
            bg=style.BACKGROUND_COLOR
            )
        # Quiz Selector
        self.columnconfigure([0, 3], weight=5)
        self.columnconfigure(1, weight=100)
        self.columnconfigure(2, weight=1)
        canvas_container = tk.Canvas(
            self, width=900, height=480, bg="#DDDDDD"
            )
        options = tk.Frame(canvas_container)
        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=canvas_container.yview
            )
        canvas_container.create_window(
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
                width=58,
                wraplength=900,
                font=(style.DEFAULT_FONT, 20),
                bd=0, bg=style.BLUE_BUTTON,
                activebackground=style.ACTIVE_BLUE,
                relief="flat",
                command=lambda button_no=button_no: [
                        self.load_quiz(button_no, controller),
                        controller.show_frame(quiz_info_frame)
                    ]
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
            self,
            text="Back",
            width=18,
            bd=0, bg=style.BLUE_BUTTON,
            activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: controller.show_frame(title_frame)
        )
        # Pack everything
        spacer1 = tk.Label(self)
        spacer2 = tk.Label(self)
        spacer1.grid(row=0, column=0, sticky="ew", padx=180)
        spacer2.grid(row=0, column=3, sticky="ew", padx=180)
        heading.grid(row=0, column=1, columnspan=2, sticky="ew", pady=60)
        canvas_container.grid(row=1, column=1, sticky="ew")
        scrollbar.grid(row=1, column=2, sticky="ns")
        back_button.grid(
            row=2, column=1, columnspan=2,
            sticky="ew", padx=200, pady=50
            )

    def load_quiz(self, quiz_no, controller):
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
            quiz_info_frame.title_label.configure(text=quiz_info["title"])
            quiz_info_frame.info_label.configure(
                text="Total {} questions".format(len(quiz_info["questions"]))
                )
            # Puts questions in random order
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
        except FileNotFoundError:
            error = tk.Frame(quiz_app, bg=style.BACKGROUND_COLOR)
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
            self,
            text="title",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
        )
        quiz_info_frame.info_label = tk.Label(
            self,
            text="info",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 24),
            bg=style.BACKGROUND_COLOR
        )
        start_button = tk.Button(
            self,
            text="Start",
            bd=0,
            bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.start_quiz(quiz_frame, controller)
        )
        back_button = tk.Button(
            self,
            text="Back",
            bd=0,
            bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: controller.show_frame(load_quiz_frame)
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
        quiz_frame.question_label = tk.Label(
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
            command=lambda: controller.show_frame(title_frame)
        )
        finish_button = tk.Button(
            master=top_frame,
            text="Finish Quiz",
            bd=0, bg="#ff3341", activebackground="#E0000F",
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.finish_quiz(self, controller)
        )
        quiz_frame.option1 = tk.Button(
            master=options_frame,
            text="option1", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 0)
        )
        quiz_frame.option2 = tk.Button(
            master=options_frame,
            text="option2", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 1)
        )
        quiz_frame.option3 = tk.Button(
            master=options_frame,
            text="option3", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 2)
        )
        quiz_frame.option4 = tk.Button(
            master=options_frame,
            text="option4", anchor="center",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: quiz_frame.check_answer(self, 3)
        )
        quiz_frame.score_label = tk.Label(
            master=bottom_frame,
            text="Your score: 0",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 28),
            bg=style.BACKGROUND_COLOR
        )
        quiz_frame.skip_next_button = tk.Button(
            self,
            text="Skip",
            font=(style.DEFAULT_FONT, 18),
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            width=10,
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
            text="Your Final Score is: {}!".format(score)
            )


# ---------- Code for Finish Screen ----------
class finish_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=style.BACKGROUND_COLOR)
        self.columnconfigure(0, weight=1)

        finish_frame.final_score_label = tk.Label(
            self,
            text="score",
            wraplength=1100, width=45,
            font=(style.DEFAULT_FONT, 32),
            bg=style.BACKGROUND_COLOR
        )
        title_button = tk.Button(
            self,
            text="Back to Title",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
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
            self,
            text="Back to Title",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: controller.show_frame(title_frame)
        )
        create_button = tk.Button(
            master=buttons_frame,
            text="Create a new quiz!",
            bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
            font=(style.DEFAULT_FONT, 24),
            width=20,
            command=lambda: controller.show_frame(create_quiz_frame)
        )
        edit_button = tk.Button(
            master=buttons_frame,
            text="Edit an existing quiz!",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 24),
            width=20,
            command=lambda: controller.show_frame(edit_quiz_frame)
        )
        delete_button = tk.Button(
            master=buttons_frame,
            text="Delete a quiz",
            bd=0, bg=style.RED_BUTTON, activebackground=style.ACTIVE_RED,
            font=(style.DEFAULT_FONT, 24),
            width=20,
            command=lambda: controller.show_frame(delete_quiz_frame)
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
        self.rowconfigure(0, weight=1)

        input_title_label = tk.Label(
            self,
            text="Quiz Title:",
            font=(style.DEFAULT_FONT, 18),
            bg=style.BACKGROUND_COLOR
        )
        self.title_entry = tk.Entry(
            self,
            font=(style.DEFAULT_FONT, 18),
            state="normal"
        )
        self.submit_button = tk.Button(
            self,
            font=(style.DEFAULT_FONT, 18),
            text="Submit",
            bd=0, bg=style.GREEN_BUTTON, activebackground=style.ACTIVE_GREEN,
            state="normal",
            command=lambda: self.create_quiz()
        )
        back_button = tk.Button(
            self,
            text="Back",
            bd=0, bg=style.BLUE_BUTTON, activebackground=style.ACTIVE_BLUE,
            font=(style.DEFAULT_FONT, 18),
            command=lambda: [
                controller.show_frame(create_edit_quiz_frame),
                self.title_entry.delete(0, "end")
                ]
        )

        # Pack everything
        input_title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.title_entry.grid(
            row=0, column=1, columnspan=2, sticky="ew", padx=20, pady=20
            )
        self.submit_button.grid(
            row=1, column=1, columnspan=2, sticky="ew", padx=20, pady=20
            )
        back_button.grid(
            row=2, column=0, columnspan=4, sticky="ew", padx=50, pady=50
            )

    def create_quiz(self):
        # Get the title from user from the title entry box
        title = self.title_entry.get().lower().replace(" ", "_")
        try:
            # Create new json file with the title
            open(
                "dependencies//quizzes//{title}.json".format(title=title), "x"
            )
        except FileExistsError:
            # Show error message if file already exists with buttons to
            # overwrite or edit the quiz with the same name
            self.title_entry.configure(state="disabled")
            self.submit_button.configure(state="disabled")
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
                        "dependencie//quizzes//{title}.json"
                        .format(title=title)
                        ),
                    open(
                        "dependencies//quizzes//{title}.json"
                        .format(title=title),
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
                    self.title_entry.configure(state="normal"),
                    self.submit_button.configure(state="normal")
                ]
            )
            # Pack error label and buttons
            error_label.place(relx=0.5, rely=0.5, anchor="center")
            edit_quiz_button.place(relx=0.3, rely=0.6, anchor="center")
            overwrite_quiz_button.place(relx=0.5, rely=0.6, anchor="center")
            cancel_button.place(relx=0.7, rely=0.6, anchor="center")


# Run mainloop
if __name__ == "__main__":
    app = quiz_app()
    app.mainloop()
