
import math

input_map = []

with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        input_map.append(line.split()[0])

test_map0 = """
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
""".split()

test_map1 = """
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

def print_map(m):
    for l in m:
        print(l)
    print("")

def clear_map(m):
    for iy, y in enumerate(m):
        for ix, x in enumerate(y):
            if x != "#" and x != "." and x != "X":
                m[iy] = m[iy][:ix] + "." + m[iy][ix+1:]
    return m

def get_angle(pos_x, pos_y, target_x, target_y):
    delta_x = target_x - pos_x 
    delta_y = target_y - pos_y
    a = math.atan2(delta_x, -delta_y)
    ret = a if a >= 0 else math.tau + a

    return ret

def is_asteroid(m, x, y):
    return m[y][x] == "#"

def test_line_of_sight(m, pos_x, pos_y, target_x, target_y):
    delta_x = target_x - pos_x 
    delta_y = target_y - pos_y

    if delta_y == 0 and delta_x == 0:
        return False

    gcd = math.gcd(delta_x, delta_y)
    step_x = delta_x // gcd
    step_y = delta_y // gcd

    for i in range(1, gcd):
        if is_asteroid(m, step_x * i + pos_x, step_y * i + pos_y):
            return False        

    return True

def find_next(m, pos_x, pos_y, angle):
    best_x = 0
    best_y = 0
    smallest_angle = math.tau
    found = False

    for iy, y in enumerate(m):
        for ix, x in enumerate(y):
            if x != "#":
                continue
            
            if test_line_of_sight(m, pos_x, pos_y, ix, iy):
                a = get_angle(pos_x, pos_y, ix, iy)
                if a > angle and a < smallest_angle:
                    found = True
                    smallest_angle = a
                    best_x = ix
                    best_y = iy

    if found:
        return best_x, best_y, smallest_angle
    else:
        return None, None, None

def clear_asteroids(m, pos_x, pos_y, count, start_angle=-1):
    current_angle = start_angle
    for i in range(count):
        x, y, current_angle = find_next(m, pos_x, pos_y, current_angle)
        if x is None:
            x, y, current_angle = find_next(m, pos_x, pos_y, -1)
            if x is None:
                break

        current_angle %= math.tau
        m[y] = m[y][:x] + "." + m[y][x+1:]

    return x,y,m,current_angle

#print_map(input_map)
#print_map(test_map)

print(get_angle(0,0, 0, -1))
print(get_angle(0,0, 1, -1))
print(get_angle(0,0, 1, 0))
print(get_angle(0,0, 1, 1))
print(get_angle(0,0, 0, 1))
print(get_angle(0,0, -1, 1))
print(get_angle(0,0, -1, 0))
print(get_angle(0,0, -1, -1))


print_map(test_map0)
m = test_map0
_,_,m,a = clear_asteroids(m, 8, 3, 9)
print_map(m)
m = clear_map(m)
_,_,m,a = clear_asteroids(m, 8, 3, 9, a)
print_map(m)
m = clear_map(m)
_,_,m,a = clear_asteroids(m, 8, 3, 9, a)
print_map(m)
m = clear_map(m)
_,_,m,a = clear_asteroids(m, 8, 3, 9, a)
print_map(m)

print_map(test_map1)
x, y, test_map1, _ = clear_asteroids(test_map1, 11, 13, 200)
print_map(test_map1)
print(x,y)

x, y, input_map, _ = clear_asteroids(input_map, 23, 29, 200)
print(x*100 + y)
