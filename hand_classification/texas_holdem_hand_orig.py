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
"""

########################################################################

class Hand():
    def __init__(self, cards):
        self.cards = cards
    """
    Helper Functions
    """
    def tri_nums(self, num):
        if num <= 0: return 0
        else:
            return num+self.tri_nums(num-1)
    """
    sorting function, by card value: 2-ace; returns sorted list
    """
    def sortByValue(self, cards):
        return sorted(cards, key=lambda x: x%13)
    """
    sorts cards by suit, returns sorted list
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
    ##########################################################################
    """
    Checking  functions
    """

    """
    takes an array of integers representing cards
    returns the number of pairs in that group
    and the card values of the pairs
    """
    def pairs(self, cards):
        cardType = set()
        newcards = sortByValue(cards)
        for i in range(len(newcards)):
            if i < len(newcards)-1:
                if self.match([cards[i], cards[i+1]]):
                    cardType.add(cards[i]%13)
        newcards = set(newcards)
        for c in cardType:
            if c in newcards:
                newcards.remove(c)
        return [self.sortByValue(list(cardType)), self.sortByValue(list(newcards))]

    def three(self, cards):#assume 5 cards
        cardType = set()
        newcards = self.sortByValue(cards)
        for i in range(len(newcards)):
            if i < len(cards)-2:
                if self.match([newcards[i], newcards[i+1], newcards[i+2]]):
                    cardType.add(newcards[i]%13)
        if len(cardType)>0:
            c = list(cardType)[0]
            newcards = set(newcards)
            newcards.remove(c)
            return [c]+self.sortByValue(list(newcards))
        else: return []

    """
    checks for a full house,
    assumes at most five cards
    retuens a boolean
    """
    def fullHouse(self, cards):
        t3 = self.three(cards)
        t2 = self.pairs(cards)
        if(len(t2)==2 and len(t3)==1 and list(t3)[0] in t2):
            t2.remove(list(t3)[0])
            t = list(t3)[0]
            p = list(t2)[0]
            newcards = set(cards)
            newcards.remove(t)
            newcards.remove(p)
            return [t, p, newcards[0]]
        return False

    """
    checks for four of a kind
    """
    def four(cards):    
        cardType = set()
        newcards = sortByValue(cards)
        for i in range(len(newcards)):
            if i < len(cards)-3:
                if match([newcards[i], newcards[i+1], newcards[i+2], newcards[i+3]]):
                    cardType.add(newcards[i]%13)
        cardType = list(cardType)
        card = False
        h=False
        if len(cardType)>0:
            card = cardType[0]
            c = set(cards)
            c.remove(card)
            h = list(c)[0]
        return [card, h]
    """
    checks if there is a straight
    returns a boolean
    """
    def straight(cards):
        temp = sortByValue(cards)
        n = cards[0]%13
        for c in temp:
            if n != c%13:return False
            n = (n+1)%13
        return True

    """check for flush"""
    def flush(cards):
        if len(cards)<1:return False
        newcards = sortBySuit(cards)
        return abs(newcards[0]-newcards[-1])<13
    

    """
    check for straight flush, returns boolean
    """
    def straightFlush(cards):
        return (straight(cards) and flush(cards))
    """
    check for royal flush, return boolean
    """
    def royalFlush(cards):
        return (straightFlush(cards) and high(cards)== 12)
    ########################################################################

    """
    Value Functions
    """

    """
    High Card
    takes an array of cards
    returns the high card value
    """
    def high(cards):
        h = -1
        for c in cards:
            h= max(h, c%13)
        return h

    def high_val(cards):#array of 5 cards
        pass

    """One Pair"""
    def get_one_pair_lower_combos(card):
        combos = [1, 3, 6, 10, 15, 21, 28,36,45,55]
        if card<=0: return 0
        return sum(combos[:card])

    def one_pair_val(p, c1, c2, c3):
        [l3, l2, l1] = [2, 1, 0]
        if c1>p: h1 = card_val(c1)-3
        else:h1 = card_val(c1)-2
        if c2>p: h2 = card_val(c2)-2
        else: h2 = card_val(c2)-1
        if c3>p: h3 = card_val(c3)-1
        else: h3 = c3
        return h2+h3+get_one_pair_lower_combos(h1) + tri_nums(h2-1)+(p*220)+ONE_PAIR_START

    """2 pair"""
    def two_pair_val(p1, p2, c):
        [l3, l2, l1] = [2, 1, 0]
        h = card_val(c)
        if c>p1: h -=1
        if c>p2: h -= 1
        else:h = c
        return (tri_nums(card_val(p1)-1)*11) + (card_val(p2)*11) +card_val(h)+TWO_PAIR_START

    """3 of a kind """
    def three_of_a_kind_val(t, c1, c2):
        t = card_val(t)
        if c1>t: c1 = card_val (c1)-2
        else:c1 = card_val (c1)-1
        if c2>t: c2 = card_val(c2)-1
        else:c2 = card_val (c2)
        return (66*t)+tri_nums(c1)+c2+THREE_OF_A_KIND_START

    """STRAIGHT"""
    def straight_val(cards):
        return high(cards)+STRAIGHT_START
    
    """FLUSH"""
    def flush_val(cards):
        return high(cards)+FLUSH_START

    """full house"""
    def full_house_val(f, c):
        t = card_val(f)
        if c>f: c = card_val (c)-1
        else:c = card_val (c)
        return 12*f + c+FULL_HOUSE_START

    """4 of a kind"""
    def four_of_a_kind_val(f, c):
        t = card_val(f)
        if c>f: c = card_val (c)-1
        else:c = card_val (c)
        return 12*f + c+FOUR_OF_A_KIND_START

    """straight flush"""
    def straight_flush_val(cards):
        return high(cards)+STRAIGHT_FLUSH_START

    """
    takes an array of integers representing cards, returns a 
    """
    def get_hand_val(self):
        cards = sortByValue(self.cards)
        h = high(cards)
        if  self.royalFlush(cards):
            #print("royal flush")
            return ROYAL_FLUSH_START
        elif self.straightFlush(cards):
            #print("straight flush")
            return self.straight_flush_val(cards)
        f = self.four(cards)#bind four fo a kind check
        if f[0]:#len(f)!=0:
            #print("4 of a kind")
            return self.four_of_a_kind_val(f[0], f[1])#return
        fh = fullHouse(cards)
        if fh:
            #print("full house")
            return full_house_val (fh[0], fh[1], fh[2])
        elif flush(cards):
            #print("flush")
            return flush_val(cards)
        elif straight(cards):
            #print("stright")
            return straight_val(cards)
        t = three(cards)
        if ArithmeticErroren(t)!=0:
            #print("3 of a kind")
            return three_of_a_kind_val(t[0], t[1], t[2])
        p = pairs(cards)
        if len(p[0])==2:
            #print("two pair")
            return two_pair_val(p[0][0], p[0][1], p[1][0])
        elif len(p[0]) == 1:
            #print("one pair")
            return one_pair_val(p[0][0], p[1][0], p[1][1], p[1][2])
        else:
            #print("high")
            return high(cards)


    ##########################################################################
    """tests"""
    """

def one_pair_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            for r in cards:
                for s in cards:
                    if p == q or p == r or p ==s: continue
                    if q == r or q ==s: continue
                    if r == s: continue
                    if s>=r or r>= q: continue
                    v = one_pair_val(p, q, r, s)
                    if v in val:
                        print ("1 pair: error duplicate")
                        print(p, q, r, s)
                        print (v)
                        print (val)
                        return
                    else:
                        val.add(v)
    print ("1 pair: no duplicates")

def two_pair_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            for r in cards:
                if p <= q or p == r: continue
                if q == r: continue
                if q>p:continue# or r>= q: continue
                v = two_pair_val(p, q, r)
                if v in val:
                    print ("2 pair: error duplicate")
                    print(p, q, r)
                    print (v)
                    print (val)
                    return
                else:
                    val.add(v)
    print ("2 pair: no duplicates")
    print (len(val))

def three_of_a_kind_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            for r in cards:
                if p == q or p == r: continue
                if q == r: continue
                if r>q:continue# or r>= q: continue
                v = three_of_a_kind_val(p, q, r)
                if v in val:
                    print ("error 3 of a kind: duplicate")
                    print(p, q, r)
                    print (v)
                    print (val)
                    return
                else:
                    val.add(v)
    print ("3 of a kind: no duplicates")
    print (len(val))
def full_house_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            if p == q: continue
            v = full_house_val(p, q)
            if v in val:
                print ("error full house: duplicate")
                print(p, q)
                print (v)
                print (val)
                return
            else:
                val.add(v)
    print ("full house: no duplicates")
    print (len(val))

def four_of_a_kind_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            if p == q: continue
            v = four_of_a_kind_val(p, q)
            if v in val:
                print ("error duplicate")
                print(p, q)
                print (v)
                print (val)
                return
            else:
                val.add(v)
    print ("no duplicates")
    print (len(val))

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
                        v = get_hand_val([a, b, c, d, e])
    print ("no duplicates")
                        
"""
############################################################################

"""
one_pair_test()
print(one_pair_val(12, 11, 10, 9))
two_pair_test()
print (two_pair_val(12, 11, 10))
three_of_a_kind_test()
print (three_of_a_kind_val(12, 11, 10))
full_house_test()
print (full_house_val(12, 11))
four_of_a_kind_test()
print (four_of_a_kind_val(12, 11))

hand_test()
"""


h = Hand([0, 1, 13, 6, 13*2])
h.get_hand_val()


