import math
import functools
import time
import re
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
#input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [line.strip().split(" ") for line in data]
data = [(line[0], [int(i) for i in line[1].split(",")]) for line in data]
#print(data[:3])
data = [((line[0] + "?") * 5, line[1] * 5) for line in data]
#print(data[:3])

#print(data)

def is_valid(line:str, check:str):
    #check = [int(i) for i in check.split(",")]
    damaged = [len(v) for v in line.split(".") if len(v)]
    return damaged == check

def line_iter(line:str):
    if "?" in line:
        yield from line_iter(line.replace("?", ".", 1))
        yield from line_iter(line.replace("?", "#", 1))
    else:
        yield line


def test_line_old(line:str, check:str):
    if "?" not in line:
        return 1 if is_valid(line, check) else 0

    else:
        tot = test_line(line.replace("?", ".", 1), check)
        tot += test_line(line.replace("?", "#", 1), check)
        return tot


@functools.cache
def test_line(line:str, res:tuple[re.Pattern]):
    #print(f"Test {stage}: ", line, res)

    if len(res) == 0:
        return 0 if "#" in line else 1

    i = 0
    matches = 0
    while (m := res[0].search(line[i:])) and "#" not in line[:m.start() + i] :
        #print(m, line[:m.start() + i], line[:i + m.end()])
        matches += test_line(line[m.end() + i:], res[1:])

        if m[0][0] == "#":
            break

        i += m.start() + 1

    return matches



total = 0

with Profile() as profile:

    for line, check in data:
        res = [re.compile(f"[#?]{{{s}}}[.?]") for s in check]
        valids = test_line(line + ".", tuple(res))
        #print(".", end="", flush=True)
        print(line, check, valids)

        if False:
            valid_old = 0
            for iter in line_iter(line):
                if is_valid(iter, check):
                    valid_old += 1

            if valids != valid_old:
                print(line, check, valids, valid_old)
                break
                print()

        total += valids

    #res = [re.compile(f"[#?]{{{s}}}[.?]") for s in [2,1]]
    #print(test_line("???????" + ".", res))
    print()

    #Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

print(total)