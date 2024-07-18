import time
import copy
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]
map_data = [[x for x in y] for y in data]


for ri, row in enumerate(map_data):
    for ci, col in enumerate(row):
        if col == "S": 
            start = (ri, ci)
            map_data[ri][ci] = "."


def print_map(map:list[str], positions=set()):
    new_map = copy.deepcopy(map)
    for p in positions:
        new_map[p[0]][p[1]] = "O"

    for l in new_map:
        print("".join([str(x) for x in l]), flush=False)
    print(flush=True)



current_positions = set([start])

def step():
    new_positions = set()

    def test_step(cur_pos, delta_pos):
        new_pos = tuple(map(sum, zip(cur_pos, delta_pos)))
        if map_data[new_pos[0]][new_pos[1]] == "#":
            return
        
        new_positions.add(new_pos)

    for pos in current_positions:
        test_step(pos, (0,1))
        test_step(pos, (0,-1))
        test_step(pos, (1,0))
        test_step(pos, (-1,0))

    return new_positions


print_map(map_data, current_positions)
print("Start", start)

for i in range(64):
    current_positions = step()
    #print_map(map_data, current_positions)
print_map(map_data, current_positions)
print(len(current_positions))
