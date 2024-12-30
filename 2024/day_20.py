from aoc import aoc_read, time_solution

DAY = 20
TEST = False
SPLIT_LINES = True

DIRS = [[1,0], [-1,0], [0,1], [0,-1]]

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    ROWS = len(data)
    COLS = len(data[0])

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == "S":
                start = [y,x]

            if value == "E":
                end = [y,x]

    distance = 0
    dist_store = {tuple(start): 0}
    queue = [start]

    while True:
        if queue == []:
            break

        current = queue[0]
        del queue[0]
        distance +=1

        for move in DIRS:
            next = [coord + change for coord, change in zip(current, move)]

            if next[0] < 0 or next[0] >= ROWS:
                continue

            if next[1] < 0 or next[1] >= COLS:
                continue

            if data[next[0]][next[1]] == "#":
                continue

            if tuple(next) in dist_store:
                continue

            queue.append(next)
            dist_store[tuple(next)] = distance

    track_length = dist_store[tuple(end)]

    cheat_impacts = {}
    for cheat_start in dist_store.keys():
        for move in DIRS:
            next = [coord + change for coord, change in zip(cheat_start, move)]
            next_2 = [coord + 2*change for coord, change in zip(cheat_start, move)]
            if next[0] < 0 or next[0] >= ROWS or next_2[0] < 0 or next_2[0] >= ROWS:
                continue

            if next[1] < 0 or next[1] >= COLS or next_2[1] < 0 or next_2[1] >= COLS:
                continue

            if data[next[0]][next[1]] != "#":
                continue

            if data[next_2[0]][next_2[1]] == "#":
                continue

            new_length = dist_store[tuple(cheat_start)] + (dist_store[tuple(end)] - dist_store[tuple(next_2)]) + 2

            if new_length < track_length:
                cheat_impacts[tuple(list(cheat_start) + move)] = track_length - new_length

    if TEST:
        summary = {}
        for value in set(list(cheat_impacts.values())):
            summary[value] = list(cheat_impacts.values()).count(value)
        summary = {k: summary[k] for k in sorted(summary.keys())}
        return summary

    saved_times = list(cheat_impacts.values())
    return len([x for x in saved_times if x >= 100])


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    ROWS = len(data)
    COLS = len(data[0])

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == "S":
                start = [y,x]

            if value == "E":
                end = [y,x]

    distance = 0
    dist_store = {tuple(start): 0}
    queue = [start]

    while True:
        if queue == []:
            break

        current = queue[0]
        del queue[0]
        distance +=1

        for move in DIRS:
            next = [coord + change for coord, change in zip(current, move)]

            if next[0] < 0 or next[0] >= ROWS:
                continue

            if next[1] < 0 or next[1] >= COLS:
                continue

            if data[next[0]][next[1]] == "#":
                continue

            if tuple(next) in dist_store:
                continue

            queue.append(next)
            dist_store[tuple(next)] = distance

    track_length = dist_store[tuple(end)]

    all_savings = []
    # Now when cheating, we can move up to 20.
    for cheat_start in dist_store.keys():
        cheat_reach_store = {}
        for y in range(ROWS):
            for x in range(COLS):
                dist = abs(y - cheat_start[0]) + abs(x - cheat_start[1])
                if dist <= 20:
                    cheat_reach_store[tuple([y,x])] = dist

        # Keep only the points on that end up back on the race track.
        cheat_reach_store = {k: v for k, v in cheat_reach_store.items() if k in dist_store}

        # Calculate the savings
        cheat_lens = {k: track_length - (dist_store[tuple(cheat_start)] + (dist_store[tuple(end)] - dist_store[tuple(k)]) + v) for k, v in cheat_reach_store.items()}

        # Drop the time saving only.
        all_savings += [x for x in cheat_lens.values() if x > 0]

    if TEST:
        summary = {}
        for value in set(all_savings):
            summary[value] = all_savings.count(value)
        summary = {k: summary[k] for k in sorted(summary.keys()) if k >= 50}
        return summary
    return len([x for x in all_savings if x >= 100])


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
