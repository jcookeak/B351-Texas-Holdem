from game import *
from no_bluff_player import *
from random_player import *

#from new_player import *

p0 = RandomPlayer()#HumanPlayer()
p0.setName("p0")
p1 = NoBluffPlayer()#HumanPlayer()
p1.setName("p1")
p2 = RandomPlayer()
p2.setName("p2")
p3 = NoBluffPlayer()#RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p3.setName("p3")
p4 = RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p4.setName("p3")

count = 0
while (count < 50):
    players_list = [p0,p1,p2]#,p3,p4]
    chip_amount = 50
    game = Game(players_list, chip_amount)#, True)
    game.startGame()
    print("players: " + str(game.players[0].name) + ", chips: " + str(game.players[0].chips))
    count+=1
