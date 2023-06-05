import random
from dataclasses import dataclass
from os import path
from typing import Tuple

from constants import VOCAB_FILE

CURRENT_DIR = path.dirname(__file__)


@dataclass
class VocabPair:
    first_word: str
    second_word: str
    rec: bool

    def get(self):
        if self.rec:
            return [self.first_word]
        return [self.first_word, self.second_word]


class Vocab:
    """The current vocabulary set being practised."""

    def __init__(self) -> None:
        self.vocab: list[VocabPair[str, str]] = []
        with open(path.join(CURRENT_DIR, VOCAB_FILE), "r") as file:
            text = file.read()
            text = text.split("\n")
            for line in text:
                rec = False
                new_line = line
                if "(rec)" in line:
                    new_line = line.replace("(rec)", "")
                    rec = True
                word1, word2 = new_line.split(":")
                self.vocab.append(VocabPair(word1.lstrip(), word2.lstrip(), rec))
        self._index = 0
        self._max_index = len(self.vocab)
        self.completed_full_cycle = False

    def __len__(self):
        return len(self.vocab)

    def config_max_index(self, max_index: int):
        "Change the maximum number of different vocab word pairs are passed over."
        self._max_index = max_index
        self._index = 0

    def shuffle(self):
        """Shuffle the current list of word pairs."""
        random.shuffle(self.vocab)

    def translate(self, word: str) -> str:
        """Translate a word using the current vocabulary."""
        for pair in self.vocab:
            if word == pair.first_word:
                return pair.second_word
            if word == pair.second_word:
                return pair.first_word

    def get(self) -> VocabPair:
        """Gets the currently held word pair."""
        return self.vocab[self._index]

    def next(self) -> None:
        """Moves the next word pair in the list to the currently held one."""
        if self._index + 1 == self._max_index:
            self._index = 0
            self.completed_full_cycle = True
        else:
            self._index += 1
