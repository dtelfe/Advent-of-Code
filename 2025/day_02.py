from aoc import read, time_solution

DAY = 2


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)[0]

    invalid_ids = set()
    for pair in data.split(","):
        left, right = pair.split("-")
        size = max(1, len(left) // 2)

        partial = left[:size]
        left, right = int(left), int(right)
        while True:
            guess = int(partial * 2)
            if guess > right:
                break

            if left <= guess and guess <= right:
                invalid_ids.add(guess)

            partial = str(int(partial) + 1)

    return sum(invalid_ids)


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)[0]
    invalid_ids = set()
    for pair in data.split(","):
        left, right = pair.split("-")

        check_points = [left]
        if len(left) != len(right):
            check_points += [str(10 ** (k - 1)) for k in range(len(left) + 1, len(right) + 1)]

        left, right = int(left), int(right)
        for point in check_points:
            point_size = len(point)
            for n in range(2, point_size + 1):
                if point_size % n != 0:
                    continue
                size = max(1, point_size // n)
                partial = point[:size]

                while True:
                    guess = int(partial * n)
                    if guess > right:
                        break

                    if left <= guess and guess <= right:
                        invalid_ids.add(guess)

                    partial = str(int(partial) + 1)

    return sum(invalid_ids)


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 1227775554
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 4174379265
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
