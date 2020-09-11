import tkinter as tk
from string import punctuation
from random import shuffle
from questions import biology_questions
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import tkinter.font as tkFont

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=False, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.
    `private`     if True, other processes cannot see this font, and this 
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts
    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx
    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
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

loadfont("Mukta-Medium.ttf")
loadfont("Mukta-Light.ttf")
loadfont("Mukta-Regular.ttf")
loadfont("Nunito-Bold.ttf")
loadfont("Nunito-Regular.ttf")
TITLE_FONT = ("Calibri", 12)

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
        question_frame = tk.Frame(self, relief="sunken", bg="black", height=self.winfo_height()/2, width=100)
        question_frame.pack_propagate(0)
        question_frame.pack(expand="True", fill='both', padx=5, pady=5)
        progress_frame = tk.Frame(self, relief="sunken", bg="grey")
        progress_frame.pack(fill='both')
        answer_frame = tk.Frame(self, relief="sunken", bg="red")
        answer_frame.pack(fill='both', padx=10, pady=5)
        test_answer = tk.Label(answer_frame, text="Answer frame")
        test_answer.grid(row=0, column=1)
        self.question_label_array = []
        self.answers_array = []
        self.used_questions = []
        self.order_of_questions = list(range(len(biology_questions)))
        shuffle(self.order_of_questions)
        self.question_iterator = 1
        self.correct_answers = tk.IntVar(value=0)
        self.incorrect_answers = tk.IntVar(value=0)
        for F, i in zip((biology_questions), (range(len(biology_questions)))):
            question_label = tk.Label(question_frame, text=biology_questions[F]["question"])
            self.question_label_array.append(question_label)
            self.question_label_array[i].grid(row=0, column=0, sticky="nsew")
            self.question_label_array[i].configure(bg="black")
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
