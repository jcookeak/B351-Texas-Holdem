import math
import re
import random

from player import *
from human import *
from no_bluff_player import *
from card import *

# Texas Hold'em Game Controller

#Init game
#Anti for Hand
#Deal Two Cards to each player
#--Turn Order--
	# Bet
	# flip 3
	#bet
	#deal 1 card
	#bet
	#deal 1 card
	#bet
	#resolve

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
face = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]	

class Deck(object):
	def __init__(self):
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
		return self.deck.pop()

	def shuffleDeck(self):
		random.shuffle(self.deck)

	# def deal(self, n):
	# 	for x in range(0,n):



class Game(object):
	def __init__(self, players, chips):
		self.totalChips = chips * len(players)
		self.history = [["initialized game"]]
		self.history.append(["set chip ammount to " + str(chips)])
		self.deck = Deck()
		self.field = []
		self.pot = 0
		self.call = {}
		self.allPlayers = players
		self.players = players
		for player in self.players:
			player.setChips(chips)
			player.setActiveGame(self)
			self.history.append([player.getName() + " added"])
		
	def __str__(self):
		self.string = ""
		for player in self.players:
			self.string = self.string + "--" + (player.getName()) + "--\n"
			self.string = self.string + "chips: " + str(player.chipAmount()) + "\n"
			self.string = self.string + "hand: " + str(player.getHand()[0]) + ", " + str(player.getHand()[1]) + "\n"
		self.string = self.string + ("--Game state--\n")
		self.string = self.string + "current pot: " + str(self.pot) + "\n"
		self.string = self.string + "field: "
		for x in self.field:
			self.string = self.string + "|" + str(x) + "| "
		self.string = self.string + "\n"

		return self.string

	def revealedCards(self):
		return self.field

	def startGame(self):
		while len(self.players) > 0:
			#self.newHand()
			self.playHand()

	def newHand(self):
		self.history.append(["starting new hand"])
		self.field = []
		self.players = self.allPlayers
		for player in self.players:
			player.resetFlag()
			player.setHand(self.deck.getCard(),self.deck.getCard())
			self.history.append(["dealt two cards", player.getName()])

	def playHand(self):
		#pay anti
		for player in self.players:
			self.pot += player.collectAnti(1)

		self.newHand() # deal cards
		self.roundOfBetting() #pre-flop betting
		self.field.append(self.deck.getCard()) #flop
		self.field.append(self.deck.getCard())
		self.field.append(self.deck.getCard())
		self.roundOfBetting() #post flop betting
		self.field.append(self.deck.getCard()) #turn
		self.roundOfBetting() #post turn betting
		self.field.append(self.deck.getCard()) #river
		self.roundOfBetting() #post river betting
		
		self.resolveHand()
		print(self)

	def getMaxBet(self):
		self.maxbet = self.totalChips
		for player in players:
			if player.chipAmount() < self.maxbet:
				self.maxbet = player.chipAmount()
		return self.maxbet

	def roundOfBetting(self):
		print(self)

		self.round = 0

		self.getMaxBet()
		for x in players:
			self.call[x.getName()] = 0
		while self.round < 3:
			if self.needToCall() == False and self.round == 0:
				for player in players:
					print("getting action for " + player.getName())
					self.currentAction = player.action(self.maxbet)
					if self.currentAction[0] == "bet":
						self.history.append(["bet " + str(self.currentAction[1]), player.getName()])
						for x in players:
							self.call[x.getName()] += self.currentAction[1]
						self.call[player.getName()] = 0
						self.maxbet -= self.currentAction[1]
						self.pot += self.currentAction[1]
					elif self.currentAction[0] == "raise":
						self.history.append(["raise " + str(self.currentAction[1]), player.getName()])
						for x in players:
							if x != player:
								self.call[x.getName()] += self.currentAction[1]
						self.maxbet = self.getMaxBet()
						self.pot += self.call[player.getName()] + self.currentAction[1]
						self.call[player.getName()] = 0
					elif self.currentAction[0] == "call":
						self.history.append(["call", player.getName()])
						self.pot += self.call[player.getName()]
						self.call[player.getName()] = 0
					elif self.currentAction[0] == "check":
						self.history.append(["check", player.getName()])
					elif self.currentAction[0] == "fold":
						self.players.remove(player)
						self.history.append(["fold", player.getName()])
			# elif self.needToCall == False:
			# 	break
			# 	# print(self)
			else: #players must call
				for player in players:
					if self.call[player.getName()] > 0:
						print("call or fold")
						self.currentAction = player.action(self.maxbet)
						if self.currentAction[0] == "call":
							self.history.append(["call", player.getName()])
							self.pot += self.call[player.getName()]
							self.call[player.getName()] = 0
						else:
							self.players.remove(player)
							self.history.append(["fold", player.getName()])
							del self.call[player.getName()]
			self.round += 1

	def needToCall(self):
		for x in self.players:
			if self.call[x.getName()] > 0:
				return True
		return False

	def callAmount(self, player):
		return self.call[player.getName()]

	def resolveHand(self):
		# payout pot to top player(s)
		return -1

	def getHistory(self):
		return self.history

c0 = Card(0)
c11 = Card(11)
c12 = Card(12)
c13 = Card(13)
c50 = Card(50)

deck = Deck()
print(deck)
#print deck.getCard()

# p0 = Player()
# p0.setName("p0")
# p1 = Player()
# p1.setName("p1")
# p2 = Player()
# p2.setName("p2")

p0 = HumanPlayer()
p0.setName("p0")
p1 = HumanPlayer()
p1.setName("p1")
p2 = HumanPlayer()
p2.setName("p2")
players = [p0,p1,p2]
game = Game(players, 200)

print(game)
game.startGame()
print(game)
for x in game.getHistory():
	print(x)
# while(p.chipAmount() > 0):
# 	p.action(p.chipAmount())

# print(c0)
# print(c11)
# print(c12)
# print(c13)
# print(c50)
