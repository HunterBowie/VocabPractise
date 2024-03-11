import random
import tkinter
import tkinter.ttk

from constants import LARGE_FONT, PageType


class QuestionPage(tkinter.Frame):
    def __init__(self, controller: tkinter.Tk, *args):
        super().__init__(controller.container)
        self.controller = controller
        self.question_word = controller.vocab.get().get()[0]
        self.answer_word = controller.vocab.translate(self.question_word)

        label = tkinter.ttk.Label(
            self, text=self.question_word, font=LARGE_FONT)
        label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.text_entry = tkinter.ttk.Entry(self, font=LARGE_FONT)
        self.text_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.text_entry.focus()

        button = tkinter.ttk.Button(
            self, text="Submit", command=self.on_button_click)
        button.config()

        button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        controller.bind("<Return>", self.on_button_click)

    def on_button_click(self, *args: tuple) -> None:
        self.controller.show_page(
            PageType.ANSWER_PAGE, self.answer_word, self.text_entry.get()
        )
