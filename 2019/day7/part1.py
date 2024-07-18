import itertools

def run(code, input):
    pos = 0
    input_pos = 0
    output = []
    #print(code, input)
    while(1):
        inst = code[pos]
        op = inst % 100
        p1_mod = (inst // 100) % 10
        p2_mod = (inst // 1000) % 10
        p3_mod = (inst // 10000) % 10
        #print(f"{inst=}, {op=}, {p1_mod=}, {p2_mod=}, {p3_mod=}")

        if op == 99:
            return output

        #SUM
        if op == 1: 
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            code[code[pos + 3]] = arg1 + arg2
            pos += 4

        #MUL
        elif op == 2:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            code[code[pos + 3]] = arg1 * arg2
            pos += 4

        #INPUT
        elif op == 3:
            code[code[pos + 1]] = input[input_pos]
            input_pos += 1
            pos += 2

        #OUTPUT
        elif op == 4:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            #print(arg1)
            output += [arg1]
            pos += 2

        #IF TRUE
        elif op == 5:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            if arg1 != 0:
                pos = arg2
            else:
                pos += 3

        #IF NOT TRUE
        elif op == 6:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            if arg1 == 0:
                pos = arg2
            else:
                pos += 3

        #LESS THAN
        elif op == 7:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            if arg1 < arg2:
                code[code[pos + 3]] = 1
            else:
                code[code[pos + 3]] = 0
            pos += 4

        #EQUAL
        elif op == 8:
            arg1 = code[pos + 1] if p1_mod == 1 else code[code[pos + 1]]
            arg2 = code[pos + 2] if p2_mod == 1 else code[code[pos + 2]]
            if arg1 == arg2:
                code[code[pos + 3]] = 1
            else:
                code[code[pos + 3]] = 0
            pos += 4

        else:
            print(f"opcode: {code[pos]}, pos = {pos}")
            print(code)
            raise Exception


def run_amp(code, phase, input):
    cc = code.copy()
    return run(cc, [phase, input])[0]

def run_all(code, phases):
    result = 0
    for phase in phases:
        result = run_amp(code, phase, result)
    return result


#print(run_all([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]))
#print(run_all([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]))
#print(run_all([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]))

def find_best(code):
    best = 0
    for test in itertools.permutations([0,1,2,3,4]):
        best = max(best, run_all(code, test))
    return best

#print(find_best([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]))
#print(find_best([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]))
#print(find_best([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]))

code = []
with open("input.txt", "r", encoding="utf-8") as f:
    code = [int(i) for i in f.readline().split(",")]


print(find_best(code))
