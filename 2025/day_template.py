from aoc import read, time_solution

DAY = 1


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    return data


# @time_solution
def part_2(file_id):
    # data = read(DAY, file_id)
    return 0


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
