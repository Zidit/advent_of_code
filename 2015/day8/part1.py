

input = open("input.txt", "r")
chars = 0
size = 0

for line in input:
    chars += len(line)
    print (line, len(line))

    new_line = ""
    escape = False
    skip = 0
    for i,c in enumerate(line):
        if skip > 0:
            skip -= 1
        else:
            if(not escape):
                if(c == "\\"):
                    escape = True
                else:
                    new_line += c
            else:
                escape = False
                if(c == "x"):
                    skip = 2
                    new_line += "#"

                else:
                    new_line += c

    print (new_line, len(new_line) - 2)

    size += len(new_line) - 2


print (chars - size)
