from card import *
import random

class Deck(object):
        def __init__(self):
                self.used = []#to fix reshuffle
                self.deck = []
                for x in range(0,52):
                        self.deck.append(Card(x))
                        random.shuffle(self.deck)
        def __str__(self):
                self.string = ""
                for x in self.deck:
                        self.string = self.string + str(x) + " \n"
                return self.string

        def getCard(self):
                card = self.deck.pop()
                self.used.append(card)
                return card

        def shuffleDeck(self):
                self.deck = self.deck + self.used
                self.used = []
                random.shuffle(self.deck)
