

def get_score(amounts, ingredients):

    total = (0,0,0,0,0)
    for i, amount in enumerate(amounts):
        total = tuple(map(sum, zip(tuple(a * amount for a in ingredients[i]), total)))

    score = 1
    for i in total[:-1]:
        if i <= 0:
            return 0
        score *= i

    if total[-1] != 500:
        return 0

    return score


def permutations_iter(amount, containers, prefix = []):
    if containers == 1:
        yield prefix + [amount]

    else:
        for i in range(amount + 1):
            yield from permutations_iter(amount - i, containers - 1, prefix + [i])

input = open("input.txt")
ingredients = []
for line in input:
    tokens = line.split()
    ingredients.append ((int(tokens[2][:-1]), int(tokens[4][:-1]), int(tokens[6][:-1]), int(tokens[8][:-1]), int(tokens[10])))

#print(get_score((44,56), ingredients))
#print(ingredients)

best_score = 0
for per in permutations_iter(100,len(ingredients)):
    best_score = max(get_score(per, ingredients), best_score)

print(best_score)
