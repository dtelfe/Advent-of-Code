from aoc import aoc_read, time_solution

DAY = 10
TEST = False
SPLIT_LINES = True

def find_zeros(data):
    coords = []

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "0":
                coords.append([y,x])
    return coords


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    ROWS = len(data) 
    COLUMNS = len(data[0])
    zeros = find_zeros(data)
    scores = {}
    for zero in zeros:
        scores[tuple(zero)] = 0
        visited = []
        next = [zero]
        visited.append(zero)
        while True:
            if next == []:
                # No more to search
                break
            current = next[0]

            # Check neighbours
            for dir in [[1,0], [-1,0], [0, 1], [0, -1]]:
                new = [a + b for a, b in zip(current, dir)]

                # Check bounds
                if new[0] < 0 or new[0] >= ROWS:
                    continue
                
                if new[1] < 0 or new[1] >= COLUMNS:
                    continue
                
                if new in visited:
                    continue

                # Get values
                c = data[current[0]][current[1]]
                v = data[new[0]][new[1]]

                # If the difference is 1, then add to list.
                # If the cell value is 9, then we dont want to look at neighbours.
                if int(v) - int(c) == 1 and int(v) != 9:
                    next.append(new)
                    visited.append(new)
                    continue
                
                if int(v) - int(c) == 1 and int(v) == 9:
                    scores[tuple(zero)] += 1
                    visited.append(new)
            
            next.pop(0)
    return sum(scores.values())


@time_solution
def part_2():
    # Copy part 1
    # Don't keep track of visited cells.
    # Change scores to keep the cells of value 9 and how many times hit.
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    ROWS = len(data) 
    COLUMNS = len(data[0])
    zeros = find_zeros(data)
    scores = {}
    for zero in zeros:
        next = [zero]
        while True:
            if next == []:
                # No more to search
                break
            current = next[0]

            # Check neighbours
            for dir in [[1,0], [-1,0], [0, 1], [0, -1]]:
                new = [a + b for a, b in zip(current, dir)]

                # Check bounds
                if new[0] < 0 or new[0] >= ROWS:
                    continue
                
                if new[1] < 0 or new[1] >= COLUMNS:
                    continue
            

                # Get values
                c = data[current[0]][current[1]]
                v = data[new[0]][new[1]]

                # If the difference is 1, then add to list.
                # If the cell value is 9, then we dont want to look at neighbours.
                if int(v) - int(c) == 1 and int(v) != 9:
                    next.append(new)
                    continue
                
                if int(v) - int(c) == 1 and int(v) == 9:
                    if tuple(new) not in scores:
                        scores[tuple(new)] = 0
                    scores[tuple(new)] += 1
            
            next.pop(0)
    return sum(scores.values())


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
