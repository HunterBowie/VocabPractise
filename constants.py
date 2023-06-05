from enum import Enum, auto
from os import path

CURRENT_DIR = path.dirname(__file__)

PLAY_SOUND = True
LARGE_FONT = "Verdana", 35
SMALL_FONT = "Verdana", 25

VOCAB_FILE = "input.txt"


class PageType(Enum):
    QUESTION_PAGE = auto()
    ANSWER_PAGE = auto()
    RESULTS_PAGE = auto()
