
wires ={}

def get_value(token):

    if(token.isdigit()):
        return int(token)
    elif(token in wires):
        return int(wires[token])
    else:
        return

def process_input(token):
    parts = token.split(" ")

    if (len(parts) == 1):
        return get_value(parts[0])

    elif (len(parts) == 2):
        A = get_value(parts[1])
        if (A is not None):
            if (parts[0] == "NOT"):
                return  ~A
            else:
                print( "not NOT")

    elif (len(parts) == 3):
        A = get_value(parts[0])
        B = get_value(parts[2])

        if (A is not None and B is not None):
            if (parts[1] == "AND"):
                return A & B
            elif (parts[1] == "OR"):
                return A | B
            elif (parts[1] == "LSHIFT"):
                return A << B
            elif (parts[1] == "RSHIFT"):
                return A >> B
            else:
                print ("Unknown OP: " + parts[1])
        return

    else:
        print ("Too many parts")



def process_line(line):
    input_token, output_token = line.split(" -> ")
    if(output_token.rstrip() in wires):
        return

    result = process_input(input_token)
    #print(result)

    if(result is not None):
        wires[output_token.rstrip()] = result


i = 1000

while ("a" not in wires and i > 0):

    input = open("input.txt", "r")
    for line in input:
        process_line(line)

    print (wires)
    i -= 1

if ("a" in wires ):
    print ("a: ", wires["a"])
