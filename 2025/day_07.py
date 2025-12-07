from collections import deque
from aoc import read, time_solution

DAY = 7


def add(c1, c2):
    return tuple([a + b for a, b in zip(c1, c2)])


DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id, split_lines=True)
    n_rows = len(data)
    n_cols = len(data[0])

    start = tuple([0, data[0].index("S")])
    queue = deque([start])

    split_points = set()
    seen = set()
    while queue:
        at = queue.popleft()
        move_to = add(at, DOWN)
        y, x = move_to
        if y >= n_rows:
            continue

        if x < 0 or x >= n_cols:
            continue

        if data[y][x] == ".":
            queue.append(move_to)
            seen.add(move_to)
        elif data[y][x] == "^":
            split_points.add(move_to)

            for move in [LEFT, RIGHT]:
                point = add(move_to, move)
                if point in seen:
                    continue
                queue.append(point)
                seen.add(point)
        else:
            assert False

    return len(split_points)


DP = {}
def possibilities(data, start):
    if start in DP:
        return DP[start]

    n_rows = len(data)
    n_cols = len(data[0])

    result = 1
    queue = deque([start])
    while queue:
        at = queue.popleft()
        move_to = add(at, DOWN)
        y, x = move_to
        if y >= n_rows:
            continue

        if x < 0 or x >= n_cols:
            continue

        if data[y][x] == ".":
            queue.append(move_to)
        elif data[y][x] == "^":
            result *= possibilities(data, (y, x - 1)) + possibilities(data, (y, x + 1))
        else:
            assert False
    DP[start] = result
    return result


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    start = tuple([0, data[0].index("S")])
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
