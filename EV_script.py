from numpy import *
from card import *

cards = []

for x in range(0,52):
	cards.append(Card(x))

# --7-card hand rank--
# take two cards in hand
# or 
# take 3 cards on flop plus in hand, etc.

# roll out remaining cards and calc odds of winning


# card 0, 1 = hand
# give x cards, find best hand
# compare against best hand found for each random combination
def hand_rank_7(cards[]):
	wins = 0
	evaluated = 0
	private = [cards[0], cards[1]]
	public = np.setdiff1d(cards[], private)
