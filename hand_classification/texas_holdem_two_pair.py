TWO_PAIR_START = 13*220+13
TWO_PAIR_END = 3730
TWO_PAIR_COMBOS = 858

def card_val (card):
    return card%13

def tri_nums(num):
    if num <= 0: return 0
    else:
        return num+tri_nums(num-1)


def two_pair_val(p1, p2, c):
    [l3, l2, l1] = [2, 1, 0]
    h = card_val(c)
    if c>p1: h -=1
    if c>p2: h -= 1
    else:h = c
    return (tri_nums(card_val(p1)-1)*11) + (card_val(p2)*11) +card_val(h)+TWO_PAIR_START

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
""""""
two_pair_test()
print (two_pair_val(12, 11, 10))
