from aoc import aoc_read, time_solution

DAY = 21
TEST = False
SPLIT_LINES = False



NUM_PAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["#", "0", "A"]
]

KEY_PAD = [
    ["#", "^", "A"],
    ["<", "v", ">"]
]

KEYS = ["<", ">", "v", "^", "A"]

MOVES = [[1, 0], [-1, 0], [0, 1], [0, -1]]

MOVE_MAP = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, 1): ">",
    (0, -1): "<"
}

PREF_ORDER = [*"<^v>A"]


def unique_values(grid):
    values = []
    for row in grid:
        for value in row:
            if value != "#" and value not in values:
                values.append(value)
    return values


def get_all_paths(grid):
    start_cells = unique_values(grid)
    ROWS = len(grid)
    COLS = len(grid[0])
    all_paths = {}
    for start_cell in start_cells:

        # Find the start cell.
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value == start_cell:
                    start = [y, x]
        queue = [[start, [start]]]
        all_paths[tuple(start + start)] = []
        while True:
            if queue == []:
                break

            current, history = queue[0]
            del queue[0]

            for move in MOVES:
                next = [a + b for a, b in zip(current, move)]

                if next == start:
                    continue

                if next[0] < 0 or next[0] >= ROWS:
                    continue

                if next[1] < 0 or next[1] >= COLS:
                    continue

                if grid[next[0]][next[1]] == "#":
                    continue

                dots = tuple(history[0] + next)
                queue_pair = [next, history.copy() + [next]]

                if dots in all_paths.keys() and len(queue_pair[1]) > len(all_paths[dots][0]):
                    continue

                if dots not in all_paths.keys():
                    all_paths[dots] = []

                all_paths[dots].append(queue_pair[1])
                queue.append(queue_pair)

    return all_paths


def get_coord(grid, cell_value):
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == cell_value:
                return [y, x]


def all_path_symbol(all_paths):
    all_paths_corrected = {}
    for key, values in all_paths.items():
        if values == []:
            new_value = "A"
            all_paths_corrected[key] = [new_value]
        else:
            all_paths_corrected[key] = []
            for value in values:
                new_value = []
                for start, to in zip(value, value[1:]):
                    delta = tuple([b - a for a, b in zip(start, to)])
                    delta = MOVE_MAP[delta]
                    new_value.append(delta)
                new_value.append("A")
                new_value = "".join(new_value)
                all_paths_corrected[key].append(new_value)
    return all_paths_corrected


DP = {}
def return_shortest_paths_for_code(code, given_paths, X_PAD):
    number_options = []
    if code in DP:
        return DP[code]
    for idx, start in enumerate(code[:-1]):
        end = code[idx + 1]
        if start + end in DP:
            paths = DP[start + end]
        else:
            start_coord = get_coord(X_PAD, start)
            end_coord = get_coord(X_PAD, end)
            paths = given_paths[tuple(start_coord + end_coord)]
            DP[start + end] = paths
        number_options.append(paths)
    number_options = [xs for x in number_options for xs in x]
    number_options = "".join(number_options)
    DP[code] = number_options
    return number_options


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    key_pad_paths = get_all_paths(KEY_PAD)
    key_pad_paths = all_path_symbol(key_pad_paths)
    key_pad_paths = cleanse(key_pad_paths, order_map)

    num_pad_paths = get_all_paths(NUM_PAD)
    num_pad_paths = all_path_symbol(num_pad_paths)
    num_pad_paths = cleanse(num_pad_paths, order_map)

    shortest_codes = []
    for code in data:
        coded = "A" + code
        options = return_shortest_paths_for_code(coded, num_pad_paths, NUM_PAD)

        optioned = "A" + options
        option_final = return_shortest_paths_for_code(optioned, key_pad_paths, KEY_PAD)
        zzz = "A" + option_final
        zzz_final = return_shortest_paths_for_code(zzz, key_pad_paths, KEY_PAD)
        shortest_codes.append(zzz_final)

    codes = [int(x.replace("A", "")) for x in data]

    return sum(a * len(b) for a, b in zip(codes, shortest_codes))


def cleanse(pad, order_map):
    corrected_pad = {}
    for key, values in pad.items():
        if len(values) == 1:
            corrected_pad[key] = values
            continue
        changes = [[x != y for x, y in zip(value, value[1:])].count(True) for value in values]
        best = min(changes)
        corrected_pad[key] = [x for x, c in zip(values, changes) if c == best]

    final_pad = corrected_pad
    for key, values in corrected_pad.items():
        if isinstance(values, list):
            if len(values) == 1:
                final_pad[key] = values[0]
            corrected_values = sorted(values, key=lambda combo: custom_sort_key(combo, order_map), reverse=False)
            corrected_value = corrected_values[0]
            final_pad[key] = corrected_value
        else:
            final_pad[key] = values
    return final_pad


order_map = {char: index for index, char in enumerate(PREF_ORDER)}
def custom_sort_key(combo, order_map):
    return [order_map[char] for char in combo]


DP2 = {}
def layered_solve(start, end, paths, depth=2):
    if (start, end, depth) in DP2:
        return DP2[(start, end, depth)]

    path_length = 0
    if depth == 1:
        result = return_shortest_paths_for_code(start + end, paths, KEY_PAD)
        path_length += len(result)
    else:
        next_code = "A" + return_shortest_paths_for_code(start + end, paths, KEY_PAD)
        for next_start, next_end in zip(next_code, next_code[1:]):
            result = layered_solve(next_start, next_end, paths, depth - 1)
            path_length += result
    DP2[(start, end, depth)] = path_length
    return path_length


@time_solution
def part_2():
    LAYERS = 25
    data = aoc_read(DAY, TEST, SPLIT_LINES)

    key_pad_paths = get_all_paths(KEY_PAD)
    key_pad_paths = all_path_symbol(key_pad_paths)
    key_pad_paths = cleanse(key_pad_paths, order_map)

    num_pad_paths = get_all_paths(NUM_PAD)
    num_pad_paths = all_path_symbol(num_pad_paths)
    num_pad_paths = cleanse(num_pad_paths, order_map)

    direction_codes = []
    for code in data:
        coded = "A" + code
        new_code = return_shortest_paths_for_code(coded, num_pad_paths, NUM_PAD)
        direction_codes.append("A" + new_code)

    path_lengths = []
    for dir_code in direction_codes:
        full_code_length = 0
        for start, end in zip(dir_code, dir_code[1:]):
            pair_length = layered_solve(start, end, num_pad_paths, LAYERS)
            full_code_length += pair_length
        path_lengths.append(full_code_length)

    codes = [int(x.replace("A", "")) for x in data]
    return sum(a * b for a, b in zip(codes, path_lengths))


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
