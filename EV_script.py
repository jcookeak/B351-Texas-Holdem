import numpy as np
import itertools as it
from card import *
from hand_classification.texas_holdem_hand import *

full_deck = []
deck = []

# only need to consider cards in range 0-12 and pairs

for x in range (0,52):
        full_deck.append(Card(x))

deck = full_deck[0:27]

#print(str(deck[25]))
        # --7-card hand rank--
        # take two cards in hand
        # or
        # take 3 cards on flop plus in hand, etc.

        # roll out remaining cards and calc odds of winning


        # card 0, 1 = hand
        # give x cards, find best hand
        # compare against best hand found for each random combination
def hand_rank_7(cards):
        wins = 0
        evaluated = 0
        cards = np.asarray(cards)
        private = np.asarray([cards[0], cards[1]])
        #print(cards.sort())
        public = np.setdiff1d(cards, private)
        pool = np.setdiff1d(np.asarray(full_deck), cards)
        # go through all combinations of cards not in inital set
        #cards to add
        add_num = 5 - public.size
        fill_cards = list(it.combinations(np.unique(pool),add_num))
        #print(np.append(private,public))
        l = []
        temp = np.append(private,public).tolist()
        for x in temp:
                l.append(x.val)
        hand = Hand(l)
        #print (hand.hand_val())
        set_max = 0
        for x in fill_cards:
                # find best player hand
                player_temp = np.append(temp,np.asarray(x))
                #print("player temp" + str(player_temp))
                player_comb = it.combinations(np.unique(player_temp), 5)
                #print(list(player_comb))
                pmax = 0
                winning_hand = []
                for y in player_comb:
                        t_hand = []
                        for p in y:
                                t_hand.append(p.val)
                        #print(str(len(t_hand)))
                        eval_hand = Hand(t_hand)
                        #print(eval_hand)
                        if eval_hand.hand_val() > pmax:
                                   pmax = eval_hand.hand_val()
                                   winning_hand = y

                #find best opponent hand
                opponent_comb = it.combinations(np.unique(np.asarray(x)), 5)
                o_max = 0
                o_win = []
                for y in opponent_comb:
                        t_hand = []
                        for p in y:
                                t_hand.append(p.val)
                        eval_hand = Hand(t_hand)
                        if eval_hand.hand_val() > o_max:
                                o_max = eval_hand.hand_val()
                                o_win = y

                #see if player beats opponent and record result
                if pmax > o_max:
                        wins += 1
                evaluated += 1
                #print(evaluated)
        #print(wins)
        #print("eval: ")
        #print(evaluated)
        #print("done?")
        print("EV: " + str(wins/evaluated))

#print(Hand([0,13,2,3,4]).hand_val())

card_combos = it.combinations(np.unique(np.asarray(deck)), 2)
for x in card_combos:
        print("evaluating starting hand: " + str(x))
        hand_rank_7([x[0], x[1]])
