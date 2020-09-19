import tkinter as tk
from string import punctuation
from random import shuffle
from questions import biology_questions
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import tkinter.font as tkFont

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=False, enumerable=False):
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

for font in ["Mukta-Medium.ttf", "Mukta-Light.ttf", "Mukta-Regular.ttf", "Nunito-Bold.ttf", "Nunito-Regular.ttf"]: loadfont(font)
PRIMARY_BLACK = '#191308'
SECONDARY_BLACK = '#322A26'
DARK_BLUE = "#454B66"
MEDIUM_BLUE = "#677DB7"
LIGHT_BLUE = "#9CA3DB"

answer_list = {
    "correct":
        [],
    "incorrect":
        []
    }

class ApplicationFramework(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        # Center application to center of screen | Source: https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/3 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight)
        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
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
            frame.configure(bg="#ffffff")
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
        logo_source = tk.PhotoImage(file="Logo_Small.gif")
        logo = tk.Label(self, image=logo_source)
        logo.image = logo_source
        logo.grid(row=0, column=1, columnspan=3)
        opening_title = tk.Label(self, text="General Biology Quiz", font=("Nunito Bold", 22))
        opening_title.grid(row=1, column=1, columnspan=3, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        #frame_left = tk.Frame(self, bg=DARK_BLUE, height=int(self.winfo_screenheight()), width=100)
        #self.grid_propagate(0)
        #frame_left.grid(column=0, row=0, rowspan=20)
        #frame_right = tk.Frame(self, bg=DARK_BLUE, height=int(self.winfo_screenheight()), width=100)
        #frame_right.grid(column=4, row=0, rowspan=20)
        opening_subtitle = tk.Label(self, text="Welcome to the biology quiz application.", font=("Nunito Regular", 16))
        opening_subtitle.grid(row=2, column=2, columnspan=2, pady=5)
        name_validation_command = self.register(ApplicationFramework.name_validate_command)
        name_label = tk.Label(self, text="Please enter your name", font=("Mukta Medium", 16))
        name_input = tk.Entry(self, validate='all', validatecommand=(name_validation_command, '%P'), font=("Calibri", 11))
        name_label.grid(row=3, column=2, pady=30, padx=20)
        name_input.grid(row=3, column=3)
        next_button = tk.Button(self, text="Next", command=lambda: controller.show_frame("QuestionPage"))
        next_button.grid(row=4, column=1, columnspan=3)
        opening_widgets = [self, logo, opening_title, opening_subtitle, name_label, name_input]
        for i in opening_widgets: i.configure(bg="#ffffff")

class QuestionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        question_frame = tk.Frame(self, relief="sunken", height=100, width=100, bg=MEDIUM_BLUE)
        self.pack_propagate(0)
        question_frame.pack(expand="true", padx=0, pady=5)
        progress_frame = tk.Frame(self, relief="sunken", bg="grey")
        progress_frame.pack(fill='both', pady=0)
        answer_frame = tk.Frame(self, relief="sunken", bg=DARK_BLUE)
        answer_frame.pack(fill='both', expand="true", padx=10, pady=10)
        self.question_label_array = []
        self.answers_array = []
        self.used_questions = []
        self.order_of_questions = list(range(len(biology_questions)))
        shuffle(self.order_of_questions)
        self.question_iterator = 1
        self.correct_answers = tk.IntVar(value=0)
        self.incorrect_answers = tk.IntVar(value=0)
        answer_frame.grid_columnconfigure(0, weight=1)
        answer_frame.grid_columnconfigure(3, weight=1)
        answer_frame.grid_rowconfigure(0, weight=1)
        answer_frame.grid_rowconfigure(4, weight=2)
        self.confirm_button = tk.Button(answer_frame, text="Confirm", command=lambda: self.end_quiz())
        self.progress_bar = tk.Frame(progress_frame, width=40, bg="grey", height=40)
        self.progress_bar.pack()
        self.correct_label_contents = tk.StringVar()
        self.correct_label = tk.Label(answer_frame, textvariable=self.correct_label_contents, bg=DARK_BLUE, fg="#ffffff", font=("Mukta Regular", 14), width=15)
        self.correct_label.grid(row=1, column=3)
        self.next_button = tk.Button(answer_frame, text="Next", command=lambda: self.iterate_question(), state="disabled", font=("Mukta Regular", 14))
        self.next_button.grid(row=3, column=1, ipadx=10)
        self.skip_button = tk.Button(answer_frame, text="Skip", command=lambda: self.iterate_question(), font=("Mukta Regular", 14))
        self.skip_button.grid(row=3, column=2, ipadx=10)
        self.previous_button = tk.Button(answer_frame, text="Previous", command=lambda: self.previous_question(), font=("Mukta Regular", 14))
        self.previous_button.grid(row=3, column=3, ipadx=10)
        for F, i in zip((biology_questions), (range(len(biology_questions)))):
            question_label = tk.Label(question_frame, text=biology_questions[F]["question"], font=("Nunito Bold", 24))
            self.question_label_array.append(question_label)
            self.question_label_array[i].grid(row=0, column=0, sticky="nsew")
            self.question_label_array[i].configure(fg=PRIMARY_BLACK, bg="white")
            answer_a = tk.Button(answer_frame, text=biology_questions[F]["answers"]["a"], command=lambda i=i: self.check_answer(i, "a"), font=("Mukta Medium", 18))
            answer_b = tk.Button(answer_frame, text=biology_questions[F]["answers"]["b"], command=lambda i=i: self.check_answer(i, "b"), font=("Mukta Medium", 18))
            answer_c = tk.Button(answer_frame, text=biology_questions[F]["answers"]["c"], command=lambda i=i: self.check_answer(i, "c"), font=("Mukta Medium", 18))
            answer_d = tk.Button(answer_frame, text=biology_questions[F]["answers"]["d"], command=lambda i=i: self.check_answer(i, "d"), font=("Mukta Medium", 18))
            self.answers_array.append([answer_a, answer_b, answer_c, answer_d])
            for button in self.traverse(self.answers_array): button.configure(bg="white", bd=0, disabledforeground=LIGHT_BLUE, fg=PRIMARY_BLACK)
            self.answers_array[i][0].grid(row=1,column=1, sticky="nsew", pady=10, padx=10)
            self.answers_array[i][1].grid(row=1,column=2, sticky="nsew", pady=10)
            self.answers_array[i][2].grid(row=2,column=1, sticky="nsew", pady=10, padx=10)
            self.answers_array[i][3].grid(row=2,column=2, sticky="nsew", pady=10)
                
        
        for button in [self.skip_button, self.previous_button, self.next_button]: button.configure(fg=SECONDARY_BLACK, bg="#ffffff", bd=0)
        self.initialize_quiz()

    def traverse(self, o, tree_types=(list, tuple)): # Taken from https://stackoverflow.com/questions/6340351/iterating-through-list-of-list-in-python
            if isinstance(o, tree_types):
                for value in o:
                    for subvalue in self.traverse(value, tree_types):
                        yield subvalue
            else:
                yield o

    def initialize_quiz(self):
        first_question = self.order_of_questions[0]
        self.question_label_array[first_question].tkraise()
        for i in range(0, 4): self.answers_array[first_question][i].tkraise()
        
    def iterate_question(self, previous=0):
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
        self.skip_button['state'] = "normal"
        self.correct_label_contents.set("")
        if next_question == biology_questions[-1]:
            self.confirm_button.grid(row=3, column=5)
        else:
            self.confirm_button.grid_forget()

    def previous_question(self, previous=0): #FINISH THE RESET FUNCTION AND IF STATEMENT IN THE END
        if self.question_iterator == 1:
            return
        previous_question = self.order_of_questions[self.question_iterator - 2]
        self.question_label_array[previous_question].tkraise()
        for i in range(0,4): self.answers_array[previous_question][i].tkraise()
        self.question_iterator -= 1
        self.next_button['state'] = "disabled"
        self.skip_button['state'] = "normal"

    def check_answer(self, question_number, answer_value):
        correct_answer_value = biology_questions[question_number]["correct_answer"]
        for widget in self.traverse(self.answers_array):
            if widget.winfo_ismapped() == 1 and widget['text'] == biology_questions[question_number]["answers"][correct_answer_value]:
                widget.configure(bg=MEDIUM_BLUE)
        if biology_questions[question_number]["correct_answer"] == answer_value:
            answer_list["correct"].append(1)
            self.correct_label_contents.set("That was correct")
        else:
            answer_list["incorrect"].append(1)
            self.correct_label_contents.set("That was incorrect")
        current_question = self.order_of_questions[self.question_iterator - 1]
        self.question_label_array[current_question].tkraise()
        for i in range(0,4): self.answers_array[current_question][i]['state'] = "disabled"
        self.next_button['state'] = "normal"
        if next_question == biology_questions[-1]:
            self.next_button['state'] = "disabled"
        self.skip_button['state'] = "disabled"

class FinalPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.final_output = tk.StringVar()
            final_score = tk.Label(self, textvariable=self.final_output)
            start_again = tk.Button(self, text="Start Again", command=lambda: self.reset_quiz())
            start_again.grid()
            final_score.grid()
            stop_quiz = tk.Button(self, text="Stop quiz", command=lambda: self.stop_quiz())
            stop_quiz.grid()

        def stop_quiz(self):
            return

        def reset_quiz(self):
            pass
            #self.destroy()

        def output(self):
            self.final_output.set("Congratulations, you got " + str(self.controller.frames[QuestionPage.__name__].correct_answers.get()) +
                                  " correct and " + str(self.controller.frames[QuestionPage.__name__].incorrect_answers.get()) + " incorrect, and you skipped " +
                                  str(len(biology_questions) - (self.controller.frames[QuestionPage.__name__].correct_answers.get() + self.controller.frames[QuestionPage.__name__].incorrect_answers.get())))

app = ApplicationFramework()
app.mainloop()
