"""AoC 2024 - Solution - Day xx"""

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

MOVE_MAP = {
        "#": "turn",
        ".": "move",
        "^": "move",
        "OOB": "exit"
    }

def find_start(data):
    for idx, row in enumerate(data):
        if "^" in row:
            return (idx, row.index("^"))

def get_value(data, cell, rows, columns):
    y = cell[0]
    x = cell[1]

    if x < 0 or x >= columns or y < 0 or y >= rows:
        return "OOB"
    return data[y][x]


def move(location, movement):
    return tuple(coord_loc + coord_move for coord_loc, coord_move in zip(location, movement))

def next_cell_move(data, location, movement, rows, columns):
    next_cell = move(location, movement)
    v = get_value(data, next_cell, rows, columns)
    return MOVE_MAP[v], next_cell


@time_solution
def part_1(size_only=True):
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    ROWS = len(data)
    COLUMNS = len(data[0])
    location = find_start(data)
    full_history = {}
    movement = (-1, 0)

    while True:
        location_movement = (location, movement)

        if full_history.get(location, -1) == -1:
            # i.e. if t_loc not present in full history, add this location and move.
            # This keeps track of the first time entering a cell.
            full_history[location_movement] = 0
        full_history[location] = 1
        
        
        move_type, next_cell = next_cell_move(data, location, movement, ROWS, COLUMNS)
        if move_type == "move":
            location = next_cell
        elif move_type == "turn":
            movement = TURN.get(tuple(movement))
        elif move_type == "exit":
            break
    
    if size_only:
        distinct_positions = [key for key, value in full_history.items() if value == 1]
        return len(distinct_positions)
    full_history = [key for key, value in full_history.items() if value == 0]
    return full_history

def dprint(data):
    pdata = [''.join(row) for row in data]
    pdata = "\n" + "\n".join(pdata)
    print(pdata)


@time_solution
def part_2():
    full_history = part_1(False)
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    location = find_start(data)
    start = deepcopy(location)
    ROWS = len(data)
    COLUMNS = len(data[0])

    loops = 0
    for new_start, block in zip(full_history, full_history[1:]):
        if block[0] == start:
            continue
        
        location = new_start[0]
        history = set()
        movement = new_start[1]

        while True:
            loc_move = (location, movement)
            if loc_move in history:
                loops += 1
                break
            else:
                history.add(loc_move)
            
            move_type, next_cell = next_cell_move(data, location, movement, ROWS, COLUMNS)
            if move_type == "move" and next_cell != block[0]:
                location = next_cell
            elif move_type == "turn" or next_cell == block[0]:
                movement = TURN.get(movement)
            elif move_type == "exit":
                break
    return loops
 

if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
