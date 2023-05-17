import random
from os import path
from typing import Tuple

from constants import VOCAB_FILE

CURRENT_DIR = path.dirname(__file__)


class Vocab:
    """The current vocabulary set being practised."""

    def __init__(self) -> None:
        self.vocab: list[Tuple[str, str]] = []
        with open(path.join(CURRENT_DIR, VOCAB_FILE), "r") as file:
            text = file.read()
            text = text.split("\n")
            for words in text:
                word1, word2 = words.split(":")
                self.vocab.append((word1.lstrip(), word2.lstrip()))
        self.index = 0

    def shuffle(self):
        """Shuffle the current list of word pairs."""
        random.shuffle(self.vocab)

    def translate(self, word: str) -> str:
        """Translate a word using the current vocabulary."""
        for word1, word2 in self.vocab:
            if word == word1:
                return word2
            if word == word2:
                return word1

    def get(self):
        """Gets the currently held word pair."""
        return self.vocab[self.index]

    def next(self) -> None:
        """Moves the next word pair in the list to the currently held one."""
        self.index += 1
        if self.index == 20:
            self.index = 0
