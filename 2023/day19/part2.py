
from cProfile import Profile
from pstats import SortKey, Stats
import copy
import itertools

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]
#print(data)
empty_line = data.index("")
workflow_data = data[:empty_line]
part_data = data[empty_line + 1:]

def change_tuple(t:tuple, i:int, value):
    l = list(t)
    l[i] = value
    return tuple(l)

parts = []
for line in part_data:
    line = line.strip("{}")
    cats = line.split(",")
    cats = map(lambda x: x.strip("=xmas"), cats)
    cats = map(int, cats)
    parts.append(list(cats))

#print(parts)

workflows = {}
for line in workflow_data:
    name, rule = line.strip("}").split("{")

    rules = []
    rule_data = rule.split(",")
    for r in rule_data[:-1]:
        comp, target = r.split(":")

        cat_map = {"x":0, "m":1, "a":2, "s":3}

        cat = cat_map[comp[0]]
        op = comp[1]
        value = int(comp[2:])

        rules.append((cat, op, value, target))

    default = rule_data[-1]

    workflows[name] = (rules, default)

#for k,v in workflows.items():
#    print(k,v)

ranges = set()

def process_part(part:list[int], workflow:str, limits:tuple[tuple[int,int]], i:int=0):
    if workflow == "A":
        ranges.add(tuple(limits))
        return

    if workflow == "R":
        return

    rules, default = workflows[workflow]

    for rule in rules:
        cat, op, value, target = rule
        cat_l = limits[cat]
        if op == "<":
            next_range = (cat_l[0], min(value - 1, cat_l[1]))
            new_range = (value, cat_l[1])

        else:
            next_range = (max(value + 1, cat_l[0]), cat_l[1])
            new_range = (cat_l[0], value)


        next_limit = change_tuple(limits, cat, next_range)
        process_part(part, target, next_limit, i+1)

        limits = change_tuple(limits, cat, new_range)


    process_part(part, default, limits, i+1)

#Find all possible ranges for each part
limits = [(1,4000),(1,4000),(1,4000),(1,4000)]
for part in parts:
     process_part(part, "in", limits)

total = 0
for r in ranges:
    range_total = 1
    for i in range(4):
        range_total *= r[i][1] - r[i][0] + 1
    total += range_total

print(total)
