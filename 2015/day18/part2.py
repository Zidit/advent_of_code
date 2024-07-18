
import copy

def is_on(grid, position, size):
    if position[0] < 0 or position[0] >= size:
        return 0
    if position[1] < 0 or position[1] >= size:
        return 0

    return grid[position[0]][position[1]]

def get_neighbors(grid, position, size):
    neighbors = 0
    neighbors += is_on(grid, (position[0] - 1, position[1] - 1), size)
    neighbors += is_on(grid, (position[0] - 1, position[1]    ), size)
    neighbors += is_on(grid, (position[0] - 1, position[1] + 1), size)

    neighbors += is_on(grid, (position[0]    , position[1] - 1), size)
    neighbors += is_on(grid, (position[0]    , position[1] + 1), size)

    neighbors += is_on(grid, (position[0] + 1, position[1] - 1), size)
    neighbors += is_on(grid, (position[0] + 1, position[1]    ), size)
    neighbors += is_on(grid, (position[0] + 1, position[1] + 1), size)

    return neighbors

def coners_on(grid):
    grid[0][0] = 1
    grid[0][-1] = 1
    grid[-1][0] = 1
    grid[-1][-1] = 1


def simulate(old_grid):
    new_grid = copy.deepcopy(old_grid)

    for y, row in enumerate(old_grid):
        for x, cell in enumerate(row):
            neighbors = get_neighbors(old_grid, (y,x), len(old_grid))
            if cell == 1:
                if neighbors == 2 or neighbors == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0

    coners_on(new_grid)
    return new_grid

def print_grid(grid):
    for row in grid:
        print(row)
    print()



grid = []

with open("input.txt") as input:
    for line in input:
        row = []
        for c in line:
            if c == "#":
                row.append(1)
            elif c == ".":
                row.append(0)
        grid.append(row)

coners_on(grid)

for i in range(100):
    grid = simulate(grid)
print_grid(grid)

lights_on = 0
for row in grid:
    for cell in row:
        if cell == 1:
            lights_on += 1

print (lights_on)
