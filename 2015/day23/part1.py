
reg_a = 0
reg_b = 0
pc = 0

input = open("input.txt")

line_offset = []
offset = 0
for line in input:
    line_offset.append(offset)
    offset += len(line)
input.seek(0)


while pc < len(line_offset):
    print(pc)
    input.seek(line_offset[pc])
    line = input.readline()[:-1]
    #print(line)
    tokens = line.split()

    if tokens[0] == "hlf":
        if tokens[1] == "a":
            reg_a //= 2
        else:
            reg_b //= 2
        pc += 1

    elif tokens[0] == "tpl":
        if tokens[1] == "a":
            reg_a *= 3
        else:
            reg_b *= 3
        pc += 1

    elif tokens[0] == "inc":
        if tokens[1] == "a":
            reg_a += 1
        else:
            reg_b += 1
        pc += 1

    elif tokens[0] == "jmp":
        pc += int(tokens[1])

    elif tokens[0] == "jie":
        if tokens[1][0] == "a" and reg_a % 2 == 0:
            pc += int(tokens[2])
        elif tokens[1][0] == "b" and reg_b % 2 == 0:
            pc += int(tokens[2])
        else:
            pc += 1

    elif tokens[0] == "jio":
        if tokens[1][0] == "a" and reg_a == 1:
            pc += int(tokens[2])
        elif tokens[1][0] == "b" and reg_b == 1:
            pc += int(tokens[2])
        else:
            pc += 1

print ("A: ", reg_a, "B: ", reg_b)
