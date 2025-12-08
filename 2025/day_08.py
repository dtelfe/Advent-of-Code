from aoc import read, time_solution

DAY = 8


def prod(items):
    total = 1
    for item in items:
        total *= item
    return total


def dist(a, b):
    return sum((c1 - c2) ** 2 for c1, c2 in zip(a, b)) ** 0.5


def value_sort(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}


# @time_solution
def part_1(file_id, max_wires=1000):
    data = read(DAY, file_id)
    data = {n: list(map(int, row.split(","))) for n, row in enumerate(data)}

    groups = [set([i]) for i in data]
    wires = 0

    distances = {(i, j): dist(c1, c2) for i, c1 in data.items() for j, c2 in data.items() if j > i}
    distances = value_sort(distances)

    for pair in distances:
        i, j = pair
        i_idx = [i in group for group in groups].index(True)
        j_idx = [j in group for group in groups].index(True)

        if i_idx != j_idx:
            keep, remove = sorted([i_idx, j_idx])
            r = groups.pop(remove)
            groups[keep] |= r

        wires += 1
        if wires == max_wires:
            break

    groups = [len(g) for g in groups]
    top_3 = sorted(groups, reverse=True)[:3]
    return prod(top_3)


# @time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    data = {n: list(map(int, row.split(","))) for n, row in enumerate(data)}
    n_items = len(data)

    result = None

    groups = [set([i]) for i in data]
    seen = set([])

    distances = {(i, j): dist(c1, c2) for i, c1 in data.items() for j, c2 in data.items() if j > i}
    distances = value_sort(distances)

    for pair in distances:
        i, j = pair

        i_idx = [i in group for group in groups].index(True)
        j_idx = [j in group for group in groups].index(True)

        if i_idx != j_idx:
            keep_idx, remove_idx = sorted([i_idx, j_idx])
            r = groups.pop(remove_idx)
            groups[keep_idx] |= r
            seen.add(i)
            seen.add(j)

        if len(seen) == n_items and len(groups) == 1:
            result = data[i][0] * data[j][0]
            break
    return result


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test", max_wires=10)
    assert test_p1 == 40
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input", max_wires=1000)
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    assert test_p2 == 25272
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
