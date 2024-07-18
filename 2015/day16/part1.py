

ref = (("children", 3), ("cats", 7), ("samoyeds", 2), ("pomeranians", 3), ("akitas", 0), ("vizslas", 0), ("goldfish", 5), ("trees", 3), ("cars", 2), ("perfumes", 1))



def test(samples, referense):
    for sample in samples:
        match = False
        for ref in referense:
            if sample[0] == ref[0] and sample[1] == ref[1]:
                match = True
        if match == False:
            return False

    return True


with open("input.txt") as input:
    for i,line in enumerate(input):
        tokens = line.split()
        sample = ((tokens[2][:-1], int(tokens[3][:-1])), (tokens[4][:-1], int(tokens[5][:-1])), (tokens[6][:-1], int(tokens[7])))
        if test(sample, ref) == True:
            print (i + 1)
