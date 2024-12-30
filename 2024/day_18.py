from aoc import aoc_read, time_solution

DAY = 18
TEST = False
SPLIT_LINES = False

if TEST:
    WIDTH = 6 + 1
    HEIGHT = 6 + 1
    SECONDS = 12
else:
    WIDTH = 70 + 1
    HEIGHT = 70 + 1 
    SECONDS = 1024

DIRECTIONS = [[1,0], [-1,0], [0,1], [0,-1]]

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.split(",") for row in data]

    start = [0,0]
    end = [HEIGHT-1, WIDTH-1] # [y,x] -> so flip coords

    row = [*"."*WIDTH]
    grid = [row.copy() for _ in range(HEIGHT)]

    
    for byte_x, byte_y in data[:SECONDS]:
        grid[int(byte_y)][int(byte_x)] = "#"
    
    queue = [start]
    history = {tuple(start): 0}
    while True:
        if queue == []:
            break

        coord_pair = queue[0]
        del queue[0]

        options = [[coord + dir for coord, dir in zip(coord_pair, move_dir)] for move_dir in DIRECTIONS]

        for option in options:
            if option[0] < 0 or option[0] >= HEIGHT:
                continue
            if option[1] < 0 or option[1] >= WIDTH:
                continue
            if tuple(option) in history.keys():
                continue
            if grid[option[0]][option[1]] != ".":
                continue
        
            queue.append(option)
            history[tuple(option)] = history[tuple(coord_pair)] + 1
            if option == end:
                return history[tuple(option)]
    return 0

def solve(data, seconds):
    start = [0,0]
    end = [HEIGHT-1, WIDTH-1] # [y,x] -> so flip coords

    row = [*"."*WIDTH]
    grid = [row.copy() for _ in range(HEIGHT)]

    
    for byte_x, byte_y in data[:seconds]:
        grid[int(byte_y)][int(byte_x)] = "#"
    
    queue = [start]
    history = {tuple(start): 0}
    while True:
        if queue == []:
            break

        current = queue[0]
        del queue[0]

        options = [[coord + dir for coord, dir in zip(current, move_dir)] for move_dir in DIRECTIONS]

        for option in options:
            if option[0] < 0 or option[0] >= HEIGHT:
                continue
            if option[1] < 0 or option[1] >= WIDTH:
                continue
            if tuple(option) in history.keys():
                continue
            if grid[option[0]][option[1]] != ".":
                continue
        
            queue.append(option)
            history[tuple(option)] = history[tuple(current)] + 1
            if option == end:
                return history[tuple(option)]
    
    # If we cant get to the end, return 0.     
    return 0

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.split(",") for row in data]

    min = 0
    max = len(data)
    while min < max:
        search = (max + min)//2
        exit_steps = solve(data, search)
        if exit_steps == 0:
            max = search - 1
        elif exit_steps > 0:
            solution = search
            min = search + 1

    return ",".join(data[solution])


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
