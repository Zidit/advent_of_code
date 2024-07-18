import time
import copy
from cProfile import Profile
from pstats import SortKey, Stats

input_file = "example.txt"
#input_file = "input.txt"

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
    #row = pos[0] % map_width
    #col = pos[1] % map_height

    if not (0 <= pos[0] < map_width):
        return False
    if not (0 <= pos[1] < map_height):
        return False

    row = pos[0]
    col = pos[1]
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
    odd_positions = set([start])
    for i in range(map_width + 2):
        odd_positions = step(odd_positions)
    even_positions = step(odd_positions)

    all_valid_positions = set([start])
    current_positions = set([start])

    edge_positions = set([start])


    for i in range(steps % map_width):
        edge_positions = step(edge_positions)
        #all_valid_positions = all_valid_positions.union(current_positions)
        #print(len(all_valid_positions), len(current_positions), len(all_valid_positions) - len(current_positions))

    Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

print("Even:", len(even_positions))
#print_map(map_data, even_positions)

print("Odd:", len(odd_positions))
#print_map(map_data, odd_positions)

print("Edge:", len(edge_positions))
#print_map(map_data, edge_positions)
print()

def grid_cout(x):
    if x == 0:
        return 0
    return 2*x*x - 2*x + 1

#for i in range(7):
#    print(i, grid_cout(i))

full_grids = grid_cout(steps//map_width)
print("Full grids:", steps//map_width, "->", full_grids)

print("Total even:", full_grids * len(even_positions) + len(edge_positions))
print("Total odds:", full_grids * len(odd_positions) + len(edge_positions))

#print(len(all_valid_positions), len(current_positions))
