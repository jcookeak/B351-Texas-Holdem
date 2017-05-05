import math
import random
from deck import *
from card import *
from hand_classification.texas_holdem_hand import *

class Game():
    def __init__(self, players, chips):
        self.allPlayers = players[:]
        self.history = []
        self.deck = Deck()
        self.current_bet = 0
        self.maxBet = chips
        self.table = []
        self.pot = 0
        self.playerChips =  {}
        self.call = []
        for player in self.allPlayers:
            player.setChips(chips)
            self.playerChips[player.getName()] = chips
            player.setActiveGame(self)
            player.setHistory(self.history)
            self.history.append([player.getName()+" added"])

    def playGame(self):
        #print("play game")
        self.deck.shuffleDeck()
        while len(self.allPlayers)>1:
            self.playHand()#continue to play until only one player is left

    def playHand(self):
        #print("playe hand")
        self.newHand()#tetative

        self.roundOfBetting()#pre-flop
        if (not self.checkHandEnd()):#if players still in game
            self.table.append(self.deck.getCard())
            self.table.append(self.deck.getCard())
            self.table.append(self.deck.getCard())
            self.roundOfBetting()#post-flop
            if (not self.checkHandEnd()):
                self.table.append(self.deck.getCard())
                self.roundOfBetting()#post turn
                if (not self.checkHandEnd()):
                    self.table.append(self.deck.getCard())
                    self.roundOfBetting()#post river
        #end of hand
        self.resolveHand()
        self.updatePlayers()
        self.rotatePlayers()

    def newHand(self):
        #print("new hand")
        self.history.append(["Starting new hand"])
        self.table = []#reset table
        self.deck.shuffleDeck()
        self.players = self.allPlayers[:]
        for player in self.players:
            self.pot+=player.collectAnti(1)
            self.playerChips[player.getName()]-=1
            player.resetFlag()
            player.setHand(self.deck.getCard(), self.deck.getCard())
    
    def roundOfBetting(self):
        #print("round of betting")
        for p in self.allPlayers:
            p.chips = self.playerChips[p.getName()]
        haveBet = False
        bettingRound = 0
        self.history.append(["Round"])
        self.getMaxBet()#maximum bet ammount for round
        self.resetCalls()#players should all have 0 call ammounts
        while bettingRound<2:
            if self.checkHandEnd():return
            if bettingRound != 0 and self.needToCall():#call round
                self.history.append(["Call Round", self.current_bet])
                for player in self.players:
                    if self.checkHandEnd(): return
                    if self.getCallAmmount(player) >0:#player has to call
                        [move, bet] = player.action(self.maxBet)
                        #print(move, bet, player.getName())
                        self.history.append([move, bet])
                        if move == "call" and self.getCallAmmount(player) == bet:
                            self.pot+=bet
                            self.call[player.getName()] = 0
                            self.playerChips[player.getName()]-=bet
                        else:#move is fold or not valid
                            self.fold(player, bet)
            else:
                for player in self.players:
                    if self.checkHandEnd():return
                    currentAction = player.action(self.maxBet)
                    [move, bet] = player.action(self.maxBet)
                    #print(move, bet, player.getName())
                    self.history.append([player.getName(), move, bet])
                    if move=="bet":
                        if bet>self.maxBet:
                            print("forced fold", player.getName())
                            self.fold(player, bet)
                        else:
                            haveBet = True
                            self.pot+=bet
                            self.playerChips[player.getName()]-=bet
                            self.call[player.getName()] = 0
                            self.adjustCalls(bet, player)
                            self.maxBet-=bet
                    elif move == "raise":
                        #call = self.getCallAmmount(player)
                        if self.maxBet<bet or haveBet==False: self.fold(player, bet)
                        else:
                            self.pot+= (bet+self.call[player.getName()])
                            self.playerChips[player.getName()]-=(bet+self.call[player.getName()])
                            self.call[player.getName()] = 0
                            self.adjustCalls(bet, player)
                            self.maxBet-=bet
                    elif move == "check":
                        if haveBet:
                            print("forced fold", player.getName())
                            self.fold(player, bet)
                    elif move == "call":
                        if (haveBet == False) or bet!=self.getCallAmmount(player):
                            print("forced fold", player.getName())
                            fold(player, bet)
                        else:
                            self.pot+=bet
                            self.playerChips[player.getName()] -=bet
                            self.call[player.getName()] = 0
                    else:#move is fold or not valid
                        self.fold(player, bet)
            bettingRound +=1
    def resolveHand(self):
        #print("resolve hand")
        if len(self.players)<1:
            self.history.append(["Error: No Winner"])
        elif len(self.players)>1:
            endPlayers = sorted(self.players, key=lambda x: Hand(x.getBestHand()).hand_val())
            winners, i, j = endPlayers[:1], 0, 1
            while j<len(endPlayers) and endPlayers[i] == endPlayers[j]:
                winners.append(endPlayers[j])
                i, j = j, j+1
            payout = math.floor(self.pot/len(winners))
            for p in winners:
                p.chips+=payout
                self.playerChips[p.getName()]+=payout
                self.history.append(["Winner: "+p.getName()])
            self.pot = self.pot%payout
        else:
            self.playerChips[self.players[0].getName()]+=self.pot
            self.players[0].chips+=self.pot
            self.pot = 0
            self.history.append(["Winner: "+self.players[0].getName()])
        self.history.append(["End of Hand"])
            
    def fold(self, player, bet):
        #print("fold function")
        self.players.remove(player)
        player.chips+=bet
        self.history.pop()
        self.history.append([player.getName(), "fold", 0])
        self.call[player.getName()] = 0
    def getMaxBet(self):
        self.maxBet =  self.playerChips[self.players[0].getName()]
        for p in self.players:
            if self.playerChips[p.getName()] < self.maxBet: self.maxBet = self.playerChips[p.getName()]
        return self.maxBet
    def getCallAmmount(self, player):
        #print("get call ammount")
        return self.call[player.getName()]
    def adjustCalls(self, bet, player):
        #print("adjust calls")
        for p in self.players:
            if p.getName()!=player.getName():
                self.call[p.getName()]+=bet
    def resetCalls(self):
        #print("reset calls")
        self.call = {}
        for player in self.players:
            self.call[player.getName()] = 0
    def needToCall(self):
        #print("need to call")
        for p in self.players:
            if self.getCallAmmount(p)>0:return True
        return False
    def rotatePlayers(self):
        #print("rottate players")
        temp = self.allPlayers[0]
        self.allPlayers.pop(0)
        self.allPlayers.append(temp)
    def getHistory(self):
        #print("get history")
        return self.history
    def checkHandEnd(self):
        #print("check end")
        return len(self.players) <=1
    def updatePlayers(self):
        #print("uppdate players")
        for p in self.allPlayers:
            if self.playerChips[p.getName()]<1:
                self.allPlayers.remove(p)
                if p in self.players: self.players.remove(p)
    def callAmount(self, player):
        return self.getCallAmmount(player)
