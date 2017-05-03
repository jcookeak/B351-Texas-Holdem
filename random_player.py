# no bluff player

"""
Last modified: 5/1/17
Last modified by: Anna

What this file does:
simulates a poker player
chooses random action (call/check, raise/bet, fold)
chooses random bet ammount

Things to fix:
random betting
"""


from player import *
from hand_classification.texas_holdem_hand import *
import random

class RandomPlayer(Player):
        def __init__(self, history = [], chips=0, af=0, verbose = False):
                Player.__init__(self)
                self.verbose = verbose
                self.agression_factor = af#work with this later
                self.chips = chips#add initial chip set option
                self.current_bet = 0#keep track of how much agent has in the pot
                self.history = history
                self.bestHand =[]#the best hand that the player has

        def getBestHand(self):
            return self.bestHand

        def setHistory(self, history):
                self.history = history

        def action(self, maxbet):
                if(self.verbose): print(self.round)
                # pre flop check
                isCallRound = self.callRound(self.history)
                if isCallRound:
                    return self.callRoundAction(isCallRound)
                self.checkHand = Hand(self.handToValue())
                self.temp = self.checkHand.sortByValue(self.handToValue())
                self.bestHand = self.checkHand.best_hand()
                #bet random ammount if possible
                moves = self.legal_moves(self.history, maxbet)#get possible moves


                # didn't fold before flop so need to check or call


                if self.verbose: print(str(self.name) + " moves: " + str(moves))
                self.round +=1#number after 1 doesn't matter; just need to differentiate the pre-flop
                #randomly choose for now
                num = random.randrange(len(moves))
                move = list(moves)[num]

                #print(move)

                #if move == "fold": self.round = 0
                if move =="check":
                    return [move, 0]
                if move == "call":
                    self.chips -= self.game.callAmount(self)
                    return [move, self.game.callAmount(self)]
                if move == "raise" or move =="bet": #bet randomly for now
                        if maxbet>1:bet = random.randrange(maxbet)+1
                        else: bet = maxbet
                        #print ("bet", bet)
                        self.chips -= bet + self.game.callAmount(self)
                        self.betFlag = 1
                        return [move, bet]

                return [move, 0]


        #this function is called if a player needs to call a bet to stay in the hand
        def callRoundAction(self, needBet):
            moves = ["call"]#, "fold"]
            num = random.randrange(len(moves))
            move = moves[num]
            if move == "call":
                bet = self.game.callAmount(self)
                #bet = needBet - self.current_bet
                self.chips -= bet
                return ["call", bet]
            return ["fold", 0]

        def callRound(self, history):
            for i in range(-1, -1*len(history), -1):
                if ("Round" in history[i]):
                    break
                if ("Call Round" in history[i]):
                    needBet = history[i][1]
                    return needBet
                return False
