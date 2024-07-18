import math
import time

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()


pattern = list()
patterns = list()
for line in data:
    if line != "\n":
        pattern.append([c for c in line.strip()])
    else:
        patterns.append(pattern)
        pattern = list()
patterns.append(pattern)
#print(patterns)

def horizontal_ref(pattern:list[list[str]]):
    pairs = []
    for i, p in enumerate(zip(pattern[:-1], pattern[1:])):
        if p[0] == p[1]:
            pairs.append(i)

    for pair in pairs:
        l = pattern[:pair]
        l = l[::-1]
        r = pattern[pair+2:]
        m = min(len(l), len(r))
        l = l[:m]
        r = r[:m]

        if l == r:
            return pair + 1

    return 0

def transpose(pattern:list[list[str]]):
    def get_col(pattern:list[list[str]], col_index:int):
        return [row[col_index] for row in pattern]

    return [get_col(pattern, i) for i in range(len(pattern[0]))]

def print_pattern(pattern:list[list[str]]):
    for line in pattern:
        print("".join(line))


start = time.perf_counter()




total = 0
for pattern in patterns:
    #print_pattern(pattern)
    t_pattern = transpose(pattern)
    #print()
    #print_pattern(t_pattern)

    total += horizontal_ref(pattern) * 100
    total += horizontal_ref(t_pattern)


print("Time: ", time.perf_counter() - start)

print(total)