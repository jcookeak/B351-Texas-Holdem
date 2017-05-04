from game import *
from no_bluff_player import *
from random_player import *

while (True):
    cmd = input("Play poker? (y/n)")
    if  cmd =="n" or cmd =="q" or cmd =="exit" or cmd =="quite" or cmd =="no":
        break

    player_list = []
    num_players=0
    while (num_players<2) or (num_players>6):
        num_players = int(input ("Number of players in hand (2-6): "))

    for i in range (num_players):
        player_type = ""
        while True:
            player_type = input("Player Type (0=human, 1=randrom, 2=robot): ")
            if player_type =="0":
                p = HumanPlayer()
            if player_type =="1":
                p = RandomPlayer()
            if player_type =="2":
                p = NoBluffPlayer()
            p.setName("p"+str(i))
            player_list.append(p)
            if (player_type == "0") or (player_type == "1") or (player_type == "2"): break

    start_chips = 0
    while (start_chips<1) or (start_chips>1000):
        start_chips = int(input("Starting chip ammount per players(1-1000): "))

    game = Game(player_list, start_chips)
    game.startGame()
    print("players: " + str(game.players[0].name) + ", chips: " + str(game.players[0].chips))
