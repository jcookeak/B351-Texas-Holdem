# no bluff player

"""
Last modified: 5/2/17
Last modified by: Anna

Things to fix:
searching history
check bet ammount for legality
"""


from player import *
from hand_classification.texas_holdem_hand import *
import random
import re
from EV_script import *

class NoBluffPlayer(Player):
        def __init__(self, history = [], chips=0, af=0, verbose = False):
                Player.__init__(self)
                self.verbose = verbose
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
                #print(self.round)#for testing
                # pre flop check
                isCallRound = self.callRound(self.history)
                if isCallRound:
                    return self.callRoundAction(isCallRound)
                self.checkHand = Hand(self.handToValue())
                self.temp = self.checkHand.sortByValue(self.handToValue())
                self.bestHand = self.checkHand.best_hand()
                
                if self.round==0 and self.checkFoldPreFlop():#should probably only check this at the begining of a hand
                        return (["fold"])
                

                #for now, bet the maximum:
                #current_bet = maxbet

                #betting strategy, go for a check unless we like our hand.

                # didn't fold before flop so need to check or call
                moves = self.legal_moves(self.history, maxbet)#get possible moves
                if self.round == 0:# don't want to bet first round
                        if "bet" in moves: moves.remove("bet")
                        if "raise" in moves: moves.remove("raise")

                self.round +=1#number after 1 doesn't matter; just need to differentiate the pre-flop
                #randomly choose for now
                num = random.randrange(len(moves))
                move = list(moves)[num]
                if self.verbose: print(str(self.name) + " moves: " + str(moves))

                if "raise" in moves:
                        return self.callRoundAction(self.callAmount(self.history))

                if (self.betFlag == 0 and "bet" in moves):
                        field_cards = []
                        for x in self.game.field:
                                field_cards.append(x.val)
                        check_hand = Hand([self.hand[0].val, self.hand[1].val], field_cards)
                        if check_hand.better_hand_check([True,"straight_flush"], check_hand.is_hand()):
                                        # we have a royal flush so let's bet higher.
                                self.chips -= maxbet
                                self.betFlag = 1
                                return ["bet", maxbet]
                        elif check_hand.better_hand_check([True,"four"], check_hand.is_hand()):
                                val =  math.floor(min(maxbet, (.3 * self.chips)))

                                self.chips -= val
                                self.betFlag = 1
                                return ["bet", val]
                        elif check_hand.better_hand_check([True,"full"], check_hand.is_hand()):
                                val =  math.floor(min(maxbet, (.2 * self.chips)))
                                self.chips -= val
                                self.betFlag = 1
                                return ["bet", val]
                        elif check_hand.better_hand_check([True,"flush"], check_hand.is_hand()):
                                val =  math.floor(min(maxbet, (.1 * self.chips)))
                                self.chips -= val
                                self.betFlag = 1
                                return ["bet", val]
                        elif check_hand.better_hand_check([True,"straight"], check_hand.is_hand()):
                                val =  math.floor(min(maxbet, (0.08 * self.chips)))
                                self.chips -= val
                                self.betFlag = 1
                                return ["bet", val]
                        elif check_hand.better_hand_check([True,"three"], check_hand.is_hand()):
                                val =  math.floor(min(maxbet, (.05 * self.chips)))
                                self.chips -= val
                                self.betFlag = 1
                                return ["bet", val]
                        else: return ["check", 0]

                return ["check", 0]


                

                #print(move)#for testing

                # #if move == "fold": self.round = 0
                # if move == "call": self.chips-=self.game.callAmount(self)
                # if move == "call" or move =="check": return [move, self.game.callAmount(self)]
                # if move == "raise" or move =="bet": #bet randomly for now
                #         if maxbet>1:bet = random.randrange(1, maxbet+1)
                #         else: bet = maxbet
                #         self.chips -= bet + self.game.callAmount(self)
                #         self.betFlag = 1
                #         return [move, bet]

                # return [move, 0]



        def callRoundAction(self, needBet):
                if (self.round == 0):
                        if needBet/self.chips >= (0.1 * self.preflop_call_percent()):
                                bet = self.game.callAmount(self)#current_bet is not reliable
                                #needBet - self.current_bet
                                self.chips -= bet#subtract bet from chips
                                return ["call", bet]
                        else:
                                return ["fold", 0]
                else:
                        field_cards = []
                        for x in self.game.field:
                                field_cards.append(x.val)
                        check_hand = Hand([self.hand[0].val, self.hand[1].val], field_cards)
                        if check_hand.better_hand_check([True,"straight_flush"], check_hand.is_hand()):
                                if (self.game.pot/needBet) >=  0:
                                        bet = self.game.callAmount(self)
                                        self.chips -= bet
                                        return ["call", bet]
                                else:
                                        return ["fold", 0]
                        elif check_hand.better_hand_check([True,"four"], check_hand.is_hand()):
                                if (self.game.pot/needBet) >=  1:
                                        bet = self.game.callAmount(self)
                                        self.chips -= bet
                                        return ["call", bet]
                                else:
                                        return ["fold", 0]
                        elif check_hand.better_hand_check([True,"full"], check_hand.is_hand()):
                                if (self.game.pot/needBet) >=  2:
                                        bet = self.game.callAmount(self)
                                        self.chips -= bet
                                        return ["call", bet]
                                else:
                                        return ["fold", 0]
                        elif check_hand.better_hand_check([True,"flush"], check_hand.is_hand()):
                                if (self.game.pot/needBet) >=  2:
                                        bet = self.game.callAmount(self)
                                        self.chips -= bet
                                        return ["call", bet]
                                else:
                                        return ["fold", 0]
                        elif check_hand.better_hand_check([True,"straight"], check_hand.is_hand()):
                                if (self.game.pot/needBet) >=  3:
                                        bet = self.game.callAmount(self)
                                        self.chips -= bet
                                        return ["call", bet]
                                else:
                                        return ["fold", 0]
                        # elif check_hand.better_hand_check([True,"three"], check_hand.is_hand()):
                        #         if (needBet/self.game.pot) >=  6:
                        #                 bet = self.game.callAmount(self)
                        #                 self.chips -= bet
                        #                 return ["call", bet]
                        #         else:
                        #                 return ["fold", 0]

                        elif (self.game.pot/needBet >= (better_hand_outs(self.hand + self.game.field)[0] - 1)):
                                bet = self.game.callAmount(self)#current_bet is not reliable
                                #needBet - self.current_bet
                                self.chips -= bet#subtract bet from chips
                                return ["call", bet]
                return ["fold", 0]

        def preflop_call_percent(self):
                c1 = self.hand[0].val % 13
                c2 = self.hand[1].val % 13 #val
                suit_flag = False
                if (abs(self.hand[0].val - self.hand[1].val) <= 13):
                        suit_flag = True
                pairs = {0:11, 1:11, 2:11, 3: 12, 4:13, 5:13, 6: 15, 7: 16, 8:19, 9:22, 10:27, 11:32, 12:40}
                suited = {1:[7],2:[7,8],3:[8,9,10],4:[6,8,10,11],5:[6,7,9,10,11],
                6:[6,6,8,9,11,12],7:[7,7,7,8,10,12,13], 8:[8,8,8,8,10,11,13,15],9:[8,9,9,9,9,11,13,15,18],
                10:[9,10,10,10,11,11,13,15,18,19], 11:[11,11,11,12,12,13,13,15,18,20,21],
                12:[13,14,14,15,14,14,15,16,19,20,22,24]}
                unsuited = {1:[1], 2:[2,3],3:[2,4,5], 4:[1,3,4,6], 5:[0,1,1,3,5,6],
                6:[0,1,2,4,5,7],7:[1,1,1,3,4,6,8],8:[2,2,2,2,4,6,8,10],
                9:[2,2,3,3,3,5,7,9,13], 10:[3,3,4,4,4,5,7,9,12,14],11:[4,5,5,5,6,6,7,9,13,14,16],
                12:[7,7,8,8,7,8,9,10,13,14,16,19]}

                if (c2 > c1):
                        tempc = c1
                        c1 = c2
                        c2 = tempc

                if (c1 == c2):
                        return pairs[c1]

                if (suit_flag):
                        return suited[c1][c2]
                else:
                        return unsuited[c1][c2]

        def callRound(self, history):
                for i in range(-1, -1*len(history), -1):
                        if ("Round" in history[i]):
                                break
                        if ("Call Round" in history[i]):
                                needBet = history[i][1]
                                return needBet
                return False
