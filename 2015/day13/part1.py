

def read_data():
    happines = {}
    quest = []
    input = open("input.txt", "r")
    for line in input:
        tokens = line.split(' ')
        quest.append(tokens[0])
        if tokens[2] == "gain":
            happines[(tokens[0],tokens[10][:-2])] = int(tokens[3])
        else:
            happines[(tokens[0],tokens[10][:-2])] = -int(tokens[3])

    return happines, list(set(quest))

def calc_pair_happines(happines):
    pair_happines = {}
    for pair in happines:
        pair_happines[pair] = happines[(pair[0],pair[1])] + happines[(pair[1],pair[0])]

    return pair_happines

def calc_total_happines(quest_order, pair_happines):
    total = 0
    for i, quest in enumerate(quest_order):
        total += pair_happines[(quest_order[i - 1], quest_order[i])]
    return total

def permutations_iter(input_list, prefix = []):
    if len(input_list) is 1:
        yield prefix + input_list
    for i, item in enumerate(input_list):
        yield from permutations_iter(input_list[:i] + input_list[i + 1:], prefix + [input_list[i]])


happines, quests = read_data()
pair_happines = calc_pair_happines (happines)

best = 0

for perm in permutations_iter(quests):
   best = max(calc_total_happines(perm, pair_happines), best)

print(best)
#print(pair_happines, quests)
