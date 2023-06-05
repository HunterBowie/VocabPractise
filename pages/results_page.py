import tkinter
import tkinter.ttk

from constants import LARGE_FONT, SMALL_FONT, PageType


class ResultsPage(tkinter.Frame):
    def __init__(self, controller: tkinter.Tk, *args):
        super().__init__(controller.container)
        self.controller = controller
        label = tkinter.ttk.Label(
            self,
            text=f"You Finished {len(controller.vocab)} Questions!",
            font=LARGE_FONT,
        )
        label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        sub_label = tkinter.ttk.Label(
            self, text=f"Your average was {controller.average.get()}", font=SMALL_FONT
        )
        sub_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        button = tkinter.ttk.Button(self, text="again", command=self.on_button_click)
        button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def on_button_click(self, *args: tuple) -> None:
        self.controller.reset()
        self.controller.show_page(PageType.QUESTION_PAGE)
