import tkinter
from os import path

import playsound

from constants import LARGE_FONT, PLAY_SOUND, SMALL_FONT, PageType

CURRENT_DIR = path.dirname(__file__)
print(CURRENT_DIR)


class AnswerPage(tkinter.Frame):
    def __init__(self, controller: tkinter.Tk, *args):
        super().__init__(controller.container)
        self.answer_word = args[0]
        self.entered_word = args[1]
        self.controller = controller
        self.entered_word = self.entered_word.lstrip()
        self.entered_word = self.entered_word.rstrip()

        if self.entered_word == self.answer_word:
            if PLAY_SOUND:
                playsound.playsound(path.join(CURRENT_DIR, "correct.mp3"), False)
            controller.on_correct_answer()
            label_text = "Correct!"
            label_style = tkinter.ttk.Style()
            label_style.configure("BW.TLabel", foreground="green")
            sub_text = f'"{self.entered_word}" is "{self.controller.vocab.translate(self.entered_word)}"'
        else:
            if PLAY_SOUND:
                playsound.playsound(path.join(CURRENT_DIR, "incorrect.mp3"), False)
            controller.on_incorrect_answer()
            label_text = "Incorrect!"
            label_style = tkinter.ttk.Style()
            label_style.configure("BW.TLabel", foreground="red")
            sub_text = (
                f'The correct answer is "{self.answer_word}" not "{self.entered_word}"'
            )
        controller.vocab.next()

        label = tkinter.ttk.Label(
            self, text=label_text, font=LARGE_FONT, style="BW.TLabel"
        )
        label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        sub_label = tkinter.ttk.Label(self, text=sub_text, font=SMALL_FONT)
        sub_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        button = tkinter.ttk.Button(self, text="Ok", command=self.on_button_click)

        button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        controller.bind("<Return>", self.on_button_click)

    def on_button_click(self, *args: tuple) -> None:
        if self.controller.vocab.completed_full_cycle:
            self.controller.show_page(PageType.RESULTS_PAGE)
        else:
            self.controller.show_page(PageType.QUESTION_PAGE)
