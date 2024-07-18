


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

        else:
            print(f"opcode: {code[pos]}, pos = {pos}")
            print(code)
            raise Exception


data = []
with open("input.txt", "r", encoding="utf-8") as f:
    data = [int(i) for i in f.readline().split(",")]

print(data)
run(data, [1])