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

        #depth is how many soft outs we want to calculate from current state
def better_hand_outs(cards_known, checked_cards = [], threshold = [False, "high"]): 
    #print(depth)
    if (depth <= 0):
        return (0, set())
    outs = set()
    soft_outs = set()
    cards = np.asarray(cards_known)
    print("cards " + str(cards))
    private = np.asarray([cards[0], cards[1]])
    public = np.setdiff1d(cards, private)

    post_flop_outs = np.setdiff1d(np.asarray(full_deck), cards)
    #pool of available cards left in deck
    pool = np.setdiff1d(np.asarray(full_deck), cards)
    pool = np.setdiff1d(pool, np.asarray(checked_cards))
    fill_cards = list(it.combinations(np.unique(pool),1))

    print(fill_cards)
    known_cards = []
    for x in (np.append(private, public)):
        known_cards.append(x.val)
    print("best cards" + str(known_cards))
    best_hand = Hand(Hand(known_cards).best_hand()).is_hand()
    print(best_hand)
    if (len(cards_known) >= 5):
        combin_n = 4
    else:
        combin_n = len(cards_known)
    for x in fill_cards:
        for p in it.combinations(np.unique(np.append(private, public)), combin_n):
            print("p ", p)
            temp_pool = np.append(p, x)
            temp_check = []
            for x in temp_pool:
                temp_check.append(x.val)
            temp_hand = Hand(temp_check)
            if(temp_hand.better_hand_check(threshold, temp_hand.is_hand())):
                print("above threshold")
                if (temp_hand.better_hand_check(best_hand, temp_hand.is_hand())):     
                    print("new best found")
                    outs.add(x)
            # else:
            #     #print("recur depth: ", depth)
            #     print("cards know: " + str(cards_known) + " x: " + str([x]))
            #     temp_cards_list = cards_known + [x]
            #     #print(temp_cards_list)
            #     checked_cards = list(outs) + list(soft_outs)
            #     print(checked_cards)
            #     soft_outs.union(better_hand_outs(temp_cards_list, checked_cards, threshold, depth - 1)[1])

            # temp_cards = []
            # if (depth > 1):
            #     for x in temp_hand.cards:
            #         temp_cards.append(Card(x))
            #     print("temp+cards" + str(temp_cards))
            #     print(better_hand_outs(p, threshold, depth-1)[1])
    #print(best_hand)
    print(outs)
    print("soft_outs:"+ str(soft_outs))
    print("number of outs: " + str(len(outs)))
    print("number of cards in deck: " + str(len(fill_cards)))
    if (len(outs) == 0):
        return (0, outs)
    return (len(fill_cards)/len(outs), outs)




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
        print("best hand: " + str(hand.best_hand()))
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
        # #print(wins)
        #print("eval: ")
        #print(evaluated)
        #print("done?")
        print("EV: " + str(wins/evaluated))

#print(Hand([0,13,2,3,4]).hand_val())

# card_combos = it.combinations(np.unique(np.asarray(deck)), 2)
# for x in card_combos:
#         print("evaluating starting hand: " + str(x))

#returns odds of getting a better hand, with min threshold
print(better_hand_outs([full_deck[0], full_deck[1], full_deck[16], full_deck[4], full_deck[13], full_deck[26]], [], [True, "straight"]))
#print(better_hand_outs([full_deck[0], full_deck[1], full_deck[16], full_deck[4], full_deck[13], full_deck[26], full_deck[42]], [True, "straight"]))

print(better_hand_outs([full_deck[12], full_deck[25]], []))

h = Hand([12,25])
print(h.better_hand_check([False, "high"], [True, "single"]))

