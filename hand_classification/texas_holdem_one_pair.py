ONE_PAIR_START = 13
ONE_PAIR_END = 13*220+13


def tri_nums(num):
    if num <= 0: return 0
    else:
        return num+tri_nums(num-1)

def card_val (card):
    return card%13

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
    return h2+h3+get_one_pair_lower_combos(h1) + tri_nums(h2-1)+13+(p*220)

"""test that there are no duplicate values"""
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

one_pair_test()
print(one_pair_val(12, 11, 10, 9))
