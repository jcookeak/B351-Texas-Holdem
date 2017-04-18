FOUR_OF_A_KIND_START = 0
FOUR_OF_A_KIND_COMBOS = 156
FOUR_OF_A_KIND_END = FOUR_OF_A_KIND_START+FOUR_OF_A_KIND_COMBOS

def card_val (card):
    return card%13

def tri_nums(num):
    if num <= 0: return 0
    else:
        return num+tri_nums(num-1)

def four_of_a_kind_val(f, c):
    t = card_val(f)
    if c>f: c = card_val (c)-1
    else:c = card_val (c)
    return 12*f + c

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

four_of_a_kind_test()
print (four_of_a_kind_val(12, 11))
