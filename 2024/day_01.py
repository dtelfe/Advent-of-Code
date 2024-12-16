from aoc import aoc_read, time_solution

DAY = 1
TEST = False
SPLIT_LINES = False

def data_to_lists(data):
    data = [row.split(" ") for row in data]
    list_1 = [int(row[0]) for row in data]
    list_2 = [int(row[-1]) for row in data]
    return list_1, list_2

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    list_1, list_2 = data_to_lists(data)
    
    list_1.sort()
    list_2.sort()
    return sum([abs(b - a) for a,b in zip(list_1, list_2)])


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    list_1, list_2 = data_to_lists(data)

    return sum([a * list_2.count(a) for a in list_1])


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
