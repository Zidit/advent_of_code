import math
import time

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [x for x in data[0].split(",")]
print(data)

def hash(data:str):
    current_value = 0
    for c in data:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value

total = 0
for d in data:
    h = hash(d)
    #print(h)
    total += h

print(total)