import random
import tkinter
import tkinter.ttk
from os import path

import playsound

CURRENT_DIR = path.dirname(__file__)

PLAY_SOUND = True

answers = []


def calc_average() -> str:
    return str(round((sum(answers) / len(answers)) * 100)) + "%"


class Vocab:
    def __init__(self) -> None:
        self.vocab = []
        with open(path.join(CURRENT_DIR, "vocab.txt"), "r") as file:
            text = file.read()
            text = text.split("\n")
            for words in text:
                fr_word, en_word = words.split(":")
                self.vocab.append(
                    [fr_word.lstrip().rstrip(), en_word.lstrip().rstrip()]
                )
        random.shuffle(self.vocab)
        self.index = 0

    def translate(self, word: str) -> str:
        for fr_word, en_word in self.vocab:
            if word == fr_word:
                return en_word
            if word == en_word:
                return fr_word

    def next(self) -> list:
        word_pair = self.vocab[self.index]
        self.index += 1
        if self.index == 20:
            self.index = 0
            random.shuffle(self.vocab)
        return word_pair


vocab = Vocab()

LARGE_FONT = ("Verdana", 35)
SMALL_FONT = ("Verdana", 25)


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("750x350")
        self.title("Vocabulary Practise")
        self.container = tkinter.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.average = tkinter.StringVar(value="0%")
        self.average_label = tkinter.ttk.Label(
            self, textvariable=self.average, font=LARGE_FONT
        )
        self.average_label.place(relx=1 - 0.96, rely=0.05, anchor=tkinter.NW)

        self.question = tkinter.StringVar(value="1/20")
        self.question_label = tkinter.ttk.Label(
            self, textvariable=self.question, font=LARGE_FONT
        )
        self.question_label.place(relx=0.96, rely=0.05, anchor=tkinter.NE)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = []
        for Page in (QuestionPage, AnswerPage, ResultsPage):
            page = Page(self.container, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages.append(page)

        self.show_page(0)

    def show_page(self, page_number) -> None:
        page = self.pages[page_number]
        page.tkraise()


class QuestionPage(tkinter.Frame):
    def __init__(self, parent, controller: App):
        self.controller = controller
        self.word: str = random.choice(vocab.next())
        tkinter.Frame.__init__(self, parent)
        label = tkinter.ttk.Label(self, text=self.word, font=LARGE_FONT)
        label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.text_entry = tkinter.ttk.Entry(self, font=LARGE_FONT)
        self.text_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.text_entry.focus()

        button = tkinter.ttk.Button(self, text="Submit", command=self.on_button_click)
        button.config()

        button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        controller.bind("<Return>", self.on_button_click)

    def on_button_click(self, *args: tuple) -> None:
        self.controller.pages[1].set_word(self.word)
        self.controller.pages[1].set_answer(self.text_entry.get())
        self.controller.show_page(1)


class AnswerPage(tkinter.Frame):
    def init(self, parent, controller: App):
        self.controller = controller
        tkinter.Frame.init(self, parent)
        self.word_label = tkinter.ttk.Label(self, font=LARGE_FONT)
        self.word_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.sub_label = tkinter.ttk.Label(self, font=SMALL_FONT)
        self.sub_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        button = tkinter.ttk.Button(self, text="Ok", command=self.on_button_click)
        button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        controller.bind("<Return>", self.on_button_click)

        def set_word(self, word: str) -> None:
            self.word = word
            self.word_label["text"] = self.word

        def set_answer(self, answer: str) -> None:
            self.answer_given = answer.lstrip().rstrip()
            self.display_feedback()

        def display_feedback(self) -> None:
            label_text = "Correct!"
            label_style = tkinter.ttk.Style()
            label_style.configure("BW.TLabel", foreground="green")
            sub_text = f'"{self.word}" is "{self.answer_given}"'
            if vocab.translate(self.word) != self.answer_given:
                if PLAY_SOUND:
                    playsound.playsound(path.join(CURRENT_DIR, "incorrect.mp3"), False)
                answers.append(0)
                label_text = "Incorrect!"
                label_style.configure("BW.TLabel", foreground="red")
                sub_text = f'The correct answer is "{vocab.translate(self.word)}" not "{self.answer_given}"'
            else:
                answers.append(1)
                if PLAY_SOUND:
                    playsound.playsound(path.join(CURRENT_DIR, "correct.mp3"), False)

            self.controller.average.set(calc_average())

            self.word_label["text"] = label_text
            self.word_label["style"] = "BW.TLabel"
            self.sub_label["text"] = sub_text

    def on_button_click(self, *args: tuple) -> None:
        if vocab.index == 0:
            self.controller.show_page(2)
        else:
            question_num = int(self.controller.question.get()[:-3])
            self.controller.question.set(str(question_num + 1) + "/20")
            self.controller.pages[0].word = random.choice(vocab.next())
            self.controller.show_page(0)


class ResultsPage(tkinter.Frame):
    def init(self, parent, controller: App):
        tkinter.Frame.init(self, parent)
        self.controller = controller
        label = tkinter.ttk.Label(
            self, text="You Finished 20 Questions!", font=LARGE_FONT
        )
        label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        sub_label = tkinter.ttk.Label(
            self, text=f"Your average was {calc_average()}", font=SMALL_FONT
        )
        sub_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


app = App()
app.mainloop()
