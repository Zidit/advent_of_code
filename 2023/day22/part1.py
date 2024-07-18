import time
import copy
from cProfile import Profile
from pstats import SortKey, Stats
import dataclasses


@dataclasses.dataclass
class point():
    x:int
    y:int
    z:int

class brick():
    def __init__(self, p1:point, p2:point, name:str=None) -> None:
        self.p1 = p1
        self.p2 = p2
        self.name = name

    def __repr__(self) -> str:
        name = self.name or ""
        return f"{name}({self.p1.x},{self.p1.y},{self.p1.z} - {self.p2.x},{self.p2.y},{self.p2.z})"

    def move_down(self):
        self.p1.z -= 1
        self.p2.z -= 1

    def move_up(self):
        self.p1.z += 1
        self.p2.z += 1

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]


bricks = []
for i, line in enumerate(data):
    p1, p2 = line.split("~")
    p1 = p1.split(",")
    p2 = p2.split(",")

    p1 = point(*map(int, p1))
    p2 = point(*map(int, p2))

    #c = "ABCDEFGHIJ"
    #bricks.append(brick(p1, p2, c[i]))
    bricks.append(brick(p1, p2, str(i)))


bricks.sort(key=lambda x: x.p1.z)

#for b in bricks:
#    print(b)

def check_collision(b1:brick, b2:brick):
    if not (b1.p1.z <= b2.p2.z and b1.p2.z >= b2.p1.z):
        return False
    if not (b1.p1.x <= b2.p2.x and b1.p2.x >= b2.p1.x):
        return False
    if not (b1.p1.y <= b2.p2.y and b1.p2.y >= b2.p1.y):
        return False

    return True


def get_colliding_bricks(b1:brick):
    colliding_bricks = []
    for b2 in bricks:
        if b1 is b2:
            continue

        if check_collision(b1, b2):
            colliding_bricks.append(b2)

    return colliding_bricks


def lower_brick(b1:brick):
    while b1.p1.z > 1:

        b1.move_down()

        for b2 in bricks:
            if b1 is b2:
                continue

            if check_collision(b1, b2):
                b1.move_up()
                return


with Profile() as profile:


    print("Dropping")
    for b1 in bricks:
        lower_brick(b1)
            
    print("Check support")
    total = 0
    for b1 in bricks:
        b1.move_up()
        supported_bricks = get_colliding_bricks(b1)
        b1.move_down()

        can_be_disintegrated = True
        for b in supported_bricks:
            b.move_down()
            supporting_bricks = get_colliding_bricks(b)
            b.move_up()
            if len(supporting_bricks) < 2:
                can_be_disintegrated = False
                break
        
        if can_be_disintegrated:
            total += 1
            #print("can_be_disintegrated", b1)

        #print(b1, supported_bricks)
            
    Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

    print(total)