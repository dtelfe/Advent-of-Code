from aoc import aoc_read, time_solution
import sys

sys.setrecursionlimit(3000)

DAY = 22
TEST = False
SPLIT_LINES = False


def step(s):
    s = ((s * 64) ^ s) % 16777216
    s = (int(s / 32) ^ s) % 16777216
    s = ((s * 2048) ^ s) % 16777216
    return s


def multi_step(s, n):
    values = [s]
    for _ in range(n):
        s = step(s)
        values.append(s)
    return values


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [int(x) for x in data]
    data = [multi_step(x, 2000)[-1] for x in data]
    return sum(data)


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [int(x) for x in data]
    combo_collection = {}
    line_collections = []
    # keep track of first sale only.
    for line in data:
        line_collection = {}
        new_res = multi_step(line, 2000)
        prices = [x % 10 for x in new_res]
        deltas = [b - a for a, b in zip(prices, prices[1:])]
        for idx in range(0, len(deltas) - 4 + 1):
            step = tuple(deltas[idx : idx + 4])
            if step not in line_collection:
                line_collection[step] = prices[idx + 4]
                combo_collection[step] = 0

        line_collections.append(line_collection)

    for line_collection in line_collections:
        for k, v in line_collection.items():
            combo_collection[k] += v

    best = max(combo_collection.values())
    return best


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
