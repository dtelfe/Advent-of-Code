from collections import deque
from aoc import read, time_solution

DAY = 7


def add(c1, c2):
    return tuple(a + b for a, b in zip(c1, c2))


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id, split_lines=True)

    n_rows = len(data)
    start = (0, data[0].index("S"))
    queue = deque([start])

    split_points = set()
    seen = set()
    while queue:
        at = queue.popleft()
        y, x = at

        path = [data[py][x] for py in range(y, n_rows)]
        if "^" in path:
            move_to = (y + path.index("^"), x)
            split_points.add(move_to)

            for move in [(0, -1), (0, 1)]:
                point = add(move_to, move)
                if point in seen:
                    continue
                queue.append(point)
                seen.add(point)

    return len(split_points)


DP = {}
def possibilities(data, start):
    if start in DP:
        return DP[start]
    result = 1
    y, x = start
    path = [data[py][x] for py in range(y, len(data))]

    if "^" in path:
        split_y = y + path.index("^")
        result = possibilities(data, (split_y, x - 1)) + possibilities(data, (split_y, x + 1))
    DP[start] = result
    return result


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    start = (0, data[0].index("S"))
    return possibilities(data, start)


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 21
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 40
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
