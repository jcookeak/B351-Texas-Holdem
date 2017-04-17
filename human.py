from player import *

class HumanPlayer(Player):
	def action(self, maxbet):

		print("your hand is " + str(self.hand[0]) + " & " + str(self.hand[1]))
		print("max bet is " + str(maxbet))
		print("--Options--")
		print("1. bet")
		print("2. call " + str(self.game.callAmount(self)) + " and raise")
		print("3. call: " + str(self.game.callAmount(self)))
		print("4. check")
		print("5. fold")

		self.input = input()
		if (self.input == 1):
			if(self.betFlag == 1):
				print("you have already bet this game.")
				return self.action(maxbet)
			print("input bet amount")
			self.input = input()
			while (int(self.input) > maxbet or int(self.input) <= 0):
				print("illegal bet, try again")
				self.input = input()
			self.chips -= int(self.input)
			self.betFlag = 1
			return (["bet", int(self.input)])

		elif (self.input == 2):
			if(self.betFlag == 1):
				print("you have already bet this game.")
				return self.action(maxbet)
			print("input raise amount (legal amount)" )
			self.input = input()
			while (int(self.input) > maxbet or int(self.input) <=0):
				print("illegal amount, try again")
				self.input = input()
			self.chips -= int(self.input) + self.game.callAmount(self)
			self.betFlag = 1
			return (["raise", int(self.input)])

		elif (self.input == 3):
			self.chips -= self.game.callAmount(self)
			return (["call", self.game.callAmount(self)])
		elif (self.input == 4):
			return(["check"])
		elif (self.input == 5):
			return(["fold"])
		else:
			print("unrecognized input: " + str(self.input))
			return self.action(maxbet)




