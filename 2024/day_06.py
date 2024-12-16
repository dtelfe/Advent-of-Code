from aoc import aoc_read, time_solution
from copy import deepcopy
import os

DAY = 6
TEST = False
SPLIT_LINES = True

TURN = {
    (-1, 0): (0, 1),
    (1, 0): (0, -1),
    (0, 1): (1, 0),
    (0, -1): (-1, 0)
}
def find_start(data):
    for idx, row in enumerate(data):
        if "^" in row:
            return idx, row.index("^")

def get_value(data, cell, rows, columns):
    y = cell[0]
    x = cell[1]

    if x < 0 or x >= columns or y < 0 or y >= rows:
        return "OOB"
    return data[y][x]


def move(location, movement):
    return [l + m for l,m in zip(location, movement)]

def next_cell_move(data, location, movement, rows, columns):
    next_cell = move(location, movement)
    v = get_value(data, next_cell, rows, columns)
    move_map = {
        "#": "turn",
        ".": "move",
        "^": "move",
        "OOB": "exit"
    }
    return move_map[v]


@time_solution
def part_1(size_only=True):
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    ROWS = len(data)
    COLUMNS = len(data[0])
    location = find_start(data)
    history = []
    movement = [-1, 0]

    # k = 0
    while True:
        # k +=1
        if location not in history:
            history.append(tuple(location))
        
        move_type = next_cell_move(data, location, movement, ROWS, COLUMNS)
        if move_type == "move":
            location = move(location, movement)
        elif move_type == "turn":
            movement = TURN.get(tuple(movement))
        elif move_type == "exit":
            break
    
    if size_only:
        return len(set(history))
    else:
        return list(set(history))

def dprint(data):
    pdata = [''.join(row) for row in data]
    pdata = "\n" + "\n".join(pdata)
    print(pdata)


@time_solution
def part_2():
    # This takes almost 10 mins lol.
    # Timing for 'part_2': 589.225s


    # The obstruction must be placed on the the current path.
    full_history = part_1(False)
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    
    # Place obstruction anywhere but "^".
    # With the goal of getting stuck in a loop.
    location = find_start(data)
    start = deepcopy(location)
    

    
    loops = 0
    for obs in full_history:
        if obs == start:
            continue
        n_data = [["#" if [y, x] == obs else v for x, v in enumerate(row)] for y, row in enumerate(data)]
        n_data[obs[0]][obs[1]] = "#"
        location = find_start(data)
        history = []
        movement = [-1, 0]

        while True:
            loc_mov = tuple(list(location) + list(movement))
            if loc_mov in history:
                loops += 1
                break
            else:
                history.append(loc_mov)
            
            move_type = next_cell_move(n_data, location, movement)
            if move_type == "move":
                location = move(location, movement)
            elif move_type == "turn":
                movement = TURN.get(tuple(movement))
            elif move_type == "exit":
                break
    
    # Feels like we could so something with making a sort of rectangle from the corner locations
    # if the corner location is on p1 path?
    return loops
 

if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
