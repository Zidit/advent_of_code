import re

input_file = "example1.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

sum = 0
for line in data:
    digits = re.findall(r"\d", line)
    sum += int(digits[0] + digits[-1])

print(sum)