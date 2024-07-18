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
map_width = len(map_data[0])
map_height = len(map_data)

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


def is_garden_plot(pos):
    row = pos[0] % map_width
    col = pos[1] % map_height

    #if not (0 <= pos[0] < map_width):
    #    return False
    #if not (0 <= pos[1] < map_height):
    #    return False

    #row = pos[0]
    #col = pos[1]
    return map_data[row][col] == "."

def step(positions):
    new_positions = set()

    def test_step(cur_pos, delta_pos):
        new_pos = (cur_pos[0] + delta_pos[0], cur_pos[1] + delta_pos[1])
        if is_garden_plot(new_pos):
            new_positions.add(new_pos)

    for pos in positions:
        test_step(pos, (0,1))
        test_step(pos, (0,-1))
        test_step(pos, (1,0))
        test_step(pos, (-1,0))

    return new_positions


#print_map(map_data, current_positions)
print("Start", start)
print(map_width, map_height)
steps = 26501365
steps = 100

with Profile() as profile:
    positions = set([start])
    for i in range(1,4):
        for _ in range(map_width):
            positions = step(positions)

        print(i, "->", len(positions))


    Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

