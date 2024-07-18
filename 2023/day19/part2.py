
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
#input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]
#print(data)
empty_line = data.index("")
workflow_data = data[:empty_line]
part_data = data[empty_line + 1:]

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
#print(workflows)


def process_part(part:list[int], workflow:str):
    if workflow == "A":
        return "A"
    if workflow == "R":
        return "R"

    rules, default = workflows[workflow]

    for rule in rules:
        if rule[1] == "<":
            if part[rule[0]] < rule[2]:
                return process_part(part, rule[3])
        else:
            if part[rule[0]] > rule[2]:
                return process_part(part, rule[3])

    return process_part(part, default)


total = 0
for part in parts:
    target = process_part(part, "in")
    if target == "A":
        total += sum(part)

print(total)




