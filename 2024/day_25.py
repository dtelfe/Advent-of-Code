from aoc import aoc_read, time_solution
import numpy as np
from copy import copy, deepcopy

DAY = 25
TEST = False
SPLIT_LINES = True

def pp(grid):
    op = []
    for row in grid:
        op.append(''.join(row))
    print("\n".join(op))

def split_to_schematics(data):
    keys = []
    locks = []

    type = "n/a"
    current_schematic = []
    init = True
    for row in data:
        if row == []:
            init = True
            if type == "lock":
                locks.append(deepcopy(current_schematic))
            elif type == "key":
                keys.append(deepcopy(current_schematic))
            continue
        
        if init:
            current_schematic = []
            init = False
            if list(set(row)) == ["#"]:
                type = "lock"
            elif list(set(row)) == ["."]:
                type = "key"
            else:
                assert False
        current_schematic.append(row)
    return keys, locks

def calculate_height(grid):
    return [list(column).count("#") - 1 for column in np.transpose(grid)]

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)
    keys, locks = split_to_schematics(data)
    key_heights = [calculate_height(key) for key in keys]
    lock_heights = [calculate_height(lock) for lock in locks]

    successes = 0
    for key in key_heights:
        checks = [max([a + b for a, b in zip(key, lock)]) > 5 for lock in lock_heights]
        successes += checks.count(False)

    return successes

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    return 0


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
