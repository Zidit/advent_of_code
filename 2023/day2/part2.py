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

    min_red = 0
    min_green = 0
    min_blue = 0

    is_valid = True
    for sets in parsed_game:
        min_red = max(min_red, sets.get("red", 0))
        min_green = max(min_green, sets.get("green", 0))
        min_blue = max(min_blue, sets.get("blue", 0))

    power = min_red * min_green * min_blue
    sum += power

print(sum)