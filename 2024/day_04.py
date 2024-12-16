from aoc import aoc_read, time_solution
import numpy as np

DAY = 4
TEST = False
SPLIT_LINES = True


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    count = 0

    # read left right
    for row in data:
        count += "".join(row).count("XMAS")
        count += "".join(row).count("SAMX")

    # read up down
    data = np.transpose(data)
    for row in data:
        count += "".join(row).count("XMAS")
        count += "".join(row).count("SAMX")
    data = np.transpose(data)

    # read diagonals
    k = 0
    while True:
        # Use ind to determine if all diagonals have been checked.
        exit_case = 0

        d_data = np.diagonal(data, k * 1)
        if list(d_data) == []:
            exit_case += 1
        count += "".join(d_data).count("XMAS")
        count += "".join(d_data).count("SAMX")

        # Reverse diagonal.
        d_data = np.diagonal(np.fliplr(data), k * 1)
        if list(d_data) == []:
            exit_case += 1
        count += "".join(d_data).count("XMAS")
        count += "".join(d_data).count("SAMX")

        if k > 0:
            # Check the negative value to check the otherside of the main diagonal
            # Do not do this for 0, else we would double count any on the main diagonal.

            d_data = np.diagonal(data, k * (-1))
            if list(d_data) == []:
                exit_case += 1
            count += "".join(d_data).count("XMAS")
            count += "".join(d_data).count("SAMX")

            # Reverse diagonal.
            d_data = np.diagonal(np.fliplr(data), k * (-1))
            if list(d_data) == []:
                exit_case += 1
            count += "".join(d_data).count("XMAS")
            count += "".join(d_data).count("SAMX")

        k += 1
        if exit_case == 4:
            # If all the lists are blank then we have reached the end.
            break

    return count


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    count = 0

    # Loop over the 2-d coords, excluding the perimeter.
    for r in range(1, len(data) - 1):
        for c in range(1, len(data[0]) - 1):
            # The centre must be A for it to be a potential match.
            if data[r][c] == "A":
                corners = [data[r + x][c + y] for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]]
                if corners.count("M") == 2 and corners.count("S") == 2 and corners[0] != corners[-1]:
                    # Check that the corners consistent of 2 M and 2 S.
                    # Lastly check one set of diagonals differ.
                    count += 1
    return count


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
