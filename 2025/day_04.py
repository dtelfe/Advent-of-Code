from collections import deque

from aoc import read, time_solution

DAY = 4

DIR8 = [(y, x) for y in [-1, 0, 1] for x in [-1, 0, 1] if (y, x) != (0, 0)]


def add(x, y):
    return tuple([a + b for a, b in zip(x, y)])


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id, split_lines=True)
    data = {(y, x) for y, row in enumerate(data) for x, v in enumerate(row) if v != "."}

    count = 0
    for point in data:
        if sum([(add(point, d) in data) * 1 for d in DIR8]) < 4:
            count += 1
    return count


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id, split_lines=True)
    data = {(y, x) for y, row in enumerate(data) for x, v in enumerate(row) if v != "."}

    rolls = {loc: set([add(loc, d) for d in DIR8 if add(loc, d) in data]) for loc in data}

    queue = deque([loc for loc, nbrs in rolls.items() if len(nbrs) < 4])

    count = 0
    while queue:
        point = queue.popleft()
        if point not in rolls:
            continue

        neighbours = rolls.get(point)
        if len(neighbours) >= 4:
            continue

        for neighbour in neighbours:
            rolls[neighbour].remove(point)
            queue.append(neighbour)

        del rolls[point]
        count += 1

    return count


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 13
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 43
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
