import re

input_file = "example1.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

sum = 0
for line in data:
    line_id, game = line.split(":")
    line_id = int(line_id.split(" ")[1])

    parsed_game = []
    for sets in game.split(";"):
    
        parsed_set = {}
        for color in sets.split(","):
            v, c = color.strip().split(" ")
            parsed_set[c] = int(v)
        parsed_game.append(parsed_set)

    is_valid = True
    for sets in parsed_game:
        is_valid = is_valid and sets.get("red", 0) <= 12
        is_valid = is_valid and sets.get("green", 0) <= 13
        is_valid = is_valid and sets.get("blue", 0) <= 14

    if is_valid:
        sum += line_id

print(sum)