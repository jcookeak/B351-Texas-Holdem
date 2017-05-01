# no bluff player

"""
Last modified: 4/20/17
Last modified by: Anna

Things to fix:
searching history
check bet ammount for legality
"""


from player import *
from hand_classification.texas_holdem_hand import *
import random

class NoBluffPlayer(Player):
        def __init__(self, history = [], chips=0, af=0):
                Player.__init__(self)
                self.agression_factor = af#work with this later
                self.chips = chips#add initial chip set option
                self.current_bet = 0#keep track of how much agent has in the pot
                self.round= 0
                self.history = history
                self.bestHand =[]

                #keep track of private vs public cards?

        # TODO
        # -- take into account aggression factor (reduce threshold by ~1)


        #fundction that determines if agent should fold initially


        def getBestHand(self):
            return self.bestHand

        def setHistory(self, history):
                self.history = history

        def checkFoldPreFlop(self): #false - don't fold | true - fold
                self.checkHand = Hand(self.handToValue())
                self.suitFlag = self.checkHand.flush()
                self.suitedThreshold = {12: 0, 11: 0, 10: 5, 9: 5, 8: 5, 7: 5, 6: 4, 5: 13, 4:13, 3:13, 2:13, 1:13, 0:13}
                self.unsuitedThreshold = {12:7, 11:7, 10:7, 9:6, 8:6, 7:6, 6:4, 5:13, 4:13, 3:13, 2:13, 1:13, 0:13 }
                # pre flop check
                # check for pairs
                if len(self.checkHand.pairs()[0]) == 0:
                        self.temp = self.checkHand.sortByValue(self.handToValue())
                        if self.temp[1]%13 > 6:
                                if self.suitFlag:#check if suit matches
                                        if self.temp[0]%13 > self.suitedThreshold[self.temp[0]%13]:#matching suit
                                                return False #good starting hand, don't fold
                                        else:
                                                return True #bad starting and, agent should fold
                                else:
                                        if self.temp[0]%13 > self.unsuitedThreshold[self.temp[0]%13]:#non-matching suiit
                                                return False #good starting hand, don't fold
                                        else:
                                                return True #bad starting and, agent should fold
                        else:
                                return True #bad starting and, agent should fold
                else:
                        return False #have a pair in opening hand (don't fold)


        def action(self, maxbet):
                print(self.round)
                # pre flop check
                isCallRound = self.callRound(self.history)
                if isCallRound:
                    return self.callRoundAction(isCallRound)
                self.checkHand = Hand(self.handToValue())
                self.temp = self.checkHand.sortByValue(self.handToValue())
                self.bestHand = self.checkHand.best_hand()
                """
                if self.round==0 and self.checkFoldPreFlop():#should probably only check this at the begining of a hand
                        return (["fold"])
                """

                #for now, bet the maximum:
                current_bet = maxbet


                # didn't fold before flop so need to check or call
                moves = self.legal_moves(self.history)#get possible moves
                if self.round == 0:# don't want to bet first round
                        if "bet" in moves: moves.remove("bet")
                        if "raise" in moves: moves.remove("raise")

                self.round +=1#number after 1 doesn't matter; just need to differentiate the pre-flop
                #randomly choose for now
                num = random.randrange(len(moves))
                move = list(moves)[num]

                print(move)

                #if move == "fold": self.round = 0
                if move == "call" or move =="check": return [move, self.game.callAmount(self)]
                if move == "raise" or move =="bet": #bet randomly for now
                        if maxbet>1:bet = random.randrange(1, maxbet+1)
                        else: bet = maxbet
                        self.chips -= bet + self.game.callAmount(self)
                        self.betFlag = 1
                        return [move, maxbet]

                return [move, 0]



        def callRoundAction(self, needBet):
            moves = ["call", "fold"]
            num = random.randrange(len(moves))
            move = moves[num]
            if move == "call":
                bet = needBet - self.current_bet
                return ["call", bet]
            return ["fold", 0]


        def legal_moves(self, history):
                if self.haveBet(history): moves = set(["call"])#bet has occured
                else: moves= set(["check"])#bet has not occured
                if not self.betFlag:
                        if "check" in moves: moves.add("bet")
                        else: moves.add("raise")
                if self.chips: moves.add("fold")#check for all in, don't fold if no chips are left
                return moves

        def haveBet(self, history):#TODO: check for hand end, check for round end
                for i in range(-1, -1*len(history), -1):
                    if ("Round" in history[i]):
                        break
                    if ("bet" in history[i]) or ("raise" in history[i]) or ("call" in history[i]):return True
                return False

        def callRound(self, history):
            for i in range(-1, -1*len(history), -1):
                if ("Round" in history[i]):
                    break
                if ("Call Round" in history[i]):
                    needBet = history[i][1]
                    return needBet
                return False
