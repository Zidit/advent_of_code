import re

input_file = "example.txt"
input_file = "input.txt"


with open(input_file, "r") as file:
    data = file.readlines()

sum = 0
valid = set()
for x, line in enumerate(data):
    for y, char in enumerate(line.strip()):
        if not char.isdigit() and char != ".":
            #print(char, x,y)
            for xi in range(x - 1, x + 2):
                for yi in range(y - 1, y + 2):
                   # print(" - ", (xi,yi), end="")
                    if xi >= 0 and xi < len(line) and yi >= 0 and yi < len(data):
                        valid.add((xi,yi))
                        #print(" ", (xi,yi))
                        
                        
#print(valid)


for x, line in enumerate(data):
    numbers = re.finditer("\d+", line)
    for num in numbers:
        for y in range(num.start(), num.end()):
            if (x, y) in valid:
                #print(num.group(), num.span())
                sum += int(num.group())
                break

print(sum)