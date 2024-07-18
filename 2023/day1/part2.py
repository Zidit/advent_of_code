import re

input_file = "example2.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

def str_to_int(line):
    line = line.replace("one", "1")
    line = line.replace("two", "2")
    line = line.replace("three", "3")
    line = line.replace("four", "4")
    line = line.replace("five", "5")
    line = line.replace("six", "6")
    line = line.replace("seven", "7")
    line = line.replace("eight", "8")
    line = line.replace("nine", "9")
    return line

sum = 0
for line in data:
    digits = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

    d1 = str_to_int(digits[0])
    d2 = str_to_int(digits[-1])

    print(digits, d1, d2)

    num = int(d1 + d2)
    sum += num

print(sum)