
class moon():
    def __init__(self, x, y, z):
        self.pos = [x,y,z]
        self.vel = [0,0,0]

    def update_gravity(self, other):
        for i in range(3):
           if self.pos[i] < other.pos[i]:
               self.vel[i] += 1
           elif self.pos[i] > other.pos[i]:
               self.vel[i] -= 1

    def update_position(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

    def get_energy(self):
        pot = sum([abs(v) for v in self.pos]) 
        kin = sum([abs(v) for v in self.vel]) 
        return pot * kin

    def get_state(self):
        return tuple(self.pos) + tuple(self.vel)

    def __str__(self):
        return f"{self.pos=}, {self.vel=}"

    def __hash__(self):
        return hash(self.get_state())


test_moons = [
"<x=-1, y=0, z=2>",
"<x=2, y=-10, z=-7>",
"<x=4, y=-8, z=8>",
"<x=3, y=5, z=-1>",
]

test_moons2 = [
"<x=-8, y=-10, z=0>",
"<x=5, y=5, z=10>",
"<x=2, y=-7, z=3>",
"<x=9, y=-8, z=-3>",
]

input_moons = [
"<x=1, y=3, z=-11>",
"<x=17, y=-10, z=-8>",
"<x=-1, y=-15, z=2>",
"<x=12, y=-4, z=-4>",
]

moons = []
states = []
hashs = []

for line in input_moons:
    part = line.strip("<>").split(",")
    axis = [int(p.strip(" xyz=")) for p in part]
    moons.append(moon(axis[0], axis[1], axis[2]))

for i in range(1000000000):
    #print("Loop: ", i)
    for moon in moons:
        for moon2 in moons:
            if moon is not moon2:
                moon.update_gravity(moon2)

    for moon in moons:
        moon.update_position()

    state = ()
    for m in moons:
        state += m.get_state()

    h = hash(state)

    #if state in states:
    #    print(i)
    #    break

    if h in hashs:
        prev = hashs.index(h)
        print(f"Hash match: {prev}, {i}")
        if state == states[prev]:
            print(f"Status match: {prev}, {i}")
            break

    hashs.append(h)
    states.append(state)

    #for moon in moons:
        #print(moon)

    #print("")

