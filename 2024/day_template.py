from aoc import aoc_read, time_solution

DAY = 1
TEST = True
SPLIT_LINES = False
REMOVE_BLANKS = True


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES, REMOVE_BLANKS)
    return data


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES, REMOVE_BLANKS)
    return 1


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
