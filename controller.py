import tkinter
import tkinter.ttk

from constants import LARGE_FONT, PageType
from pages import AnswerPage, QuestionPage, ResultsPage
from vocab import Vocab


class Controller(tkinter.Tk):
    PAGES: dict[PageType : tkinter.Frame.__class__] = {
        PageType.QUESTION_PAGE: QuestionPage,
        PageType.ANSWER_PAGE: AnswerPage,
        PageType.RESULTS_PAGE: ResultsPage,
    }

    def __init__(self):
        super().__init__()

        self.vocab = Vocab()
        self.vocab.shuffle()
        self.page: tkinter.Frame = None

        self.geometry("750x350")
        self.title("Vocabulary Practise")
        self.container = tkinter.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.average = tkinter.StringVar()
        self.average_label = tkinter.ttk.Label(
            self, textvariable=self.average, font=LARGE_FONT
        )
        self.average_label.place(relx=1 - 0.96, rely=0.05, anchor=tkinter.NW)

        self.question = tkinter.StringVar()
        self.question_label = tkinter.ttk.Label(
            self, textvariable=self.question, font=LARGE_FONT
        )
        self.question_label.place(relx=0.96, rely=0.05, anchor=tkinter.NE)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.reset()

        self.show_page(PageType.QUESTION_PAGE)

    def calc_average(self) -> float:
        if sum(self.answers) == 0:
            return 0
        return round((sum(self.answers) / len(self.answers)) * 100)

    def show_page(self, page_type: PageType, *args) -> None:
        if page_type == PageType.QUESTION_PAGE:
            question_num = int(self.question.get()[:-3])
            self.question.set(str(question_num + 1) + f"/{len(self.vocab)}")
            self.average.set(str(self.calc_average()) + "%")
        self.page = self.PAGES[page_type](self, *args)
        self.page.grid(row=0, column=0, sticky="nsew")
        self.page.tkraise()

    def on_correct_answer(self):
        self.answers.append(1)

    def on_incorrect_answer(self):
        self.answers.append(0)

    def reset(self):
        self.answers = []
        self.question.set(f"0/{len(self.vocab)}")
        self.average.set("0%")
