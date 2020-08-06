import tkinter as tk
from string import punctuation
from random import randint
from questions import *
LARGE_FONT = ("Verdana", 12)

class ApplicationFramework(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (OpeningPage, QuestionPage):
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
        self.question_counter = 0
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
        for F, i in zip((biology_questions), (range(len(biology_questions)))):
            question_label = tk.Label(question_frame, text=biology_questions[F]["question"])
            self.question_label_array.append(question_label)
            self.question_label_array[i].grid(row=0, column=0, sticky="nsew")
            answer_a = tk.Button(answer_frame, text=biology_questions[F]["answers"]["a"])
            answer_b = tk.Button(answer_frame, text=biology_questions[F]["answers"]["b"])
            answer_c = tk.Button(answer_frame, text=biology_questions[F]["answers"]["c"])
            answer_d = tk.Button(answer_frame, text=biology_questions[F]["answers"]["d"])
            print(biology_questions[F]["answers"]["a"])
            print(biology_questions[F]["answers"]["b"])
            self.answers_array.append([answer_a, answer_b, answer_c, answer_d])
            self.answers_array[i][0].grid(row=0,column=0, sticky="nsew")
            self.answers_array[i][1].grid(row=0,column=1, sticky="nsew")
            self.answers_array[i][2].grid(row=0,column=2, sticky="nsew")
            self.answers_array[i][3].grid(row=0,column=3, sticky="nsew")
            
        self.iterate_question(0)
        next_question_button = tk.Button(self, text="next", command=lambda: self.iterate_question(self.question_counter))
        next_question_button.pack()


    def iterate_question(self, question):
        current_question = self.question_label_array[question]
        self.question_counter += 1
        current_question.tkraise()
        self.answers_array[question][0].tkraise()
        self.answers_array[question][1].tkraise()
        self.answers_array[question][2].tkraise()
        self.answers_array[question][3].tkraise()
        
        
        
        


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
