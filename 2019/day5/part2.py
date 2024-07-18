


def run(code, input):
    pos = 0
    input_pos = 0
    while(1):
        inst = code[pos]
        op = inst % 100
        p1_mod = (inst // 100) % 10
        p2_mod = (inst // 1000) % 10
        p3_mod = (inst // 10000) % 10
        #print(f"{inst=}, {op=}, {p1_mod=}, {p2_mod=}, {p3_mod=}")

        if op == 99:
            return code[0]

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
            print(arg1)
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

        
    

def unit_test(code, input, result):
    print(f"Running {code}..")
    print(f"Input {input}")
    run(code, [input])
    print(f"Expected {result}")
    print()


unit_test([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0 ,0)
unit_test([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1, 1)
unit_test([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0, 0)
unit_test([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 4, 1)
unit_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7, 999)
unit_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8, 1000)
unit_test([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9, 1001)

data = []
with open("input.txt", "r", encoding="utf-8") as f:
    data = [int(i) for i in f.readline().split(",")]

print(data)
run(data, [5])