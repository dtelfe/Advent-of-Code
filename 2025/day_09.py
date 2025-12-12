from aoc import read, time_solution

DAY = 9


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    data = [list(map(int, line.split(","))) for line in data]

    max_area = 0
    for i, p1 in enumerate(data):
        for j, p2 in enumerate(data):
            if j <= i:
                continue
            x1, y1 = p1
            x2, y2 = p2
            area = (abs(y2 - y1) + 1) * (abs(x2 - x1) + 1)
            max_area = max(max_area, area)
    return max_area


def construct_edges(data):
    draw_points = data + [data[0]]
    edges = []
    for p1, p2 in zip(draw_points, draw_points[1:]):
        x1, y1 = p1
        x2, y2 = p2

        minx, maxx = sorted([x1, x2])
        miny, maxy = sorted([y1, y2])
        edge = [range(minx, maxx + 1), range(miny, maxy + 1)]
        edges.append(edge)
    return edges


def get_ordered_rectangles(data):
    sizes = {}
    max_area = 0
    for i, p1 in enumerate(data):
        for j, p2 in enumerate(data):
            if j <= i:
                continue
            x1, y1 = p1
            x2, y2 = p2
            area = (abs(y2 - y1) + 1) * (abs(x2 - x1) + 1)
            sizes[(i, j)] = area
            max_area = max(max_area, area)

    sizes = {k: v for k, v in sorted(sizes.items(), key=lambda item: item[1], reverse=True)}
    return sizes


def ranges_intersect(range_1, range_2):
    intersection = range(max(range_1.start, range_2.start), min(range_1.stop, range_2.stop))
    return len(intersection) > 0


@time_solution
def part_2(file_id):
    data = read(DAY, file_id)
    data = [list(map(int, line.split(","))) for line in data]
    edges = construct_edges(data)

    x1, *_, x2 = sorted([c[0] for c in data])
    y1, *_, y2 = sorted([c[1] for c in data])

    verticals = [edge for edge in edges if edge[0].stop - edge[0].start == 1]
    horizontals = [edge for edge in edges if edge[1].stop - edge[1].start == 1]

    # Check no horizontals are vertical neighbours as this would give a "fake" cut.
    # We expect the edge to split inside/outside, but this wouldn't be the case if they neighbour.
    for i, edge_1 in enumerate(horizontals):
        for j, edge_2 in enumerate(horizontals):
            if j <= i:
                continue

            if abs(edge_2[1].start - edge_1[1].start) != 1:
                continue

            if ranges_intersect(edge_1[0], edge_2[0]):
                raise Exception("Solution probably breaks")

    # Similar for vert.
    for i, edge_1 in enumerate(verticals):
        for j, edge_2 in enumerate(verticals):
            if j <= i:
                continue
            if abs(edge_2[0].start - edge_1[0].start) != 1:
                continue
            if ranges_intersect(edge_1[1], edge_2[1]):
                raise Exception("Solution probably breaks")

    p1_rectangles = get_ordered_rectangles(data)
    for pair, area in p1_rectangles.items():
        i, j = pair
        # print(area, end="\r")
        p1 = data[i]
        p2 = data[j]

        x1, y1 = p1
        x2, y2 = p2

        y_low, y_high = sorted([y1, y2])
        x_low, x_high = sorted([x1, x2])

        check_y = range(y_low + 1, y_high)
        check_x = range(x_low + 1, x_high)

        invalid = False
        for edge in verticals:
            if invalid:
                continue
            elif (x_low < edge[0].start < x_high) and ranges_intersect(check_y, edge[1]):
                invalid = True

        if invalid:
            continue

        for edge in horizontals:
            if invalid:
                continue
            elif (y_low < edge[1].start < y_high) and ranges_intersect(check_x, edge[0]):
                invalid = True

        if invalid:
            continue

        return area
    return -1


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    print(f"Solution to part 1 testcase: {test_p1}")
    assert test_p1 == 50
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    print(f"Solution to part 2 testcase: {test_p2}")
    assert test_p2 == 24
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
