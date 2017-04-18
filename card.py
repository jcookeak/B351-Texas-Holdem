# card.py

class Card(object):
	def __init__(self, card_val):
		self.val = card_val

	def __str__(self):
		self.string = str(face[self.val % 13]) + " of " + str(suits[int(math.floor(self.val / 13))])#+ str(suits[(self.val / 11) + 1])
		return self.string

	def toValue(self):
		return self.val