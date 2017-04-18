THREE_OF_A_KIND_START = 3730#13*220+13 + 858
THREE_OF_A_KIND_COMBOS = 858
THREE_OF_A_KIND_END = THREE_OF_A_KIND_START+THREE_OF_A_KIND_COMBOS

def card_val (card):
    return card%13

def tri_nums(num):
    if num <= 0: return 0
    else:
        return num+tri_nums(num-1)

def three_of_a_kind_val(t, c1, c2):
    t = card_val(t)
    if c1>t: c1 = card_val (c1)-2
    else:c1 = card_val (c1)-1
    if c2>t: c2 = card_val(c2)-1
    else:c2 = card_val (c2)
    return (66*t)+tri_nums(c1)+c2

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

three_of_a_kind_test()
print (three_of_a_kind_val(12, 11, 10))
