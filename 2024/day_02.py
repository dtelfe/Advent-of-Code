from aoc import aoc_read, time_solution
from copy import deepcopy

DAY = 2
TEST = False
SPLIT_LINES = False


def cleanse_data(data):
    data = [row.split(" ") for row in data]
    data = [[int(x) for x in row] for row in data]
    return data


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = cleanse_data(data)

    differences = [[b - a for a, b in zip(row, row[1:])] for row in data]
    monotonic = [all(x > 0 for x in line) or all(x < 0 for x in line) for line in differences]
    delta_check = [all(abs(x) >= 1 for x in line) and all(abs(x) <= 3 for x in line) for line in differences]
    all_pass = [all([x, y]) for x, y in zip(monotonic, delta_check)]
    return all_pass.count(True)


def check_row(row):
    differences = [b - a for a, b in zip(row, row[1:])]
    monotonic = all(x > 0 for x in differences) or all(x < 0 for x in differences)
    delta_check = all(abs(x) >= 1 for x in differences) and all(abs(x) <= 3 for x in differences)
    return monotonic and delta_check


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = cleanse_data(data)
    passes = 0

    for row in data:
        base_pass = check_row(row)
        if base_pass:
            passes += 1
            continue

        search_ind = True
        for idx in range(len(row)):
            if search_ind:
                altered_row = deepcopy(row)
                altered_row.pop(idx)
                altered_pass = check_row(altered_row)
                if altered_pass:
                    passes += 1
                    search_ind = False
    return passes


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
