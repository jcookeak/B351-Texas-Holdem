
"""
Clubs 0-13
Diamonds 14-26
Hearts 27-39
Spades 40-52

0 1 2 3 4 5 6 7 8  9 10 11 12
2 3 4 5 6 7 8 9 10 J Q  K  A


types:
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

at most 5 cards

"""
#Suit Keys
CLUBS = 0
DIAMONDS = 1
HEARTS = 2
SPADES = 3

#Hand keys:
#highcard = 0-12
ONE_PAIR = 13
TWO_PAIR = 14
THREE_OF_A_KIND = 15
STRAIGHT = 16
FLUSH = 17
FULL_HOUSE = 18
FOUR_OF_A_KIND = 19
STRAIGHT_FLUSH = 20
ROYAL_FLUSH = 21

"""
takes a card and returns a value representing the card's suit
"""
def getSuit(card):
    if card >= 40: return SPADES
    elif card >=27: return HEARTS
    elif card >=14: return DIAMONDS
    else: return CLUBS

"""
takes a group of cards and reutrns a boolean indicating
if the cards are the same suit
"""
def flush(cards):
    s = set()
    for c in cards:
        set.add(getSuit(c))
    return len(list(s)) == 1

"""
takes two integers representing cards and returns a boolean
inidicating if the two cards are a pair
"""
def pair(c1, c2):
    return c1%13 == c2%13

"""
takes an array of integers representing cards
returns a boolean indicating if there is a pair
"""
def hasPair(cards):
    for i in range(len(cards)):
        if i > len(cards)-1:
            for j in range(len(cards)-1):
                if pair(cards[i], cards[j]): return True
    return False

"""
takes an array of integers representing cards
returns the number of pairs in that group
and the card values of the pairs
"""
def pairs(cards):
    cardType = set()
    for i in range(len(cards)):
        if i < len(cards)-1:
            for j in range(i+1, len(cards)):
                if match([cards[i], cards[j]]):
                    cardType.add(cards[i]%13)
    return cardType

"""
takes a group of cards and checks if they match
"""
def match(cards):
    v = cards[0]%13
    for c in cards:
        if c%13!=v: return False
    return True

"""
"""
def three(cards):
    cardType = set()
    for i in range(len(cards)):
        if i < len(cards)-1:
            for j in range(i+1, len(cards)):
                if i < len(cards)-2:
                    for k in range(j+1, len(cards)):
                        if match([cards[i], cards[j], cards[k]]):
                            cardType.add(cards[i]%13)
    return cardType

"""
checks for a full house,
assumes at most five cards
retuens a boolean
"""
def fullHouse(cards):
    t3 = three(cards)
    t2 = pairs(cards)
    if(len(t2)==2 and len(t3)==1 and list(t3)[0] in t2):
        t2.remove(list(t3)[0])
        return [list(t3)[0], list(t2)[0]]
    return False

"""
checks for four of a kind
"""
def four(cards):
    res = set()
    cardType = {}
    for c in cards:
        if c%13 in cardType:
            cardType[c] = 1
        else: cardType[c] += 1
    for t in cardType:
        if cardType[i] == 4:
            res.add(t)
    return res

"""
takes an array of cards
returns the high card value
"""
def high(cards):
    h = -1
    for c in cards:
        h= max(h, c%13)
    return h

"""
sorting function, by card value: 2-ace; returns sorted list
"""
def sortByValue(cards):
    return sorted(cards, key=lambda x: x%13)

"""
sorts cards by suit, returns sorted list
"""
def sortBySuit(cards):
    return cards.sort()

"""
checks if there is a straight
returns a boolean
"""
def straight(cards):
    temp = sortByValue(cards)
    n = cards[0]%13
    for c in temp:
        if n != c%13:
            return False
        n = c%13+1
    return True

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

"""
takes an array of integers representing cards, returns a 
"""
def getHand(card):
    h = high(cards)
    if  royalFlush(cards):
        return (ROYAL_FLUSH, None)
    elif straightFlush(cards):
        return (STRAIGHT_FLUSH , [None, h])
    f = four(cards)#bind four fo a kind check
    if len(f)!=0:
        return (FOUR_OF_A_KIND, [f, h])#return
    fh = fullHouse(cards)
    if fh:
        return (FULLHOUSE, [fh, h])
    elif flush(cards):
        return (FLUSH, [None, h])
    elif straight(cards):
        return (STRAIGHT, [None, h])
    t = three(cards)
    if len(t)!=0:
        return (THREE_OF_A_KIND, [t, h])
    p = pair(cards)
    if len(p)==2:
        return (TWO_PAIR, [p, h])
    elif len(p) == 1:
        return (ONE_PAIR, [p, h])
    else:
        return (h, [None, h])

"""
hand1 better than hand 2
takes two hands
hand:= (Hand_key, hand info)

high card wins:
straight flush, flush, straight, high card
match win:

"""

def compairHand(id1, id2, hand1, hand2):
    (key1, info1) = hand1
    (key2, info2) = hand1
    if key1>key2: return id1
    elif key2>key1: return id2
    else:#the hand key is the same
        [i1, h1] = info1
        [i2, h2] = info2
        if i1==None:#win based on high card
            if h1>h2: return id1
            elif h2>h1: return id2
            else: pass#return tie
        else:#win based on match
            if key1 == FULL_HOUSE:
                #check 3 first then 2
                pass
            else:#one pair, two pair, three of a kind, four of a kind
                #check for two pair
                if key1 == TWO_PAIR:
                    #check higher pair
                    pass
                else:
                    hp1 = high(list(i1))
                    hp2 = high(list(i2))
                    #check if equal then high
                pass
        pass
        

"""
hand:= [id, hand]
"""
def bestHand(hands):
    pass

"""
tests
print(fullHouse([0, 13, 26, 1, 14]))
print(straight([0, 2+13, 3, 4+13, 1+13+13]))
"""
