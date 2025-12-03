from aoc import read, time_solution

DAY = 3


def find_largest_joltage(line, n_digits):
    current = []
    values = [int(x) for x in line]
    i = 0
    for n in range(n_digits - 1, -1, -1):
        if n != 0:
            sub_list = values[i:-n]
        else:
            sub_list = values[i:]

        d = max(sub_list)
        loc = sub_list.index(d)
        current.append(str(d))
        i += loc + 1
    return int("".join(current))


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)

    total = 0
    for line in data:
        total += find_largest_joltage(line, 2)
    return total


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    total = 0
    for line in data:
        total += find_largest_joltage(line, 12)

    return total


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 357
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 3121910778619
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
