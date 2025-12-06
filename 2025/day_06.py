from aoc import read, time_solution

DAY = 6


def prod(items):
    total = 1
    for item in items:
        total *= item
    return total

OP_MAP = {"+": sum, "*": prod}


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    for n, line in enumerate(data):
        line = [item.strip() for item in line.split(" ") if item != ""]
        data[n] = line

    total = 0
    for row in zip(*data):
        *values, op = row
        op = OP_MAP[op]
        total += op(map(int, values))

    return total


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    data = [line[::-1] for line in data]

    total = 0
    values = []
    for row in zip(*data):
        if "".join(row).strip() == "":
            values = []
        else:
            *numbers, op = row
            values.append(int("".join(numbers)))

            if op != " ":
                op = OP_MAP[op]
                total += op(values)

    return total


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 4277556
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 3263827
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
