

input = open("input.txt", "r")
chars = 0
size = 0

for line in input:
    chars += len(line)
    #print (line, len(line))

    new_line = ""
    for c in line:
        if c == "\"" or c == "\\":
            new_line += "\\"
        new_line += c

    #print (new_line, len(new_line) + 2)

    size += len(new_line) + 2


print (size - chars)
