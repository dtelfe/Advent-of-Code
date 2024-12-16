from aoc import aoc_read, time_solution
from math import gcd

DAY = 8
TEST = False
SPLIT_LINES = True


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    freqs = [item for row in data for item in row if item != "."]
    freqs = list(set(freqs))
    antennas = {f: [] for f in freqs}

    COLS = len(data[0])
    ROWS = len(data)
    for y in range(ROWS):
        for x in range(COLS):
            if data[y][x] in freqs:
                antennas[data[y][x]].append([y,x])

    anti_nodes = []

    for ops in antennas.values():
        if len(ops) == 1:
            continue

        # For each pair of nodes.
        # Create the line of points that are on the map.
        # Check the distance satisfies the condition.
        for idx, ant_1 in enumerate(ops):
            for ant_2 in ops[idx+1:]:
                diff = [x - y for x, y in zip(ant_1, ant_2)]
                diff = [int(y / gcd(*diff)) for y in diff]
                line_pts = []
                k = 0
                while True:
                    fails = 0
                    p_point = [a + k*b for a, b in zip(ant_1, diff)]
                    n_point = [a - k*b for a, b in zip(ant_1, diff)]
                    for point in [p_point, n_point]:
                        if (point[0] < 0 or point[0] >= ROWS) or (point[1] < 0 or point[1] >= COLS):
                            fails +=1
                        else:
                            if point not in line_pts:
                                line_pts.append(point)

                    if fails == 2:
                        break
                    k+=1
                dist_1 = [[a - b for a, b in zip(ant_1, point)] for point in line_pts]
                dist_2 = [[a - b for a, b in zip(ant_2, point)] for point in line_pts]

                two_dist_1 = [[x*2 for x in point] for point in dist_1]
                two_dist_2 = [[x*2 for x in point] for point in dist_2]

                for point, d1, d2 in zip(line_pts, dist_1, two_dist_2):
                    if d1 != d2:
                        continue
                    if point not in anti_nodes:
                        anti_nodes.append(point)

                for point, d1, d2 in zip(line_pts, two_dist_1, dist_2):
                    if d1 != d2:
                        continue
                    if point not in anti_nodes:
                        anti_nodes.append(point)

    return len(anti_nodes)

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    freqs = [item for row in data for item in row if item != "."]
    freqs = list(set(freqs))
    antennas = {f: [] for f in freqs}

    COLS = len(data[0])
    ROWS = len(data)
    for y in range(ROWS):
        for x in range(COLS):
            if data[y][x] in freqs:
                antennas[data[y][x]].append([y,x])

    anti_nodes = []

    for ops in antennas.values():
        if len(ops) == 1:
            continue

        # For each pair of nodes.
        # Create the line of points that are on the map.
        # Check the distance satisfies the condition.
        for idx, ant_1 in enumerate(ops):
            for ant_2 in ops[idx+1:]:
                diff = [x - y for x, y in zip(ant_1, ant_2)]
                diff = [int(y / gcd(*diff)) for y in diff]
                line_pts = []
                k = 0
                while True:
                    fails = 0
                    p_point = [a + k*b for a, b in zip(ant_1, diff)]
                    n_point = [a - k*b for a, b in zip(ant_1, diff)]
                    for point in [p_point, n_point]:
                        if (point[0] < 0 or point[0] >= ROWS) or (point[1] < 0 or point[1] >= COLS):
                            fails +=1
                        else:
                            if point not in line_pts:
                                line_pts.append(point)

                    if fails == 2:
                        break
                    k+=1
                anti_nodes += line_pts
    
    # Reduce to unique points.
    anti_nodes = [tuple(x) for x in anti_nodes]
    anti_nodes = list(set(anti_nodes))
    return len(anti_nodes)



if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
