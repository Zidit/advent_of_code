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


def test_reflection(pattern:list[list[str]]):
    for i in range(0, len(pattern) - 1):
        if test_reflection_line(pattern, i):
            return i + 1
    return 0

def test_reflection_line(pattern:list[list[str]], line:int):
    #print("Test:")
    #print_pattern(pattern)
    #print(line)
    l = pattern[:line + 1]
    l = l[::-1]
    r = pattern[line + 1:]
    m = min(len(l), len(r))
    l = l[:m]
    r = r[:m]

    #print_pattern(l)
    #print()
    #print_pattern(r)
    #print()

    return l == r



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

    total += test_reflection(pattern) * 100
    total += test_reflection(t_pattern)


print("Time: ", time.perf_counter() - start)

print(total)