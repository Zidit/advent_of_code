input = open("input.txt", "r")

output = 0

def test_line(line):

    ok = False

    for i,char in enumerate(line):
        if line[i + 2:].find(line[i:i+2]) != -1:
            #print(line + " " + line[i + 2:] + " " + line[i:i+2])
            ok = True

    if(ok == False): return 0

    for i,char in enumerate(line[2:]):
        #print(line[i] + char)
        if(line[i] == char):
            #print(line[i] + char)
            return 1

    return 0


test_line("issasljhemltasdzlum")

for line in input:
    if(test_line(line) != 0):
        output = output + 1

print(str(output))
