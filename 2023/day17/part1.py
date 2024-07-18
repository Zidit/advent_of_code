
import dataclasses
import time
import math
from cProfile import Profile
from pstats import SortKey, Stats
import os
from operator import itemgetter

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]
map_data = [[int(x) for x in y] for y in data]

def print_map(map:list[str]):
    for l in map:
        print("".join([str(x) for x in l]), flush=False)
    print(flush=True)

#print_map(map_data)

@dataclasses.dataclass
class astar_item:
    pos:tuple[int,int,int,int]
    parent:tuple[int,int,int]
    g:int
    f:int


def print_astart_map(open_list:list[astar_item], closed_list:list[astar_item], map_data:list[list[int]]):
    #os.system('cls')
    new_map = [["."]*len(y) for y in map_data]

    for n in closed_list:
        new_map[n.pos[1]][n.pos[0]] = "#"

    for n in open_list:
        new_map[n.pos[1]][n.pos[0]] = "*"

    print_map(new_map)

def astar(start:tuple[int,int], end:tuple[int,int], map_data:list[list[int]]):

    map_width = len(map_data[0])
    map_height = len(map_data)


    def get_route(closed_list:dict[astar_item], end:astar_item):
        route = [end]
        while n := closed_list.get(route[-1].parent):
            route.append(n)
        return route

    def get_neighbor(node:astar_item, d:tuple[int,int]):
        cont = node.pos[2] + 1 if node.pos[3] == d else 1

        if not (0 <= cont < 4):
            return None

        if d == 1:
            new_pos = (node.pos[0] + 1, node.pos[1], cont, d)
        if d == 2:
            new_pos = (node.pos[0] - 1, node.pos[1], cont, d)
        if d == 3:
            new_pos = (node.pos[0], node.pos[1] + 1, cont, d)
        if d == 4:
            new_pos = (node.pos[0], node.pos[1] - 1, cont, d)

        if not (0 <= new_pos[0] < map_width):
            return None
        if not (0 <= new_pos[1] < map_height):
            return None

        n = astar_item(new_pos, node.pos, node.g, 0)
        if node.parent and n.pos[0] == node.parent[0] and n.pos[1] == node.parent[1]:
            return None

        return n

    def dist(start:tuple[int,int,int], end:tuple[int,int]):
        #return 0
        return end[0] - start[0] + end[1] - start[1]

    def pop_best_candidate(open_list:dict[tuple, astar_item]):
        best_f = 1000000
        best = None
        for k, v in open_list.items():
            if v.f < best_f:
                best_f = v.f
                best = (k,v)

        if best is not None:
            del open_list[best[0]]
        return best


    first_key = (*start, 0, 0)
    first_node = astar_item(first_key, None, 0, dist(first_key, end))

    open_list:dict[tuple, astar_item] = {first_node.pos: first_node}
    closed_list:dict[tuple, astar_item] = {}

    i = 0
    while open_list:

        #i += 1
        #if i % 10000 == 0:
        #    print_astart_map(open_list.values(), closed_list.values(), map_data)

        _, q = pop_best_candidate(open_list)
        closed_list[q.pos] = q

        neighbors = [
            get_neighbor(q, 1),
            get_neighbor(q, 2),
            get_neighbor(q, 3),
            get_neighbor(q, 4),
        ]

        for n in neighbors:
            #Make surethe node is valid
            if n is None:
                continue

            #Calculate the new cost
            cost = map_data[n.pos[1]][n.pos[0]]
            n.g += cost
            if cost == 0:
                continue

            #Return if we found the end
            if (n.pos[0], n.pos[1]) == end:
                closed_list[n.pos] = n
                return get_route(closed_list, n)[::-1]

            h = dist(n.pos, end)
            n.f = h + n.g

            if old_n := closed_list.get(n.pos):
                if old_n.g > n.g:
                    closed_list[n.pos] = n

            elif old_n := open_list.get(n.pos):
                if old_n.g > n.g:
                    open_list[n.pos] = n

            else:
                open_list[n.pos] = n



with Profile() as profile:
    end = (len(map_data[0]) - 1, len(map_data) - 1)
    #end = (20,20)
    path = astar((0,0), end, map_data)
    Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

#print()
#for l in path:
#    print(l)

print()
print_astart_map([], path, map_data)
print("Heat loss:", path[-1].g)

path_xy = [(p.pos[0],p.pos[1]) for p in path ]
#print(path_xy)

#total = 0
#for x,y in path_xy[1:]:
#    total += map_data[y][x]
#print(total)
