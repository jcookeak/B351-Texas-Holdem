from game_mechanics import *
from no_bluff_player import *
from bluff_player import *
from random_player import *

#from new_player import *

p0 = RandomPlayer()#HumanPlayer()
p0.setName("p0")
p1 = BluffPlayer()
p1.setName("p1")
p2 = RandomPlayer()
p2.setName("p2")
p3 = RandomPlayer()#RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p3.setName("p3")
p4 = RandomPlayer()#NoBluffPlayer()#HumanPlayer()
p4.setName("p4")

wins = {"p0":0, "p1":0, "p2":0, "p3":0, "p4":0}
count = 0
while (count < 10):
    players_list = [p0,p1,p2,p3,p4]#,p3,p4]
    chip_amount = 50
    game = Game(players_list, chip_amount)#, True)
    game.playGame()
    print("players: " + str(game.players[0].name) + ", chips: " + str(game.players[0].chips))
