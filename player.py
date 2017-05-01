#from game import *

# Player default class
import re

class Player(object):
	def __init__(self):
		self.name = "default"
		self.hand = [-1, -1]
		self.betFlag = 0
		self.round = 0
		self.chips = 0

	def handToValue(self):
		self.tempHand = []
		for x in self.hand:
			self.tempHand.append(x.toValue())
		return self.tempHand

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
		self.round = 0

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
		return(["fold", 0])

	def collectAnti(self, amount):
		self.chips -= amount
		return amount

	def legal_moves(self, history, maxbet):
			moves = set()
			if self.haveBet(history): moves.add("call")#bet has occured
			else: moves= set(["check"])#bet has not occured
			if (not self.betFlag) and maxbet>0:
					if "check" in moves: moves.add("bet")
					else: moves.add("raise")
			if self.chips: moves.add("fold")#check for all in, don't fold if no chips are left
			return moves

	def haveBet(self, history):#TODO: check for hand end, check for round end
			for i in range(-1, -1*len(history), -1):

				if ("Round" in history[i]): return False
				#parsing issue
				if re.match ("bet*", history[i][0]) or ("raise" in history[i]) or ("call" in history[i]):return True
			return False

	def chipAmount(self):
		return self.chips
