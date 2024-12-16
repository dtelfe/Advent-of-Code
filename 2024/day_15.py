from aoc import aoc_read, time_solution
from copy import deepcopy
import time
import os

DAY = 15
TEST = False
SPLIT_LINES = True

MOVEMENT = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0)
}

def grid_print(grid):
    x = [''.join(row) for row in grid]
    y = "\n".join(x)
    y = y + "\n\n"
    print(y)

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)
    data_point = data.index([])
    
    grid = data[:data_point]
    grid = [row for row in grid if row != []]
    instructions = data[data_point:]
    instructions = [i for i in instructions if i != []]
    instructions = [instruction for row in instructions for instruction in row]
    
    # Get starting location
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == "@":
                current_loc = [y,x]

    for instruction in instructions:
        t = 1
        next_move = MOVEMENT.get(instruction)
        valid_move = False
        # Determine if the move is valid or not.
        while True:
            goal_loc = [coord + t * move for coord, move in zip(current_loc, next_move)]
            cell_value = grid[goal_loc[0]][goal_loc[1]]
            if cell_value == ".":
                valid_move = True
                break
            elif cell_value == "#":
                # The move is invalid as we have hit a blocker.
                break
            t +=1
        
        if valid_move:
            if t == 1:
                grid[current_loc[0]][current_loc[1]] = "."
                current_loc = goal_loc.copy()
                grid[current_loc[0]][current_loc[1]] = "@"

            if t > 1:
                # Go through the blocks to push in reverse order.
                # i.e The block moving into clean air will move first.
                stack = [[coord + j * move for coord, move in zip(current_loc, next_move)] for j in range(1, t+1)][::-1]
                for coord_to, coord_from in zip(stack, stack[1:]):
                    grid[coord_to[0]][coord_to[1]] = grid[coord_from[0]][coord_from[1]]
                grid[stack[-1][0]][stack[-1][1]] = "."

                grid[current_loc[0]][current_loc[1]] = "."
                current_loc = stack[-1].copy()
                grid[current_loc[0]][current_loc[1]] = "@"

            # print(f"{instruction=}\n--------")
            # grid_print(grid)


    # Total the boxes based on position / formula.
    total = 0
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == "O":
                total += 100 * y + x

    return total

def double_grid(grid):
    double_grid = []

    for row in grid:
        double_grid.append([])
        for value in row:
            double_grid[-1].append(value)
            double_grid[-1].append(value)

    # Cleanse it
    for y, row in enumerate(double_grid):
        str_row = ''.join(row).replace("OO", "[]").replace("@@", "@.")
        double_grid[y] = [*str_row]

    return double_grid

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)
    data_point = data.index([])

    grid = data[:data_point]
    grid = [row for row in grid if row != []]
    instructions = data[data_point:]
    instructions = [i for i in instructions if i != []]
    instructions = [instruction for row in instructions for instruction in row]

    # Alter the grid for part 2.
    grid = double_grid(grid)
    
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == "@":
                start = [y, x]
    
    current_loc = start

    for instruction in instructions:
        t = 1
        next_move = MOVEMENT.get(instruction)
        valid_move = False
        # Determine if the move is valid or not.
        # If we are moving left and right, use the logic as in p1.
        # For up and down we have to check for partial block overlaps.
        if next_move in [(0,1), (0,-1)]:
            while True:
                goal_loc = [coord + t * move for coord, move in zip(current_loc, next_move)]
                cell_value = grid[goal_loc[0]][goal_loc[1]]
                if cell_value == ".":
                    valid_move = True
                    break            
                elif cell_value == "#":
                    break
                t +=1
            if valid_move:
                if t == 1:
                    grid[current_loc[0]][current_loc[1]] = "."
                    current_loc = goal_loc.copy()
                    grid[current_loc[0]][current_loc[1]] = "@"

                if t > 1:
                    # Go through the blocks to push in reverse order.
                    # i.e The block moving into clean air will move first.
                    stack = [[coord + j * move for coord, move in zip(current_loc, next_move)] for j in range(1, t+1)][::-1]
                    for coord_to, coord_from in zip(stack, stack[1:]):
                        grid[coord_to[0]][coord_to[1]] = grid[coord_from[0]][coord_from[1]]
                    grid[stack[-1][0]][stack[-1][1]] = "."

                    grid[current_loc[0]][current_loc[1]] = "."
                    current_loc = stack[-1].copy()
                    grid[current_loc[0]][current_loc[1]] = "@"

        # Vertical direction update logic
        if next_move in [(-1,0), (1,0)]:               
            # Keep track of the various layers in dictionary.
            shifts_required = {}            
            shift_locs = [current_loc]
            all_shift_locs = []
            all_shift_locs.append(deepcopy(shift_locs))
            # replace use of current location with each cell moving up.
            while True:
                shifts_required[t] = {}

                goal_locs = []
                for loc in shift_locs:
                    goal_loc = [coord + movement for coord, movement in zip(loc, next_move)]
                    goal_locs.append(goal_loc)
                
                for start, end in zip(shift_locs, goal_locs):
                    # Keep track of where each cell would move to if its valid.
                    shifts_required[t][tuple(start)] = end
                
                # Prepare to store another layer of cells that need to be checked
                next_shift_locs = []
                cell_values = [grid[goal_loc[0]][goal_loc[1]] for goal_loc in goal_locs]                   

                if all([value == "." for value in cell_values]):
                    # All the blocks can move, so okay.
                    valid_move = True
                    break
                elif any([value == "#" for value in cell_values]):
                    # One of the blocks has hit a wall so cannot move.
                    break
                
                for loc, value in zip(goal_locs, cell_values):
                    # If we encounter [ or ], then ensure we have the other half of the box in the next locations.
                    if value in ["[", "]"]:
                        # If we hit the left side of the box, the add the right etc.
                        other_dir = {"[": [0,1], "]": [0, -1]}.get(value)

                        next_shift_locs.append(loc)
                        other_half = [coord + move for coord, move in zip(loc, other_dir)]
                        if other_half not in next_shift_locs:
                            next_shift_locs.append(deepcopy(other_half))

                shift_locs = deepcopy(next_shift_locs)
                all_shift_locs.append(shift_locs)
                t +=1

            if valid_move:
                # Go through the blocks to push in reverse order.
                # i.e The block moving into clean air will move first.
                for key in list(shifts_required.keys())[::-1]:
                    move_pair = shifts_required[key]
                    for coord_from, coord_to in move_pair.items():
                        grid[coord_to[0]][coord_to[1]] = grid[coord_from[0]][coord_from[1]]
                        grid[coord_from[0]][coord_from[1]] = "."
                
                
                # Move the robot.
                previous_loc = list(shifts_required[1].keys())[0]
                grid[previous_loc[0]][previous_loc[1]] = "."

                current_loc = list(shifts_required[1].values())[0].copy()
                grid[current_loc[0]][current_loc[1]] = "@"
                
    # Print final grid for test checking.
    # grid_print(grid)

    # Total the boxes based on position / formula.
    total = 0
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == "[":
                total += 100 * y + x

    return total

if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
