"""
texas_holdem_hand.py
holds the Hand class

Last Modified: 4/20/17
Last Modified By: Anna

Comments:
currently works with 5 or 2 cards
high card and flush values only take into account the highest card in the hand

TODO:
add fix to determine best hand for hand of more than 5 cards
add hand comparison function
"""

#import numpy as np
import itertools as it


#########
#GLOBALS#
#########
HIGH_CARD_START = 0
HIGH_CARD_COMBOS = 13#fix later
HIGH_CARD_END = HIGH_CARD_START + HIGH_CARD_COMBOS

ONE_PAIR_START = HIGH_CARD_END
ONE_PAIR_COMBOS = 13*220
ONE_PAIR_END = ONE_PAIR_COMBOS + ONE_PAIR_START

TWO_PAIR_START = ONE_PAIR_END#13*220+13
TWO_PAIR_COMBOS = 858
TWO_PAIR_END = TWO_PAIR_COMBOS+ TWO_PAIR_START#3730

THREE_OF_A_KIND_START = TWO_PAIR_END#3730#13*220+13 + 858
THREE_OF_A_KIND_COMBOS = 858
THREE_OF_A_KIND_END = THREE_OF_A_KIND_START+THREE_OF_A_KIND_COMBOS

STRAIGHT_START = THREE_OF_A_KIND_END
STRAIGHT_COMBOS = 11#??
STRAIGHT_END = THREE_OF_A_KIND_END+STRAIGHT_COMBOS

FLUSH_START = STRAIGHT_END
FLUSH_COMBOS = 9#?? (probably needs less)
FLUSH_END = FLUSH_START+FLUSH_COMBOS

FULL_HOUSE_START = FLUSH_END
FULL_HOUSE_COMBOS = 156
FULL_HOUSE_END = FULL_HOUSE_START  + FULL_HOUSE_COMBOS

FOUR_OF_A_KIND_START = FULL_HOUSE_END
FOUR_OF_A_KIND_COMBOS = 156
FOUR_OF_A_KIND_END = FOUR_OF_A_KIND_START+FOUR_OF_A_KIND_COMBOS

STRAIGHT_FLUSH_START = FOUR_OF_A_KIND_END
STRAIGHT_FLUSH_COMBOS = 9
STRAIGHT_FLUSH_END = STRAIGHT_FLUSH_START+STRAIGHT_FLUSH_COMBOS

ROYAL_FLUSH_START = STRAIGHT_FLUSH_START
ROYAL_FLUSH_COMBOS = 1
ROYAL_FLUSH_END = ROYAL_FLUSH_COMBOS+ROYAL_FLUSH_START

"""
royal flush
straight flush
four of a kind
full house
flush
straight
three of a kind
two pair
one pair
high card

should assume 2 to 5 cards

"""

"""
The Hand class
takes an array of private cards and an array of public cards
can check for types of hands and rank hands
"""

class Hand():
    def __init__(self, private_cards, public_cards = []):
        self.cards = private_cards + public_cards
        self.private = private_cards
        self.public = public_cards
        self.cards = self.sortByValue(self.cards)

    def __repr__(self):
        return str(self.cards)

    """
    takes an integer and returns the recursive result of summing the number
    with tri-num applied to the number -1
    """
    def tri_nums(self, num):
        if num <= 0: return 0
        else:return num+self.tri_nums(num-1)
    """
    sorting function, by card value: 2-ace; returns sorted list
    """
    def sortByValue(self, cards):
        return sorted(cards, key=lambda x: x % 13)
    """
    sorts cards by suit, returns sorted list lowest to highest by suit then card
    """
    def sortBySuit(self, cards):
        cards.sort()
        return cards
    """
    takes a group of cards and checks if they match
    """
    def match(self, cards):
        v = cards[0]%13
        for c in cards:
            if c%13!=v: return False
        return True
    """
    modCards: a helper function that takes a set of ints
    returns a set of modded integers: num%13
    """
    def modCards(self, cardset):
        newset = set(cardset)
        for i in cardset:
            newset.remove(i)
            newset.add(i%13)
        return newset
    """
    High Card
    takes an array of cards
    returns the high card value
    """
    def high(self, cards):
        h = -1
        for c in cards:
            h= max(h, c%13)
        return h

    """
    takes an integer representing a card
    returns an integer representing the card type (0-12)
    """
    def card_val(self, card):
        return card%13

    def lowest_cards(self, p):
        c = set([0, 1, 2, 3])
        if p in c: c.remove(p)
        else: c.remove(3)
        c = list(c)
        c.sort()
        return c

    ###############################
    """checkers"""

    """
    checks for pairs in the hand
    returns an array [[card type of pairs], [rest of cards]]
    """
    def pairs(self):
        cardType = set()
        newcards = self.sortByValue(self.cards)
        for i in range(len(newcards)):
            if i < len(newcards)-1:
                if self.match([newcards[i], newcards[i+1]]):
                    cardType.add(newcards[i]%13)
        newcards = set(newcards)
        if len(cardType) >0:
            newcards = self.modCards(newcards)
        for c in cardType:
            if c in newcards:
                newcards.remove(c)
        return [self.sortByValue(list(cardType)), self.sortByValue(list(newcards))]

    """
    checks for 3 of a kind
    returns an array [3-of-a-kind-type, card1, card2]
    or false
    """
    def three(self):
        if len(self.cards)<3: return False
        cardType = set()
        newcards = self.sortByValue(self.cards)
        for i in range(len(newcards)):
            if i < len(newcards)-2:
                if self.match([newcards[i], newcards[i+1], newcards[i+2]]):
                    cardType.add(newcards[i]%13)
        if len(cardType)>0:
            c = list(cardType)[0]
            newcards = self.modCards(set(newcards))
            newcards.remove(c)
            return [c]+self.sortByValue(list(newcards))
        else: return False
    """
    checks for a full house,
    assumes at most five cards
    retuens a boolean
    """
    def fullHouse(self):
        if len(self.cards)<5:return False
        t3 = self.three()
        t2 = self.pairs()
        if(t3 and len(t2[0]) == 2):return t3
        return False
    """
    checks for four of a kind
    returns an array:
    [4-of-a-kind-card-type, other-card]
    or
    [false, false]
    """
    def four(self):
        cardType = set()
        newcards = self.sortByValue(self.cards)
        for i in range(len(newcards)):
            if i < len(newcards)-3:
                if self.match([newcards[i], newcards[i+1], newcards[i+2], newcards[i+3]]):
                    cardType.add(newcards[i]%13)
        cardType = list(cardType)
        card = False
        h=False
        if len(cardType)>0:
            card = cardType[0]
            c = self.modCards(set(self.cards))
            c.remove(card)
            h = list(c)[0]
        return [card, h]
    """
    checks if there is a straight
    returns a boolean
    """
    def straight(self):
        if len(self.cards)<5:return False
        temp = self.sortByValue(self.cards)
        n = temp[0]%13
        for c in temp:
            if n != c%13:return False
            n = (n+1)%13
        return True

    """
    check for flush
    returns a boolean
    """
    def flush(self):
        if len(self.cards)<5:return False
        newcards = self.sortBySuit(self.cards)
        pred = abs(newcards[0]-newcards[-1])<13
        return pred
    """
    check for straight flush, returns boolean
    """
    def straightFlush(self):
        return (self.straight() and self.flush())
    """
    check for royal flush, return boolean
    """
    def royalFlush(self):
        return (self.straightFlush() and self.high(self.cards)== 12)
    """
    Value Functions
    """
    def high_val(self):
        return self.high(self.cards)
    """One Pair"""
    def get_one_pair_lower_combos(self, card):
        combos = [1, 3, 6, 10, 15, 21, 28,36,45,55]
        if card<=0: return 0
        return sum(combos[:card])

    def one_pair_val(self, p, c1=-1, c2=-1, c3=-1):
        [l3, l2, l1] = [2, 1, 0]
        #print(c1)
        if c1<0:
            c3, c2, c1 = self.lowest_cards(p)
        if c1>p: h1 = self.card_val(c1)-3
        else:h1 = self.card_val(c1)-2
        if c2>p: h2 = self.card_val(c2)-2
        else: h2 = self.card_val(c2)-1
        if c3>p: h3 = self.card_val(c3)-1
        else: h3 = c3
        return h2+h3+self.get_one_pair_lower_combos(h1) + self.tri_nums(h2-1)+(p*220)+ONE_PAIR_START

    """2 pair"""
    def two_pair_val(self, p1, p2, c):
        [l3, l2, l1] = [2, 1, 0]
        h = self.card_val(c)
        if c>p1: h -=1
        if c>p2: h -= 1
        else:h = c
        return (self.tri_nums(self.card_val(p1)-1)*11) + (self.card_val(p2)*11) +self.card_val(h)+TWO_PAIR_START

    """3 of a kind """
    def three_of_a_kind_val(self, t, c1, c2):
        t = self.card_val(t)
        if c1>t: c1 = self.card_val (c1)-2
        else:c1 = self.card_val (c1)-1
        if c2>t: c2 = self.card_val(c2)-1
        else:c2 = self.card_val (c2)
        return (66*t)+self.tri_nums(c1)+c2+THREE_OF_A_KIND_START

    """STRAIGHT"""
    def straight_val(self, cards):
        return self.high(cards)+STRAIGHT_START

    """FLUSH"""
    def flush_val(self, cards):
        return self.high(cards)+FLUSH_START

    """full house"""
    def full_house_val(self, f, c):
        t = self.card_val(f)
        if c>f: c = self.card_val (c)-1
        else:c = self.card_val (c)
        return 12*f + c+FULL_HOUSE_START

    """4 of a kind"""
    def four_of_a_kind_val(self, f, c):
        t = self.card_val(f)
        if c>f: c = self.card_val (c)-1
        else:c = self.card_val (c)
        return 12*f + c+FOUR_OF_A_KIND_START
    """straight flush"""
    def straight_flush_val(self, cards):
        return self.high(cards)+STRAIGHT_FLUSH_START
    """
    takes an array of integers representing cards, returns an integer hand ranking
    """
    def hand_val(self):
        cards = self.sortByValue(self.cards)
        if  self.royalFlush():
            return ROYAL_FLUSH_START
        elif self.straightFlush():
            return self.straight_flush_val(cards)
        f = self.four()#bind four of a kind check
        if f[0] or f[1]:
            return self.four_of_a_kind_val(f[0], f[1])#return
        fh = self.fullHouse()
        if fh:
            return self.full_house_val (fh[0], fh[1])
        elif self.flush():
            return self.flush_val(cards)
        elif self.straight():
            return self.straight_val(cards)
        t = self.three()
        if t:
            return self.three_of_a_kind_val(t[0], t[2], t[1])
        p = self.pairs()
        #print(p)
        if len(p[0])==2:
            return self.two_pair_val(p[0][0], p[0][1], p[1][0])
        elif len(p[0]) == 1:
            if len(self.cards) ==2: return self.one_pair_val(p[0][0])
            return self.one_pair_val(p[0][0], p[1][0], p[1][1], p[1][2])
        else: return self.high_val()

    def is_hand(self):
        cards = self.sortByValue(self.cards)
        if  self.royalFlush():
            return [True, "royal_flush"]
        elif self.straightFlush():
            return [True, "straight_flush"]
        f = self.four()#bind four of a kind check
        if f[0] or f[1]:
            return [True, "four"]#return
        fh = self.fullHouse()
        if fh:
            return [True, "full"]
        elif self.flush():
            return [True, "flush"]
        elif self.straight():
            return [True, "straight"]
        t = self.three()
        if t:
            return [True, "three"]
        p = self.pairs()
        #print(p)
        if len(p[0])==2:
            return [True, "two"] #two pair
        elif len(p[0]) == 1:
            if len(self.cards) ==2: return [True, "single"] #one pair
            return [True, "single"] #one pair
        else: return [False, "high"] #high-card

    ### get type of hand
    def hand_type(self, cards):
        return 0

    #takes in result from is_hand
    def better_hand_check(self, hand1, hand2):
        hands = ["high", "single", "two", "three", "straight", "flush", "full", "four", "straight_flush", "royal_flush"]
        return hands.index(hand2[1]) > hands.index(hand1[1])
        return 0

    #use for after flop?
    def hand_outs(self, cards):
        if len(cards) < 5:
            return -1

        return 0

    def best_hand(self):
        cards = self.cards[:]
        if len(cards)<5: return cards
        hand_combos = list(it.combinations(cards ,5))
        best_hand_val, best_hand_cards = -1, [-1, -1, -1, -1, -1]
        for h in hand_combos:
            self.cards = list(h)
            v = self.hand_val()
            if v > best_hand_val:
                best_hand_val = v
                best_hand_cards = list(h)
        self.cards = self.private + self.public
        return best_hand_cards
        
        
    
"""
Tests
"""
"""
check every possible 5 card hand
"""
def hand_test():
    cards = range(52)
    val = set()
    for a in cards:
        for b in cards:
            for c in cards:
                for d in cards:
                    for e in cards:
                        if a<=b or a==c or a==d or a==e:continue
                        if b<=c or b==d or b==e:continue
                        if c<=d or c==e or d<=e:continue
                        h = Hand([a, b, c, d, e])
                        v = h.hand_val()
if __name__ == "__main__":
    #h = Hand([1, 2, 3, 4, 49])
    #print(h.hand_val())
    #hand_test()
    #f = Hand([0, 1, 13, 26, 39])
    pass
"""
h = Hand([1, 2, 3, 4, 5, 6, 7])
print(h.best_hand())
"""
