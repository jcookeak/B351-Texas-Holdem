# no bluff player

from player import *
from hand_classification.texas_holdem_hand import *

class NoBluffPlayer(Player):

	# TODO
	# -- take into account aggression factor (reduce threshold by ~1)

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
				if self.suitFlag:
					if self.temp[0]%13 > self.suitedThreshold[self.temp[0]%13]:
						return False
					else:
						return True
				else:
					if self.temp[0]%13 > self.unsuitedThreshold[self.temp[0]%13]:
						return False
					else:
						return True
			else:
				return True
		else:
			return False #have a pair in opening hand


	def action(self, maxbet):
		# pre flop check
		self.checkHand = Hand(self.handToValue())
		self.temp = self.checkHand.sortByValue(self.handToValue())
		if self.checkFoldPreFlop:
			return (["fold"])

		# don't want to bet first round
		# didn't fold before flop so need to check or call

