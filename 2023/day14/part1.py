import math
import time

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [[i for i in x.strip()] for x in data]

def transpose(data:list[list[str]]):
    def get_col(data:list[list[str]], col_index:int):
        return [row[col_index] for row in data]

    return [get_col(data, i) for i in range(len(data[0]))]

def print_data(data:list[list[str]]):
    for line in data:
        print("".join(line))
    print()


print_data(data)


def roll_north_one_step(platform:list[list[str]]):
    for line_a, line_b in zip(platform[:-1], platform[1:]):
        for i in range(len(line_a)):
            if line_a[i] == "." and line_b[i] == "O":
                line_a[i] = "O"
                line_b[i] = "."

def roll_north(platform:list[list[str]]):
    for _ in range(len(platform)):
        roll_north_one_step(platform)


def calc_weight(platform:list[list[str]]):
    total = 0
    for i, line in enumerate(platform[::-1]):
        for c in line:
            if c == "O":
                total += i + 1

    return total


start = time.perf_counter()

roll_north(data)
print_data(data)


print(calc_weight(data))


print("Time: ", time.perf_counter() - start)

