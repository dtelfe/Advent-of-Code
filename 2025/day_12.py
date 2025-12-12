from aoc import read, time_solution

DAY = 12


def clean(data):
    n = None
    shapes = {}
    packings = []

    shape = []
    for line in data:
        if ":" in line and "x" not in line:
            n, _ = line.split(":")
            n = int(n)
        elif line == "" and n is not None and shape != []:
            shapes[n] = shape
            n = None
            shape = []
        elif "#" in line or "." in line:
            shape.append(line)
        elif ":" in line and "x" in line:
            size, items = line.split(": ")
            size = list(map(int, size.split("x")))
            items = list(map(int, items.split(" ")))
            packings.append([size, items])

    return shapes, packings


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id, remove_blanks=False)
    shapes, packings = clean(data)
    shape_sizes = {n: sum(row.count("#") for row in shape) for n, shape in shapes.items()}

    total = 0
    i = 0
    for size, reqs in packings:
        i += 1
        width, length = size
        total_area = width * length
        count_hashes = sum([n * shape_sizes[i] for i, n in enumerate(reqs)])

        if count_hashes > total_area:
            continue

        full_widths = width - (width % 3)
        full_lengths = length - (length % 3)

        if sum(reqs) * 9 <= full_lengths * full_widths:
            total += 1
            continue

        print("To consider. Number of squares to save:", sum(reqs) - full_lengths * full_widths)
        # This case isn't needed for the full input.
        # TODO: Solve this case to allow testcase to run.
        assert False

    return total


# @time_solution
def part_2(file_id):
    # data = read(DAY, file_id)
    return 0


if __name__ == "__main__":
    print("\nRunning Calculations")
    # test_p1 = part_1("test")
    # print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
