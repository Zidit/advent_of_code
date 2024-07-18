import math
import functools
import time
import re
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [line.strip().split(" ") for line in data]
data = [(line[0], [int(i) for i in line[1].split(",")]) for line in data]
data = [("?".join([line[0]]* 5) , line[1] * 5) for line in data]

#print(data)

@functools.cache
def test_line(line:str, res:tuple[re.Pattern]):
    #print(f"Test {stage}: ", line, res)

    if len(res) == 0:
        return 0 if "#" in line else 1

    i = 0
    matches = 0
    while (m := res[0].search(line[i:])) and "#" not in line[:m.start() + i] :
        #print(m, line[:m.start() + i], line[:m.end() + i - 1])
        matches += test_line(line[m.end() + i - 1:], res[1:])

        if m[0][0] == "#":
            break

        i += m.start() + 1

    return matches


total = 0
with Profile() as profile:

    for line, check in data:
        res = [re.compile(f"[.?][#?]{{{s}}}[.?]") for s in check]
        valids = test_line("." + line + ".", tuple(res))
        #print(".", end="", flush=True)
        #print(line, check, valids)

        total += valids

    print()

    #Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

print(total)