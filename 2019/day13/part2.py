import os
import time

class intcode:
    def __init__(self, code=None, file=None):
        if file:
            with open(file, "r", encoding="utf-8") as f:
                code = f.readline()

        code = [int(i) for i in code.split(",")]

        self.code = code + [0] * 10000
        self.halted = False
        self.pos = 0
        self.rel_base = 0

    def run_for_multiple_outputs(self, inputs, outputs):
        out = []
        for _ in range(outputs):
            out.append(self.run(inputs))
            inputs = None

        return tuple(out)

    def run(self, input):
        output = []
        input_pos = 0
        #print(code, input)
        while(1):
            inst = self.code[self.pos]
            op = inst % 100

            arg_pos = [None, None, None]
            args = [None, None, None]
            for i in range(3):
                try:
                    mod_pos = 100 * (10**i)
                    mod = (inst // mod_pos) % 10
                    if mod == 1: #Immediate Mode
                        arg_pos[i] = self.pos + i + 1
                    elif mod == 2: #Relative Mode
                        arg_pos[i] = self.code[self.pos + i + 1] + self.rel_base
                    else: #Position Mode
                        arg_pos[i] = self.code[self.pos + i + 1]

                    args[i] = self.code[arg_pos[i]]

                except IndexError:
                    pass
            #print(f"{inst=}, {op=}, {args=}, {arg_pos=}, {self.rel_base=}")

            #HALT
            if op == 99:
                self.halted = True
                return

            #SUM
            if op == 1: 
                self.code[arg_pos[2]] = args[0] + args[1]
                self.pos += 4

            #MUL
            elif op == 2:
                self.code[arg_pos[2]] = args[0] * args[1]
                self.pos += 4

            #INPUT
            elif op == 3:
                self.code[arg_pos[0]] = input[input_pos]
                input_pos += 1
                self.pos += 2

            #OUTPUT
            elif op == 4:
                output += [args[0]]
                self.pos += 2
                return args[0]

            #IF TRUE
            elif op == 5:
                if args[0] != 0:
                    self.pos = args[1]
                else:
                    self.pos += 3

            #IF NOT TRUE
            elif op == 6:
                if args[0] == 0:
                    self.pos = args[1]
                else:
                    self.pos += 3

            #LESS THAN
            elif op == 7:
                if args[0] < args[1]:
                    self.code[arg_pos[2]] = 1
                else:
                    self.code[arg_pos[2]] = 0
                self.pos += 4

            #EQUAL
            elif op == 8:
                if args[0] == args[1]:
                    self.code[arg_pos[2]] = 1
                else:
                    self.code[arg_pos[2]] = 0
                self.pos += 4

            #SET RELATIVE BASE
            elif op == 9:
                self.rel_base += args[0]
                self.pos += 2

            else:
                print(f"opcode: {self.code[self.pos]}, pos = {self.pos}")
                raise Exception


def print_map(m):
    for l in m:
        line = "".join(str(x) for x in l)
        line = line.replace("0", " ")
        line = line.replace("1", "|")
        line = line.replace("2", "#")
        line = line.replace("3", "-")
        line = line.replace("4", "o")
        print(line)

    print("")

arcade = intcode(file="input.txt")
arcade.code[0] = 2

size_x = 42
size_y = 25
m = [[0 for _ in range(size_x)] for _ in range(size_y)]

def find(m, char):
    for i, y in enumerate(m):
        if char in y:
            return y.index(char), i

    return None

score = 0
move = 0
while True:
    x, y, t = arcade.run_for_multiple_outputs([move], 3)
    if x is None:
        break

    if x == -1:
        score = t
    else:
        m[y][x] = t

    ball = find(m, 4)
    padel = find(m, 3)

    if padel is not None and ball is not None:

        if ball[0] < padel[0]:
            move = -1
        elif ball[0] > padel[0]:
            move = 1
        else:
            move = 0

        #os.system('clear')
        #print_map(m)
        #print(score)
        #time.sleep(0.03)

        #if sum([y.count(2) for y in m]) == 0:
            #break

print_map(m)
print(score)