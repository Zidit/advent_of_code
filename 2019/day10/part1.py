
import math

input_map = []

with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        input_map.append(line.split()[0])

test_map0 = """
.#..#
.....
#####
....#
...##
""".split()

test_map1 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""".split()

test_map2 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""".split()

test_map3 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""".split()

test_map4 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""".split()


def is_asteroid(m, x, y):
    return m[y][x] == "#"

def test_line_of_sight(m, pos_x, pos_y, target_x, target_y):
    delta_x = target_x - pos_x 
    delta_y = target_y - pos_y

    gcd = math.gcd(delta_x, delta_y)
    step_x = delta_x // gcd
    step_y = delta_y // gcd

    for i in range(1, gcd):
        if is_asteroid(m, step_x * i + pos_x, step_y * i + pos_y):
            return False        

    return True

def count_visible_asteroids(m, pos_x, pos_y):
    count = 0
    for iy, y in enumerate(m):
        for ix, x in enumerate(y):
            if ix == pos_x and iy == pos_y:
                continue
            if x == ".":
                continue

            if test_line_of_sight(m, pos_x, pos_y, ix, iy):
                count += 1

    return count

def find_best(m):
    best_x = 0
    best_y = 0
    best_count = 0

    for iy, y in enumerate(m):
        for ix, x in enumerate(y):
            if x == ".":
                continue
            count = count_visible_asteroids(m, ix, iy)
            if count > best_count:
                best_count = count
                best_x = ix
                best_y = iy

    return best_x, best_y, best_count


#print(input_map)
#print(test_map1)

#print(test_line_of_sight(test_map0, 3, 4, 1, 0))
#print(count_visible_asteroids(test_map0, 3, 4)) # == 8
#print(count_visible_asteroids(test_map1, 5, 8)) # == 33
#print(count_visible_asteroids(test_map2, 1, 2)) # == 35
#print(count_visible_asteroids(test_map3, 6, 3)) # == 41
#print(count_visible_asteroids(test_map4, 11, 13)) # == 210

print(find_best(test_map0)) # == 3, 4, 8
print(find_best(test_map1)) # == 5, 8, 33
print(find_best(test_map2)) # == 1, 2, 35
print(find_best(test_map3)) # == 6, 3, 41
print(find_best(test_map4)) # == 11, 13, 210

print(find_best(input_map))

