ONE_PAIR_START = 13
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

def card_val (card):
    return card%13

def tri_nums(num):
    if num <= 0: return 0
    else:
        return num+tri_nums(num-1)

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
    return h2+h3+get_one_pair_lower_combos(h1) + tri_nums(h2-1)+ONE_PAIR_START#13+(p*220)


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
    return high(cards)

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
    return 12*f + c+FOUr_OF_A_KIND_START


##########################################################################
"""tests"""
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
                        print ("error duplicate")
                        print(p, q, r, s)
                        print (v)
                        print (val)
                        return
                    else:
                        val.add(v)
    print ("no duplicates")

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
                    print ("error duplicate")
                    print(p, q, r)
                    print (v)
                    print (val)
                    return
                else:
                    val.add(v)
    print ("no duplicates")
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
                    print ("error duplicate")
                    print(p, q, r)
                    print (v)
                    print (val)
                    return
                else:
                    val.add(v)
    print ("no duplicates")
    print (len(val))
def full_house_test():
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12]
    val = set()
    for p in cards:
        for q in cards:
            if p == q: continue
            v = full_house_val(p, q)
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

