class intcode:
    def __init__(self, code_string):
        code = [int(i) for i in code_string.split(",")]
        self.code = code + [0] * 10000
        self.halted = False
        self.pos = 0
        self.rel_base = 0

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
        line = "".join(l).replace("0", ".").replace("1", "#")
        print(line)

    print("")

def run_code(code):
    program = intcode(code)

    size = 10000
    #panel_map = ["".join(["." for _ in range(size)]) for _ in range(size)]
    panel_map = [[0 for _ in range(size)] for _ in range(size)]

    pos_x = size // 2
    pos_y = size // 2
    direction = 0
    painted_panels = []

    while program.halted == False:
        panel = panel_map[pos_y][pos_x]
        paint = program.run([panel])
        turn = program.run([])

        if program.halted == True:
            break

        if panel_map[pos_y][pos_x] != paint:
            painted_panels.append((pos_x, pos_y))

        panel_map[pos_y][pos_x] = paint

        if turn == 0:
            direction -= 1
            if direction < 0:
                direction = 3
        else:
            direction += 1
            if direction > 3:
                direction = 0
     
        if direction == 0:
            pos_y += 1
        elif direction == 1:
            pos_x += 1
        elif direction == 2:
            pos_y -= 1
        elif direction == 3:
            pos_x -= 1

        print(pos_x, pos_y, direction)


    #print_map(panel_map)

    return len(set(painted_panels))



with open("input.txt", "r", encoding="utf-8") as f:
    input_code = f.readline()

i = run_code(input_code)
print(i)