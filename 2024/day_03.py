from aoc import aoc_read, time_solution
import re


DAY = 3
TEST = False
SPLIT_LINES = False


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = "|".join(data)

    # Search for mul(x,y) where x and y are 1-3 digit numbers
    successes = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", data)
    
    total = 0
    for pair in successes:
        v1, v2 = map(int, re.findall(r"\d{1,3}", pair))
        total += v1 * v2
    return total


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = "|".join(data)

    # Search for mul(x,y) where x and y are 1-3 digit numbers, or do() or don't().
    successes = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", data)
    
    total = 0
    add = True
    for pair in successes:
        if pair == "do()":
            add = True
        elif pair == "don't()":
            add = False
        elif add:
            v1, v2 = map(int, re.findall(r"\d{1,3}", pair))
            total += v1 * v2 * add

    return total


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
