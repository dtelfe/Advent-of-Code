from ast import Try
from aoc import aoc_read, time_solution

DAY = 19
TEST = False
SPLIT_LINES = False


def valid_towel(towels, design, DP):
    valid = False
    if design == []:
        return True

    if design in DP:
        return DP[design]
    for towel in towels:
        chk = len(towel)
        if towel == design:
            return True
        elif towel == design[:chk]:
            valid = valid or valid_towel(towels, design[chk:], DP)

    DP[design] = valid
    return valid

def valid_towel_count(towels, design, DP):
        count = 0
        if design == []:
            return 1

        if design in DP:
            return DP[design]

        for towel in towels:
            chk = len(towel)
            if towel == design:
                count += 1
            elif towel == design[:chk]:
                count += valid_towel_count(towels, design[chk:], DP)

        DP[design] = count
        return count


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    towels = data[0].split(", ")
    designs = [design for design in data[1:] if design != ""]

    possible = []
    DP = {}
    for design in designs:
        possible.append(valid_towel(towels, design, DP))

    return possible.count(True)


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    towels = data[0].split(", ")
    designs = [design for design in data[1:] if design != ""]

    possible = []
    DP = {}
    for design in designs:
        possible.append(valid_towel_count(towels, design, DP))

    return sum(possible)


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
