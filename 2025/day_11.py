from collections import deque
from aoc import read, time_solution

DAY = 11


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    graph = {}
    for line in data:
        starting, endings = line.split(": ")
        endings = endings.split(" ")
        graph[starting] = endings

    paths = 0
    queue = deque(["you"])
    while queue:
        at = queue.popleft()

        for device in graph[at]:
            if device == "out":
                paths += 1
            else:
                queue.append(device)

    return paths


DP = {}
def solve(file_id, graph, at, dac, fft):
    dp_key = (file_id, at, dac, fft)
    if dp_key in DP:
        return DP[dp_key]

    paths = 0
    for device in graph[at]:
        if device == "out":
            paths += 1 * (dac and fft)
        else:
            seen_dac = dac | (device == "dac")
            seen_fft = fft | (device == "fft")
            paths += solve(file_id, graph, device, seen_dac, seen_fft)
    DP[dp_key] = paths
    return paths


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    graph = {}
    for line in data:
        starting, endings = line.split(": ")
        endings = endings.split(" ")
        graph[starting] = endings

    paths = solve(file_id, graph, "svr", False, False)
    return paths


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    print(f"Solution to part 1 testcase: {test_p1}")
    assert test_p1 == 5
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test_2")
    print(f"Solution to part 2 testcase: {test_p2}")
    assert test_p2 == 2
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
