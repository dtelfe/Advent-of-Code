from aoc import aoc_read, time_solution
import time
import os

DAY = 14
TEST = False
SPLIT_LINES = False

ORTHOGONAL_DIAGONAL_DIRECTIONS = [[0,1], [0, -1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
ORTHOGONAL_DIRECTIONS = [[0,1], [0, -1], [1,0], [-1,0]]

@time_solution
def part_1():
    if TEST:
        WIDTH = 11
        HEIGHT = 7
    else:
        WIDTH = 101
        HEIGHT = 103
    TIME = 100

    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.replace("p=","").replace("v=","").split(" ") for row in data]

    # Find position of all after 100 seconds.
    # [x,y]
    finals = {}
    for positions, velocities in data: 
        positions = [int(x) for x in positions.split(",")]
        velocities = [int(x) for x in velocities.split(",")]
        final_pos = [p + TIME*v for p, v in zip(positions, velocities)]
        final_pos = [final_pos[0] % WIDTH, final_pos[1] % HEIGHT]
        
        store_pos = tuple(final_pos)
        if store_pos in finals:
            finals[store_pos] +=1
        else:
            finals[store_pos] = 1

    # Finals -> Quadrants
    mid_x = WIDTH // 2
    mid_y = HEIGHT // 2

    q1, q2, q3, q4 = 0, 0, 0, 0
    for position, count in finals.items():

        if position[0] < mid_x and position[1] < mid_y:
            q1 += count
    
        if position[0] > mid_x and position[1] < mid_y:
            q2 += count

        if position[0] < mid_x and position[1] > mid_y:
            q3 += count
        
        if position[0] > mid_x and position[1] > mid_y:
            q4 += count

    # print([q1, q2, q3, q4])
    return q1 * q2 * q3 * q4

def plot(width, height, robot_positions):
    ROW = ["."] * width
    grid = []
    for _ in range(height):
        grid += [ROW.copy()]

    for position, value in robot_positions.items():
        if value > 9:
            d = "#"
        else:
            d = str(value)
        x = position[1]
        y = position[0]
        grid[x][y] = d
    drawing = '\n'.join([''.join(row) for row in grid])
    os.system('cls')

    print(f"\n{drawing}")
    return None

def locations_at(data, time, width, height):
    finals = {}
    for positions, velocities in data: 
        positions = [int(x) for x in positions.split(",")]
        velocities = [int(x) for x in velocities.split(",")]
        final_pos = [p + time*v for p, v in zip(positions, velocities)]
        final_pos = [final_pos[0] % width, final_pos[1] % height]
        
        store_pos = tuple(final_pos)
        if store_pos in finals:
            finals[store_pos] +=1
        else:
            finals[store_pos] = 1
    return finals


@time_solution
def part_2():
    if TEST:
        WIDTH = 11
        HEIGHT = 7
    else:
        WIDTH = 101
        HEIGHT = 103
    

    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.replace("p=","").replace("v=","").split(" ") for row in data]
    data = data

    # Keep track of the potential times for faster reruns.
    maybe = [] 
    for t in range(0, 10000):
        # Print indicator of progress.
        if t % 100 == 0: print(t)
        locations = locations_at(data, t, WIDTH, HEIGHT)
        loc_values = [value for value in locations.keys()]

        nb_count = 0
        # For each of the plotted points, check to see if it has neighbours plotted.
        # As to draw a picture, i expect lots of continuous lines.
        for loc in loc_values:
            search = True
            for dir in ORTHOGONAL_DIRECTIONS:
                if not search:
                    continue
                if tuple([a + b for a, b in zip(loc, dir)]) in loc_values:
                    nb_count += 1
                    search = True
        
        # First found using 0.5, but this prints many non-trees.
        if nb_count >= 0.9 * len(loc_values):
            maybe.append(t)
            plot(WIDTH, HEIGHT, locations)
            print(f"\n {t}")
    return maybe

if __name__ == "__main__":

    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
