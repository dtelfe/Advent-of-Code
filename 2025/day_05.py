from aoc import read, time_solution

DAY = 5


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    fresh = [line.split("-") for line in data if "-" in line]
    fresh = [range(int(a), int(b) + 1) for a, b in fresh]

    available = [int(line) for line in data if "-" not in line]

    t = 0
    for id in available:
        if any([id in fresh_range for fresh_range in fresh]):
            t += 1
    return t


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    fresh = sorted([list(map(int, line.split("-"))) for line in data if "-" in line])

    left = 0
    right = 0
    total = 0
    for a, b in fresh:
        if a > left:
            left = a

        if b > right:
            right = b

        total += right + 1 - left
        left = right + 1

    return total


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 3
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 14
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
