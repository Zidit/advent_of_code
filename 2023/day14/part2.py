import math
import time
import sys
from cProfile import Profile
from pstats import SortKey, Stats
import functools

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [x.strip() for x in data]



def rotate_right(table:list[str]):
    def get_col(table:list[str], col_index:int):
        return [row[col_index] for row in table]

    return ["".join(get_col(table, i)[::-1]) for i in range(len(table[0]))]


def print_data(data:list[list[str]]):
    for line in data:
        print(line)
    print()


@functools.cache
def tilt_line(line:str):
    parts = line.split("#")

    tilted_parts = []
    for part in parts:
        l = len(part)
        o = part.count("O")
        tilted_parts.append("O"*o + "."*(l-o))

    return "#".join(tilted_parts)

def tilt_left(platform:list[str]):
    new_platform = []
    for line in platform:
        new_platform.append(tilt_line(line))

    return new_platform

def spin_cycle(platform:list[str]):
    for _ in range(4):
        platform = tilt_left(platform)
        platform = rotate_right(platform)
    return platform

def calc_weight(platform:list[str]):
    total = 0
    for i, line in enumerate(platform[::-1]):
        total += line.count("O") * (i + 1)

    return total



with Profile() as profile:

    data = rotate_right(data)
    data = rotate_right(data)
    data = rotate_right(data)

    cache = [data]

    for i in range(1000):
        data = spin_cycle(data)

        if data in cache:
            a = cache.index(data)
            i += 1
            period = i - a
            print("Dublicate found:", a, "->", i, period)

            break

        cache.append(data)


    ci = ((1000000000 - a) % period) + a
    print(calc_weight(rotate_right(cache[ci])))

    Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()