from aoc import aoc_read, time_solution
from copy import deepcopy

DAY = 16
TEST = False
SPLIT_LINES = True

MOVE_DIRS= [[1,0], [-1,0], [0,1], [0,-1]]

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    # Find start and end.
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == "S":
                start = [y,x]
            elif value == "E":
                end = [y,x]
    
    current_location = start
    current_direction = [0,1]

    SHORTEST = {}
    SHORTEST[tuple(start + current_direction)] = 0
    move_queue = [start + current_direction]

    while True:
        if move_queue == []:
            break
        
        # Get the first element from the queue.
        loc_dir = move_queue[0]
        del move_queue[0]

        current_location = loc_dir[:2]
        current_direction = loc_dir[2:]

        last_move = tuple(current_location + current_direction)
        for move in MOVE_DIRS:
            neighbour = [coord + move for coord, move in zip(current_location, move)]
            nb_value = data[neighbour[0]][neighbour[1]]
            
            # If its turning around, ignore it.
            if [m + cd for m, cd in zip(move, current_direction)] == [0, 0]:
                continue

            if nb_value == "#":
                continue

            next_move = tuple(neighbour + move)
            # Allow turning and moving at the same time.
            # Hence, if the move and current direction differ then add 1000 extra.
            if next_move not in SHORTEST:
                if move == current_direction:
                    SHORTEST[next_move] = SHORTEST[last_move] + 1
                    move_queue.append(list(next_move))
                else:
                    SHORTEST[next_move] = SHORTEST[last_move] + 1000 + 1
                    move_queue.append(list(next_move))
            elif next_move in SHORTEST:
                if move == current_direction and SHORTEST[next_move] > SHORTEST[last_move] + 1:
                    SHORTEST[next_move] = SHORTEST[last_move] + 1
                    move_queue.append(list(next_move))
                elif SHORTEST[next_move] > SHORTEST[last_move] + 1000 + 1:
                    SHORTEST[next_move] = SHORTEST[last_move] + 1000 + 1
                    move_queue.append(list(next_move))

    end_point_keys = [key for key in SHORTEST if list(key)[:2] == end]
    end_point_scores = [SHORTEST.get(key) for key in end_point_keys]
    return min(end_point_scores)


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    # Find start and end.
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == "S":
                start = [y,x]
            elif value == "E":
                end = [y,x]
    
    current_location = start
    current_direction = [0,1]

    # Keep track of shortest path value to each point (score).
    SHORTEST = {}
    SHORTEST[tuple(start + current_direction)] = 0

    # Keep track of previous node that gave the smallest score to arrive at current node.
    PREV_NODES = {}
    PREV_NODES[tuple(start + current_direction)] = []

    move_queue = [start + current_direction]

    while True:
        if move_queue == []:
            break
        
        # Get the first element from the queue.
        loc_dir = move_queue[0]
        del move_queue[0]

        current_location = loc_dir[:2]
        current_direction = loc_dir[2:]

        last_move = tuple(current_location + current_direction)
        for move in MOVE_DIRS:
            neighbour = [coord + move for coord, move in zip(current_location, move)]
            nb_value = data[neighbour[0]][neighbour[1]]
            
            # If its turning around, ignore it.
            if [m + cd for m, cd in zip(move, current_direction)] == [0, 0]:
                continue
        
            if nb_value == "#":
                continue

            next_move = tuple(neighbour + move)

            # Differ from p1. Split out moves and rotations.
            # If the move direction match, the do the move.
            if move == current_direction:
                if next_move not in SHORTEST:
                    move_queue.append(list(next_move))
                    PREV_NODES[next_move] = [last_move]
                    SHORTEST[next_move] = SHORTEST[last_move] + 1    
                elif move == current_direction and SHORTEST[next_move] > SHORTEST[last_move] + 1:
                    SHORTEST[next_move] = SHORTEST[last_move] + 1
                    PREV_NODES[next_move] = [last_move]
                    move_queue.append(list(next_move))
                elif move == current_direction and SHORTEST[next_move] == SHORTEST[last_move] + 1:
                    PREV_NODES[next_move] = PREV_NODES[next_move] + [last_move]
            else:
                # If the move directions don't match. Then rotate on the spot.
                updated_current = tuple(current_location + move)
                if updated_current not in SHORTEST:
                    move_queue.append(list(updated_current))
                    SHORTEST[updated_current] = SHORTEST[last_move] + 1000
                    PREV_NODES[updated_current] = [last_move]
                elif SHORTEST[updated_current] > SHORTEST[last_move] + 1000:
                    move_queue.append(list(updated_current))
                    SHORTEST[updated_current] = SHORTEST[last_move] + 1000
                    PREV_NODES[updated_current] = [last_move]
                elif SHORTEST[updated_current] == SHORTEST[last_move] + 1000:
                    PREV_NODES[updated_current] = PREV_NODES[updated_current] + [last_move]

            
    end_point_keys = [key for key in SHORTEST if list(key)[:2] == end]
    end_point_scores = [SHORTEST.get(key) for key in end_point_keys]

    # Find all ending keys which have the best score.
    winning_keys = [key for key in end_point_keys if SHORTEST.get(key) == min(end_point_scores)]

    # Use PREV_NODES to start at the winning spots, and step backwards through the path
    # to retrace all of the best paths.
    # For best paths, keep track of location only (and forget about direction).
    key_queue = winning_keys.copy()
    all_seats = []
    while True:
        if key_queue == []:
            break

        loc_dir = key_queue[0]
        del key_queue[0]

        if loc_dir[:2] not in all_seats:
            all_seats.append(loc_dir[:2])
        
        previous = PREV_NODES.get(loc_dir)
        key_queue = key_queue + previous
        
    # Make a copy of the data, and update a visual to see if test case is correct.
    # grid = deepcopy(data)
    # for loc in all_seats:
    #     grid[loc[0]][loc[1]] = "O"
    # grid_print(grid)

    # Return the cells on the best paths.
    return len(all_seats)

def grid_print(grid):
    x = [''.join(row) for row in grid]
    y = "\n".join(x)
    y = y + "\n\n"
    print(y)

if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
