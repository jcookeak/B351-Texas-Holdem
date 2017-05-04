
"""
Game.py

Last modified: 5/2/17
Last modified by: Anna

What this file does:
runs a poker simulation
creates a list of poker players
calls cation on each player
finds winner

Current player types:
human
random
no bluff

"""

import math
import re
import random

from player import *
from human import *
from no_bluff_player import *
from card import *
from random_player import *
#from EV_script import *

from hand_classification.texas_holdem_hand import *


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

    # def deal(self, n):
    #   for x in range(0,n):



class Game(object):
        def __init__(self, players, chips, verbose = False):
                self.verbose = verbose
                self.gameRound = -1
                self.totalChips = chips * len(players)
                self.history = [["initialized game"]]
                self.history.append(["set chip ammount to " + str(chips)])
                self.deck = Deck()
                self.field = []
                self.pot = 0
                self.call = {}
                self.allPlayers = players[:]
                self.current_bet = 0
                for player in self.allPlayers:
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
                self.deck.shuffleDeck()
                for player in self.allPlayers:
                    player.setHistory(self.history)
                while len(self.allPlayers) > 1:#add check for winner
            #self.newHand()
                        self.playHand()

        def newHand(self):
                self.history.append(["starting new hand"])
                self.gameRound = -1
                self.field = []
                self.players = self.allPlayers[:]
                #collect anti from players
                self.updatePlayers()
                for player in self.players:
                        self.pot += player.collectAnti(1)

                self.deck.shuffleDeck()
                for player in self.players:
                        player.resetFlag()
                        player.setHand(self.deck.getCard(),self.deck.getCard())
                        self.history.append(["dealt two cards", player.getName()])

        def playHand(self):
                #pay anti
                self.newHand() # deal 2 cards
                self.roundOfBetting() #pre-flop betting
                if(not self.checkEndHand()):
                #add 3 public cards
                    self.field.append(self.deck.getCard()) #flop
                    self.field.append(self.deck.getCard())
                    self.field.append(self.deck.getCard())
                    self.roundOfBetting() #post flop betting
                if(not self.checkEndHand()):
                    self.field.append(self.deck.getCard()) #turn
                    self.roundOfBetting() #post turn betting
                if(not self.checkEndHand()):
                    self.field.append(self.deck.getCard()) #river
                    self.roundOfBetting() #post river betting
                self.resolveHand()
                self.updatePlayers()
                if(self.verbose): print(self)
                self.history.append(["Rotate Players"])
                self.rotatePlayers()

        def getMaxBet(self):
            self.maxbet = self.totalChips
            for player in self.players:
                if player.chipAmount() < self.maxbet:
                    self.maxbet = player.chipAmount()
            return self.maxbet

        def updatePlayers(self):
                for p in self.allPlayers:
                        #print(p.getName())
                        # if p.chips > (chip_amount * (len(players_list) + 1)):
                        #     print("player: " + p.name + " chips: " + str(p.chips))
                        #     raise ValueError("player chips exceed total amount")
                        if p.chips < 1:
                            #print(p.getName(), "removed")
                            self.history.append(["Player out " + p.getName()])
                            self.allPlayers.remove(p)
                            if p in self.players: self.players.remove(p)
                #print("second loop")

        def checkEndHand(self):
            if len(self.players)<2:return True
            return False

        def roundOfBetting(self):
                if(self.verbose): print(self)
                #self.updatePlayers()
                self.round = 0
                self.gameRound+=1
                self.history.append(["Round"])#round marker in history for checking bet vs raise

                self.getMaxBet()
                self.current_bet = 0
                for x in self.players:
                        self.call[x.getName()] = 0
                while self.round < 2:
                        if self.needToCall() == False and self.round == 0:
                                for player in self.players:
                                        if(self.verbose): print("getting action for " + player.getName())
                                        self.currentAction = player.action(self.maxbet)
                                        if(self.verbose): print("player action: " + self.currentAction[0])
                                        if self.currentAction[0] == "bet":
                                                self.history.append(["bet " + str(self.currentAction[1]), player.getName()])
                                                for x in self.players:
                                                        self.call[x.getName()] += self.currentAction[1]
                                                self.call[player.getName()] = 0
                                                self.maxbet -= self.currentAction[1]
                                                self.current_bet += self.currentAction[1]
                                                self.pot += self.currentAction[1]
                                        elif self.currentAction[0] == "raise":
                                                self.history.append(["raise " + str(self.currentAction[1]), player.getName()])
                                                for x in self.players:
                                                        if x != player:
                                                                self.call[x.getName()] += self.currentAction[1]
                                                        self.maxbet = self.getMaxBet()
                                                self.current_bet += self.currentAction[1]
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
                        #   break
                        #   # print(self)
                        else: #players must call
                                self.history.append(["Call Round", self.current_bet])
                                for player in self.players:
                                        if self.call[player.getName()] > 0:#check if any player needs to call
                                                if(self.verbose): print("call or fold")
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
            if len(self.players)<1:return
            elif len(self.players)>1:
                self.players =  sorted(self.players, key=lambda x: Hand(x.getBestHand()).hand_val())
                winners = []
                for x in self.players:
                    if Hand(self.players[0].getBestHand()).hand_val() == Hand(x.getBestHand()).hand_val():
                        winners.append(x)
                if len(winners)>1:
                    payout = math.floor(self.pot / len(winners))
                    if(self.verbose): print ("multiple winners ",len(winners), self.pot, payout, self.pot/len(winners))
                    self.history.append(["multiple winners, pot split"])
                    for x in winners:
                        x.chips += payout
                        self.history.append(["Winner: "+ x.getName()])
                    self.pot = self.pot % len(winners)
                    if(self.verbose): print("pot ", self.pot)
                    self.history.append(["End of Hand"])
                    return

            Winner = self.players[0]
            Winner.chips+=self.pot
            self.pot = 0
            self.history.append(["Winner: "+Winner.getName()])
            self.history.append(["End of Hand"])
            self.updatePlayers()

        def getHistory(self):
                return self.history

        def rotatePlayers(self):
            temp = self.allPlayers[0]
            self.allPlayers.pop(0)
            self.allPlayers.append(temp)


##########################################################

##########################################################
c0 = Card(0)
c11 = Card(11)
c12 = Card(12)
c13 = Card(13)
c50 = Card(50)

#deck = Deck()
#print(deck)
#print deck.getCard()

# p0 = Player()
# p0.setName("p0")
# p1 = Player()
# p1.setName("p1")
# p2 = Player()
# p2.setName("p2")

p0 = RandomPlayer()#HumanPlayer()
p0.setName("p0")
p1 = NoBluffPlayer()#HumanPlayer()
p1.setName("p1")
p2 = NoBluffPlayer()#HumanPlayer()RandomPlayer()
p2.setName("p2")
p3 = NoBluffPlayer()#RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p3.setName("p3")
p4 = RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p4.setName("p3")


count = 0
while (count < 50):
    players_list = [p0,p1,p2]#,p3,p4]
    chip_amount = 50
    game = Game(players_list, chip_amount)#, True)
    game.startGame()
    print("players: " + str(game.players[0].name) + ", chips: " + str(game.players[0].chips))
    count+=1


#print(game)
#print(game)
#for x in game.getHistory():
   #print(x)



#print("all players " + str(game.allPlayers))

# del game

# games_to_run = 5
# counter_games = 0
# player_wins = {p0:0, p1:0, p2:0}

# while counter_games < games_to_run:
#     #del running_game
#     running_game = Game(players_list,chip_amount)
#     running_game.startGame()
#     print(running_game)
#     print(counter_games)
#     print(str(running_game.players[0].hand))
#     if str(running_game.players[0].name) == "p0":
#         player_wins[p0] += 1
#     if str(running_game.players[0].name) == "p1":
#         player_wins[p1] += 1
#     if str(running_game.players[0].name) == "p2":
#         player_wins[p2] += 1
#     counter_games += 1
#     del running_game

# print("player p0 wins: " + str(player_wins[p0]))
# print("player p1 wins: " + str(player_wins[p1]))
# print("player p2 wins: " + str(player_wins[p2]))
# while(p.chipAmount() > 0):
#   p.action(p.chipAmount())

# print(c0)
# print(c11)
# print(c12)
# print(c13)
# print(c50)
