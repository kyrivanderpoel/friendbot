import string
from random import choice

from tabulate import tabulate
import attr

def get_words(min_length):
    with open("/usr/share/dict/words", "r") as f:
        words = []
        for word in f.readlines():
            word = word.strip("\n")
            if len(word) >= min_length:
                words.append(word.lower())
    return words

WORDS = get_words(5)

def get_random_word():
    return choice(WORDS)


@attr.s
class Hangman(object):
    word = attr.ib(default=attr.Factory(get_random_word))
    guessed = attr.ib(default=attr.Factory(set))
    misses = attr.ib(default=0)
    max_misses = attr.ib(default=5)

    def was_guessed(self, guess):
        guess = guess.lower()
        return guess in self.guessed

    def guess(self, guess):
        guess = guess.lower()
        self.guessed.add(guess)
        if guess in self.word:
            return True
        else:
            self.misses += 1
            return False

    def hangman_string(self):
        s = ""
        for letter in self.word:
            s += letter if letter in self.guessed else "/"
        return s

    def won(self):
        return "/" not in self.hangman_string()

    def lost(self):
        return self.misses >= self.max_misses

    def choices(self):
        return sorted(set(string.ascii_lowercase) - self.guessed)

    def remaining_attempts(self):
        return self.max_misses - self.misses

    def stats_table(self):
        stat_tuples = [
            ("Your Guess", self.hangman_string()),
            ("Word", self.word),
            ("Remaining Attempts", self.remaining_attempts()),
        ]
        return tabulate(stat_tuples)

