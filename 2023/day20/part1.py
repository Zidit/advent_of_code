import time
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
input_file = "example2.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

class mod_ff():
    def __init__(self):
        self.state = False

    def process(self, sender, pulse):
        if pulse == True:
            return
        self.state = not self.state
        return self.state

    def __str__(self) -> str:
        return f"FF:   {self.state}"
    def __repr__(self) -> str:
        return self.__str__()

class mod_con():
    def __init__(self):
        self.state = False
        self.inputs = {}

    def add_input(self, input_name):
        self.inputs[input_name] = False

    def process(self, sender, pulse):
        self.inputs[sender] = pulse

        states = set(self.inputs.values())
        if len(states) == 1 and True in states:
            return False
        else:
            return True
        
    def __str__(self) -> str:
        return f"Conj: {self.state} {self.inputs}"
    def __repr__(self) -> str:
        return self.__str__()


modules = {}
for line in data:
    line = line.strip()
    i, o = line.split(" -> ")
    o = o.split(", ")
    
    if i == "broadcaster":
        broadcaster = o
        continue
    
    func = i[0]
    if func == "%":
        func = mod_ff()
    elif func == "&":
        func = mod_con()
    else:
        raise Exception(f"Unknown func {func}")

    name = i[1:]
    modules[name] = (func, o)


for name, (func, out) in {k:v for k,v in modules.items() if isinstance(v[0], mod_con)}.items():
    for name2, (func2, out2) in modules.items():
        if name in out2:
            func.add_input(name2)


print(modules)
print(broadcaster)



def push_button():
    pulses = []
    high_pulses = 0
    low_pulses = 1 # 1 form button press

    def send_pulse(sender, receiver, state):
        nonlocal high_pulses
        nonlocal low_pulses

        state_repr = "-high->" if state else "-low->"
        pulse = (sender, receiver, state)
        #print(f"{sender} {state_repr} {receiver}")

        pulses.append(pulse)

        if state:
            high_pulses += 1
        else:
            low_pulses += 1


    for b in broadcaster:
        send_pulse("broadcaster", b, False)

    while pulses:
        #print(pulses)
        pulse = pulses.pop(0)
        module = modules.get(pulse[1])
        if module is None:
            continue

        func, outputs = module

        ret_state = func.process(pulse[0], pulse[2])
        if ret_state is not None:
            for out in outputs:
                send_pulse(pulse[1], out, ret_state)

    return high_pulses, low_pulses

def smash_the_button(count:int):
    high = 0
    low = 0
    for _ in range(count):
        #print()
        h, l = push_button()
        high += h
        low += l

    
    print(high, low, high*low)
    return high*low

print(smash_the_button(1000))