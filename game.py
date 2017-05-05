
"""
Game.py

Last modified: 5/4/17
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

#from player import *
#from human import *
#from no_bluff_player import *
from card import *
#from random_player import *
#from EV_script import *
from deck import *
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
                self.winner = None
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
                while len(self.allPlayers) > 1:
                        self.playHand()
                if len(self.allPlayers)==1: self.winnner = self.allPlayers[0]


        def newHand(self):#set up a new game hand
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

        def playHand(self):#simulates a hand of poker
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

        def getMaxBet(self):#returns the maximum bet a player can make
            self.maxbet = self.totalChips
            for player in self.players:
                if player.chipAmount() < self.maxbet:
                    self.maxbet = player.chipAmount()
            return self.maxbet

        def updatePlayers(self):# check for and remove players with no chips
                for p in self.allPlayers:
                        #print(p.getName())
                        # if p.chips > (chip_amount * (len(players_list) + 1)):
                        #     print("player: " + p.name + " chips: " + str(p.chips))
                        #     raise ValueError("player chips exceed total amount")
                        if p.chips < 1:
                            self.history.append(["Player out " + p.getName()])
                            self.allPlayers.remove(p)
                            if p in self.players: self.players.remove(p)

        def checkEndHand(self):
            if len(self.players)<2:return True
            return False

        def roundOfBetting(self):
                if(self.verbose): print(self)
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
                                                        self.maxbet -= self.currentAction[1]
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

        def needToCall(self):#boolean indication that a player must call to stay in the game
                for x in self.players:
                        if self.call[x.getName()] > 0:
                                return True
                return False

        def callAmount(self, player):#ammount a given player must call to stay in the game
                return self.call[player.getName()]

        def resolveHand(self):#decide hand winner and poyout/reset pot
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

        def getHistory(self):#returns array of game history
                return self.history

        def rotatePlayers(self):#rotates player order
            temp = self.allPlayers[0]
            self.allPlayers.pop(0)
            self.allPlayers.append(temp)
