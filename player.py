#from game import *

# Player default class

class Player(object):
	def __init__(self):
		self.name = "default"
		self.hand = [-1, -1]
		self.betFlag = 0

	def setChips(self,chips):
		self.chips = chips

	def addChips(self, amount):
		self.chips += amount

	def subChips(self, amount):
		self.chips -= amount

	def setActiveGame(self, game):
		self.game = game

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def resetFlag(self):
		self.betFlag = 0

	def setHand(self, card1, card2):
		self.hand = [card1, card2]

	def getHand(self):
		return self.hand

	def action(self, maxbet):
		# bet
		# raise
		# call
		# check
		# fold
		return(["check"])

	def collectAnti(self, amount):
		self.chips -= amount
		return amount

	def chipAmount(self):
		return self.chips