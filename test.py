from no_bluff_player import *
from card import *

# test file

nb_player = NoBluffPlayer()

#check pairs
c2 = Card(0)
d2 = Card(13)

ca = Card(12)
da = Card(25)

c9 = Card(7)
d9 = Card(13+7)

#check don't fold on pair of twos
nb_player.setHand(c2, d2)

print("checking pairs")
if nb_player.checkFoldPreFlop():
	raise AssertionError()
print("pair of twos is good")

nb_player.setHand(c2, c9)
assert nb_player.checkFoldPreFlop()

nb_player.setHand(c2, d9)
assert nb_player.checkFoldPreFlop()

print("passes all NoBluffPlayer.checkFoldPreFlop() tests")
#---passes all NoBluffPlayer.checkFoldPreFlop() tests---#
