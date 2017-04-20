# card.py
import math

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
face = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

class Card(object):
        def __init__(self, card_val):
                self.val = card_val

        def __str__(self):
                self.string = str(face[self.val % 13]) + " of " + str(suits[int(math.floor(self.val / 13))])#+ str(suits[(self.val / 11) + 1])
                return self.string

        def __lt__(self, other):
                return self.val < other.val

        def __gt__(self, other):
                return self.val > other.val

        def __repr__(self):
                return "card_" + str(self.val)

        def toValue(self):
                return self.val
