input = open("input.txt", "r")

output = 0

def test_line(line):
    if (line.count("a") + line.count("e") + line.count("i") + line.count("o") + line.count("u") < 3):
        return 0

    for a in ["ab", "cd", "pq", "xy"]:
        if (a in line):
            return 0

    #print(line)

    last_char = line[0]
    for char in line[1:]:
        #print(last_char + char)
        if(char == last_char):
            return 1
        last_char = char

    return 0


#test_line("sszojmmrrkwuftyv")

for line in input:
    if(test_line(line) != 0):
        output = output + 1

print(str(output))
