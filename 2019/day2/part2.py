


def run(code):
    pos = 0
    while(1):
        if code[pos] == 99:
            return code[0]

        arg1_pos = code[pos + 1]
        arg2_pos = code[pos + 2]
        out_pos = code[pos + 3]

        if code[pos] == 1:
            code[out_pos] = code[arg1_pos] + code[arg2_pos]
        elif code[pos] == 2:
            code[out_pos] = code[arg1_pos] * code[arg2_pos]
        else:
            print(f"opcode: {code[pos]}, pos = {pos}")
            print(code)
            raise Exception

        pos += 4
    

def unit_test(code, result):
    print(f"Running {code}..")
    res = run(code)
    print(f"{result} == {res}")

#unit_test([1,0,0,0,99], 2)
#unit_test([2,3,0,3,99], 2)
#unit_test([2,4,4,5,99,0], 2)
#unit_test([1,1,1,4,99,5,6,0,99], 30)

def test(data):
    for verb in range(0, 99):
        for noun in range(0, 99):
            _data = data.copy()
            _data[1] = noun
            _data[2] = verb
            result = run(_data)
            if(result == 19690720):
                print(100 * noun + verb)
                return

data = []
with open("input.txt", "r", encoding="utf-8") as f:
    data = [int(i) for i in f.readline().split(",")]

test(data)

                
