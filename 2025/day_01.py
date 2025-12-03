from aoc import read, time_solution

DAY = 1

SIGN_MAP = {"L": -1, "R": 1}

# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)

    location = 50
    count = 0
    for line in data:
        pos, value = line[0], int(line[1:])
        sign = SIGN_MAP[pos]

        location = (location + sign * value) % 100

        if location == 0:
            count += 1
    return count


# @aoc.time_solution
def part_2(file_id):
    data = read(DAY, file_id)

    location = 50
    count = 0
    for line in data:
        pos, value = line[0], int(line[1:])
        sign = SIGN_MAP[pos]

        for _ in range(value):
            location = (location + sign) % 100

            if location == 0:
                count += 1
    return count



if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 3
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 6
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
