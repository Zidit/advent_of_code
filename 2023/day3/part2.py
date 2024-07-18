import re


input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()
    data = [line.strip() for line in data]

def get_number(line:str, pos):
    #print(line, pos)
    if not line[pos].isdigit():
        return None
    
    while line[pos].isdigit() and pos > 0:
        pos -= 1

    #print(pos, line[pos:])

    tmp = re.findall("\d+", line[pos:])
    if len(tmp):
        return int(tmp[0])

sum = 0
valid = set()
for x, line in enumerate(data):
    for y, char in enumerate(line):
        if char == "*":
            print(x,y)
            gears = set()
            for xi in range(x - 1, x + 2):
                for yi in range(y - 1, y + 2):
                    num = get_number(data[xi], yi)
                    if num:
                        gears.add(num)

            if len(gears) == 2:
                tmp = list(gears)
                sum += tmp[0] * tmp[1]

                        


print(sum)