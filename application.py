import tkinter as tk
from string import punctuation
from random import shuffle, randint
from questions import biology_questions
LARGE_FONT = ("Verdana", 12)

answer_list = {
    "correct":
        [],
    "incorrect":
        []
    }

class ApplicationFramework(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (OpeningPage, QuestionPage, FinalPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("OpeningPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    @staticmethod
    def name_validate_command(new_text):
        # validation command for the name entry
        for letter in new_text:
            if letter.isdigit() or letter in punctuation:
                return False
        if len(new_text) > 20:
            return False
        return not new_text.isdigit()

class OpeningPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        opening_title = tk.Label(self, text="Biology Quiz", font=LARGE_FONT)
        opening_title.pack(pady=10, padx=10)
        opening_subtitle = tk.Label(self, text="Hi, welcome to the biology quiz application.")
        opening_subtitle.pack()
        name_validation_command = self.register(ApplicationFramework.name_validate_command)
        name_label = tk.Label(self, text="Please enter your name:")
        name_input = tk.Entry(self, validate='all', validatecommand=(name_validation_command, '%P'), font=("Calibri", 11))
        name_label.pack()
        name_input.pack()
        next_button = tk.Button(self, text="Next", command=lambda: controller.show_frame("QuestionPage"))
        next_button.pack()

class QuestionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        question_frame = tk.Frame(self, relief="sunken", bg="black")
        question_frame.pack(fill="both", padx=10, pady=5)
        test_question = tk.Label(question_frame, text="Question frame")
        test_question.grid(row=0, column=1)
        answer_frame = tk.Frame(self, relief="sunken", bg="red")
        answer_frame.pack(fill="both", padx=10, pady=5)
        test_answer = tk.Label(answer_frame, text="Answer frame")
        test_answer.grid(row=0, column=1)
        self.question_label_array = []
        self.answers_array = []
        self.used_questions = []
        self.order_of_questions = list(range(7))
        shuffle(self.order_of_questions)
        self.question_iterator = 1
        self.correct_answers = tk.IntVar(value=0)
        self.incorrect_answers = tk.IntVar(value=0)
        for F, i in zip((biology_questions), (range(len(biology_questions)))):
            question_label = tk.Label(question_frame, text=biology_questions[F]["question"])
            self.question_label_array.append(question_label)
            self.question_label_array[i].grid(row=0, column=0, sticky="nsew")
            answer_a = tk.Button(answer_frame, text=biology_questions[F]["answers"]["a"], command=lambda i=i: self.check_answer(i, "a"))
            answer_b = tk.Button(answer_frame, text=biology_questions[F]["answers"]["b"], command=lambda i=i: self.check_answer(i, "b"))
            answer_c = tk.Button(answer_frame, text=biology_questions[F]["answers"]["c"], command=lambda i=i: self.check_answer(i, "c"))
            answer_d = tk.Button(answer_frame, text=biology_questions[F]["answers"]["d"], command=lambda i=i: self.check_answer(i, "d"))
            self.answers_array.append([answer_a, answer_b, answer_c, answer_d])
            for j in range(0, 4): self.answers_array[i][j].grid(row=0,column=j, sticky="nsew")
        self.next_button = tk.Button(answer_frame, text="Next", command=lambda: self.iterate_question(), state="disabled")
        self.next_button.grid()
        self.initialize_quiz()        

    def initialize_quiz(self):
        first_question = self.order_of_questions[0]
        self.question_label_array[first_question].tkraise()
        for i in range(0, 4): self.answers_array[first_question][i].tkraise()
        
    def iterate_question(self):
        print(sum(answer_list["correct"]))
        try:
            next_question = self.order_of_questions[self.question_iterator]
        except IndexError:
            self.correct_answers.set(sum(answer_list["correct"]))
            self.incorrect_answers.set(sum(answer_list["incorrect"]))
            self.controller.frames[FinalPage.__name__].output()
            return self.controller.show_frame("FinalPage")
        self.question_label_array[next_question].tkraise()
        for i in range(0,4): self.answers_array[next_question][i].tkraise()
        self.question_iterator += 1
        self.next_button['state'] = "disabled"
        

    def check_answer(self, question_number, answer_value):
        if biology_questions[question_number]["correct_answer"] == answer_value:
            print("you are correct")
            answer_list["correct"].append(1)
        else:
            print("try again")
            answer_list["incorrect"].append(1)
        current_question = self.order_of_questions[self.question_iterator - 1]
        self.question_label_array[current_question].tkraise()
        for i in range(0,4): self.answers_array[current_question][i]['state'] = "disabled"
        self.next_button['state'] = "normal"

class FinalPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.final_output = tk.StringVar()
            final_score = tk.Label(self, textvariable=self.final_output)
            final_score.grid()

        def output(self):
            self.final_output.set("Congratulations, you got " + str(self.controller.frames[QuestionPage.__name__].correct_answers.get()) + " correct and " + str(self.controller.frames[QuestionPage.__name__].incorrect_answers.get()) + " incorrect.")


app = ApplicationFramework()
app.geometry("800x600")
# Center application to center of screen | Source: https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
windowWidth = app.winfo_reqwidth()
windowHeight = app.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(app.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(app.winfo_screenheight()/3 - windowHeight)
# Positions the window in the center of the page.
app.geometry("+{}+{}".format(positionRight, positionDown))
app.mainloop()
