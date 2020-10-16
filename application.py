import tkinter as tk
from tkinter import messagebox
from string import punctuation
from random import shuffle
from questions import biology_questions
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import tkinter.font as tkFont

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20
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

# Function for loading custom fonts
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

# Load custom fonts needed for the application
for font in ["Mukta-Medium.ttf", "Mukta-Light.ttf", "Mukta-Regular.ttf", "Nunito-Bold.ttf", "Nunito-Regular.ttf"]: loadfont(str("./fonts/" + font))
TITLE_FONT_BOLD = "Nunito Bold"
TITLE_FONT = "Nunito Regular"
BODY_LARGE = ("Mukta Medium", 18)
BODY_MEDIUM = ("Mukta Regular", 16)
BODY_SMALL = ("Mukta Regular", 14)

class ApplicationFramework(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("900x600")
        # Center application to center of screen | Source: https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/3 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight)
        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.iconbitmap("./images/Logo.ico")
        self.title("Biology Quiz")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.loop_decide_variable = False
        # Creates each frame by using a for loop and by creating the classes below and gridding them, and then to iterate it raises the next frame
        for F in (OpeningPage, QuestionPage, FinalPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg="#ffffff")
        self.show_frame("OpeningPage")

    # Function to raise the next frame in the quiz
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    # Destroys and closes the tkinter window
    def kill_quiz(self):
        self.destroy()

    # Outputs a boolean to check whether to loop code or not (reset quiz)
    def output_loop_variable(self):
        return self.loop_decide_variable

    # General function to validate the name of the person
    @staticmethod
    def name_validate_command(new_text):
        # validation command for the name entry
        for letter in new_text:
            if letter.isdigit() or letter in punctuation:
                return False
        if len(new_text) > 20:
            return False
        return not new_text.isdigit()
    
# Class that holds the opening page of the quiz
class OpeningPage(tk.Frame):

    # Initializes the widgets in the opening page of the quiz
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Set the source of the logo and add it to a label
        logo_source = tk.PhotoImage(file="./images/Logo_Small.gif")
        logo = tk.Label(self, image=logo_source)
        logo.image = logo_source
        logo.grid(row=0, column=1, columnspan=3)
        opening_title = tk.Label(self, text="General Biology Quiz", font=(TITLE_FONT_BOLD, 22))
        opening_title.grid(row=1, column=1, columnspan=3, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        next_button = tk.Button(self, text="Next", command=lambda: self.next_button(), font=BODY_SMALL)
        next_button.configure(fg=SECONDARY_BLACK, bg=LIGHT_BLUE, bd=0)
        next_button.grid(row=4, column=1, columnspan=3, ipadx=10)
        opening_subtitle = tk.Label(self, text="Welcome to the biology quiz application.", font=(TITLE_FONT, 16))
        opening_subtitle.grid(row=2, column=2, columnspan=2, pady=5)
        name_validation_command = self.register(ApplicationFramework.name_validate_command)
        name_label = tk.Label(self, text="Please enter your name", font=("Mukta Medium", 16)) # Validates the entry widget
        user_name = tk.StringVar(controller)
        self.name_input = tk.Entry(self, textvariable=user_name, validate='all', validatecommand=(name_validation_command, '%P'), font=("Mukta Light", 12)) 
        name_label.grid(row=3, column=2, pady=30, padx=20)
        self.name_input.grid(row=3, column=3)
        opening_widgets = [self, logo, opening_title, opening_subtitle, name_label, self.name_input]
        for i in opening_widgets: i.configure(bg="#ffffff") # Configures all widgets in the opening page to be white

    # Function to see if there is a name entered in the entry to continue. If not, then return an error message
    def next_button(self):
        if self.name_input.get() == "":
            return messagebox.showerror("No name entered", "Please enter a name to continue.")
        return self.controller.show_frame("QuestionPage")

# Class that holds the opening page of the quiz
class QuestionPage(tk.Frame):

    # Initializes the widgets in the question page of the quiz
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        question_frame = tk.Frame(self, relief="sunken", height=100, width=100, bg=MEDIUM_BLUE)
        self.pack_propagate(0)
        question_frame.pack(expand="true", padx=0, pady=5)
        progress_frame = tk.Frame(self, relief="sunken", bg=MEDIUM_BLUE)
        progress_frame.pack(fill='both', pady=0)
        answer_frame = tk.Frame(self, relief="sunken", bg=DARK_BLUE)
        answer_frame.pack(fill='both', expand="true", padx=0, pady=0)
        self.question_label_array = []
        self.answers_array = []
        self.used_questions = []
        self.order_of_questions = list(range(len(biology_questions))) # Creates a list of integers holding the number of biology questions
        shuffle(self.order_of_questions) # Shuffles the list in order for it to be in random order
        # Initializes other variables to their starting point
        self.question_iterator = 1
        self.correct_answers = tk.IntVar(value=0)
        self.incorrect_answers = tk.IntVar(value=0)
        self.end_statement = tk.StringVar()
        answer_frame.grid_columnconfigure(0, weight=1)
        answer_frame.grid_columnconfigure(5, weight=1)
        answer_frame.grid_rowconfigure(0, weight=1)
        answer_frame.grid_rowconfigure(4, weight=2)
        # Creation of all buttons needed outside the frame where all the questions and answers are contained
        self.confirm_button = tk.Button(answer_frame, text="Confirm", command=lambda: self.iterate_question(end=True), font=BODY_SMALL)
        self.progress_bar = tk.Frame(progress_frame, bg=MEDIUM_BLUE, height=10)
        self.progress_bar.pack()
        self.progress_bar_width = tk.DoubleVar()
        self.progress_bar_width.set(self.question_iterator/len(biology_questions)*100)
        self.actual_progress_bar = tk.Frame(self.progress_bar, bg=MEDIUM_BLUE, height=20, width=self.progress_bar_width.get())
        self.actual_progress_bar.grid(row=0,column=0)
        self.progress_bar_backdrop = tk.Frame(self.progress_bar, bg=SECONDARY_BLACK, height=20, width=100)
        self.progress_bar_backdrop.grid(row=0, column=0)
        #self.actual_progress_bar.tkraise()
        self.correct_label_contents = tk.StringVar()
        self.correct_label = tk.Label(answer_frame, textvariable=self.correct_label_contents, bg=DARK_BLUE, fg="#ffffff", font=BODY_MEDIUM, width=15)
        self.correct_label.grid(row=0, column=1, columnspan=4)
        self.next_button = tk.Button(answer_frame, text="Next", command=lambda: self.iterate_question(), state="disabled", font=BODY_SMALL)
        self.next_button.grid(row=3, column=2, ipadx=10)
        self.skip_button = tk.Button(answer_frame, text="Skip", command=lambda: self.iterate_question(), font=BODY_SMALL)
        self.skip_button.grid(row=3, column=3, columnspan=2, ipadx=10)
        self.previous_button = tk.Button(answer_frame, text="Previous", command=lambda: self.previous_question(), font=BODY_SMALL)
        self.previous_button.grid(row=3, column=1, ipadx=10)
        for F, i in zip((biology_questions), (range(len(biology_questions)))): # Creates each question and answer and other content for each question in a for loop and hides them behind eachother.
            question_label = tk.Label(question_frame, text=biology_questions[F]["question"], font=(TITLE_FONT_BOLD, 24))
            self.question_label_array.append(question_label)
            self.question_label_array[i].grid(row=0, column=0, sticky="nsew")
            self.question_label_array[i].configure(fg=PRIMARY_BLACK, bg="white")
            # Create each button with their custom parameters
            answer_a = tk.Button(answer_frame, text=biology_questions[F]["answers"]["a"], command=lambda i=i: self.check_answer(i, "a"), font=BODY_LARGE)
            answer_b = tk.Button(answer_frame, text=biology_questions[F]["answers"]["b"], command=lambda i=i: self.check_answer(i, "b"), font=BODY_LARGE)
            answer_c = tk.Button(answer_frame, text=biology_questions[F]["answers"]["c"], command=lambda i=i: self.check_answer(i, "c"), font=BODY_LARGE)
            answer_d = tk.Button(answer_frame, text=biology_questions[F]["answers"]["d"], command=lambda i=i: self.check_answer(i, "d"), font=BODY_LARGE)
            
            self.answers_array.append([answer_a, answer_b, answer_c, answer_d])
            for button in self.traverse(self.answers_array): button.configure(bg="white", bd=0, disabledforeground=LIGHT_BLUE, fg=PRIMARY_BLACK) # A nested loop for creating the four buttons for each question
            # Grid each button in their separate areas
            self.answers_array[i][0].grid(row=1,column=1, columnspan=2, sticky="nsew", pady=10, padx=10)
            self.answers_array[i][1].grid(row=1,column=3, columnspan=2, sticky="nsew", pady=10)
            self.answers_array[i][2].grid(row=2,column=1, columnspan=2, sticky="nsew", pady=10, padx=10)
            self.answers_array[i][3].grid(row=2,column=3, columnspan=2, sticky="nsew", pady=10)

        for button in [self.skip_button, self.previous_button, self.next_button, self.confirm_button]: button.configure(fg=SECONDARY_BLACK, bg="#ffffff", bd=0)
        self.initialize_quiz()

    # Allows iteration inside lists inside lists
    def traverse(self, o, tree_types=(list, tuple)): # Taken from https://stackoverflow.com/questions/6340351/iterating-through-list-of-list-in-python
            if isinstance(o, tree_types):
                for value in o:
                    for subvalue in self.traverse(value, tree_types):
                        yield subvalue
            else:
                yield o
                
    # Initializes the first question inside the quiz by calling the first integer in the shuffled list
    def initialize_quiz(self):
        first_question = self.order_of_questions[0]
        self.question_label_array[first_question].tkraise()
        for i in range(0, 4): self.answers_array[first_question][i].tkraise()

    # Iterates through each question, and if an error (reaches end of list) then sets the final score for variables and proceeds to the final page
    def iterate_question(self, previous=0, end=False):
        try:
            next_question = self.order_of_questions[self.question_iterator]
            if end is True:
                raise IndexError
        except IndexError:
            # Sets each variable based on the amount correct or incorrect
            self.correct_answers.set(sum(answer_list["correct"]))
            self.incorrect_answers.set(sum(answer_list["incorrect"]))
            if sum(answer_list["correct"]) >= (len(biology_questions)/3*2):
                self.end_statement.set("Congratulations " + self.controller.frames[OpeningPage.__name__].name_input.get() + ", you got excellence, with: \n")
            elif (len(biology_questions)/3) <= sum(answer_list["correct"]) < (len(biology_questions)/3*2):
                self.end_statement.set("Good job " + self.controller.frames[OpeningPage.__name__].name_input.get() + ", you got merit, with: \n")
            else:
                self.end_statement.set("Too bad " + self.controller.frames[OpeningPage.__name__].name_input.get() + ", you got achieved/not achieved, with: \n")
            self.controller.frames[FinalPage.__name__].output()
            return self.controller.show_frame("FinalPage")
        self.question_label_array[next_question].tkraise()
        for i in range(0,4): self.answers_array[next_question][i].tkraise()
        self.question_iterator += 1
        # Changes the state of each button for the next question
        self.next_button['state'] = "disabled"
        self.skip_button['state'] = "normal"
        self.correct_label_contents.set("")
        if next_question == self.order_of_questions[-1]:
            self.confirm_button.grid(row=4, column=1, columnspan=4, ipadx=10)
            self.skip_button['state'] = "disabled"
        else:
            self.confirm_button.grid_forget() # If the final question, then grid or hide the confirm button

    # Allows the user to iterated backwards to a previous question by reversing the above procedures
    def previous_question(self, previous=0):
        if self.question_iterator == 1:
            return
        previous_question = self.order_of_questions[self.question_iterator - 2]
        self.question_label_array[previous_question].tkraise()
        for i in range(0,4): self.answers_array[previous_question][i].tkraise()
        self.question_iterator -= 1
        self.next_button['state'] = "disabled"
        self.skip_button['state'] = "normal"
        if self.confirm_button.winfo_ismapped() == 1:
            self.confirm_button.grid_forget()

    # Is called when an answer is clicked, checks if the answer is correct or not and outputs it onto the quiz, as well as appending the answer. Also makes it unable to change the answer
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
        self.progress_bar_width.set((len(answer_list["correct"])+len(answer_list["incorrect"]))/len(biology_questions)*100)
        self.actual_progress_bar.configure(width=self.progress_bar_width.get())
        self.actual_progress_bar.tkraise()
        self.next_button['state'] = "normal"
        self.skip_button['state'] = "disabled"
        if self.confirm_button.winfo_ismapped() == 1:
            self.confirm_button['state'] = "normal"
            self.next_button['state'] = "disabled"

# Class that holds the final page of the quiz
class FinalPage(tk.Frame):

        # Initializes the widges in the final page of the quiz
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            final_page_title = tk.Label(self, text="Final Results", font=(TITLE_FONT_BOLD, 20))
            final_page_title.grid(row=1, column=1, columnspan=3)
            self.final_output = tk.StringVar()
            final_score = tk.Label(self, textvariable=self.final_output, font=("Mukta Medium", 16))
            # Define the buttons in order to either start again or stop the quiz
            start_again = tk.Button(self, text="Start Again", command=lambda: self.reset_quiz(), font=BODY_SMALL)
            start_again.grid(row=3, column=1, pady=50)
            final_score.grid(row=2, column=1, columnspan=2)
            stop_quiz = tk.Button(self, text="Stop quiz", command=lambda variable=self.controller.loop_decide_variable: self.stop_quiz(), font=BODY_SMALL)
            stop_quiz.grid(row=3, column=2, pady=50)
            logo_source = tk.PhotoImage(file="./images/Logo_Small.gif")
            logo = tk.Label(self, image=logo_source)
            logo.image = logo_source
            logo.grid(row=0, column=1, columnspan=3)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(4, weight=1)
            final_widgets = [final_score, start_again, stop_quiz, final_page_title, logo]
            for i in final_widgets: i.configure(bg="#ffffff")
            start_again.configure(fg=SECONDARY_BLACK, bg=LIGHT_BLUE, bd=0)
            stop_quiz.configure(fg=SECONDARY_BLACK, bg=LIGHT_BLUE, bd=0)

        # Calls a function from the framework to kill the entire quiz
        def stop_quiz(self):
            return self.controller.kill_quiz()

        # Does the same as above but also sets a variable so that the quiz will be regenerated
        def reset_quiz(self):
            self.controller.loop_decide_variable = True
            return self.controller.kill_quiz()

        # Sets the output for the final score variable above in a condensed manner
        def output(self):
            self.final_output.set("{} {} correct,\n {} incorrect,\n and you skipped {} questions.".format(
                self.controller.frames[QuestionPage.__name__].end_statement.get(),
                self.controller.frames[QuestionPage.__name__].correct_answers.get(),
                self.controller.frames[QuestionPage.__name__].incorrect_answers.get(),
                len(biology_questions) -(self.controller.frames[QuestionPage.__name__].correct_answers.get() +
                self.controller.frames[QuestionPage.__name__].incorrect_answers.get())
                )
                                  )
# For loop to allow the code to be reset and regenerated, or broken out of with no problems
while True:
    loop_decider = False # Immediately sets the variable as false in order to allow users to close the window
    app = ApplicationFramework()
    app.mainloop()
    if app.output_loop_variable() == True:
        loop_decider = True
    elif loop_decider == False:
        break
    
