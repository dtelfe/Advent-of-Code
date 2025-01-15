from aoc import aoc_read, time_solution
from copy import deepcopy
import time

DAY = 9
TEST = False
SPLIT_LINES = False


def first_read(data):
    blank = False
    id = 0
    out = []
    for value in data:
        if blank and value != 0:
            item = ["."] * value
            out.append(item)
        elif value != 0:
            item = [id] * value
            out.append(item)
            id += 1
        blank = not blank
    return out

def compress(d):
    # data = deepcopy(d)
    data = d
    ls = 0
    ls_idx = 0
    rs = len(data) - 1
    while True:
        if rs < ls:
            # If search indicators have flipped, we are done.
            break

        if sum([x.count(".") for x in data]) == 0:
            # If all dots removed, we are done.
            break

        item = data[ls]
        ls_max = len(item)
        if item == []:
            ls += 1
            ls_idx = 0
            continue
        
        while True:
            if ls_idx >= ls_max:
                ls_idx = 0
                ls +=1
                break
            elif item[ls_idx] != ".":
                ls +=1
                ls_idx = 0
                break
            elif item[ls_idx] == ".":
                rs_item = data[rs]
                if rs_item == [] or rs_item[0] == ".":
                    rs -=1
                else:
                    data[ls][ls_idx] = rs_item[-1]
                    ls_idx += 1
                    del rs_item[-1]

    data = [sub for sub in data if sub != [] and set(sub) != {"."}]
    data = [value for items in data for value in items]
    return data

def check_sum(value):
    return sum(idx * int(v) for idx, v in enumerate(value))

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [int(x) for x in data[0]]
    data = first_read(data)
    compressed = compress(data)
    ans = check_sum(compressed)
    return ans

def lump_compress(data):
    move_ids = set()
    rs = len(data) - 1
    ls = 0

    while True:
        if rs == 0:
            break

        if ls >= rs:
            ls = 0
            rs -= 1
            continue

        if data[rs][0] == "." or data[rs][0] in move_ids:
            rs -= 1
            continue

        if data[ls][0] != ".":
            ls +=1
            continue

        ls_space = len(data[ls])
        rs_req = len(data[rs])

        if rs_req == ls_space:
            move_ids.add(data[rs][0])
            data[ls] = data[rs].copy()
            data[rs] = ["."] * rs_req
            ls = 0
            rs -= 1
            continue

        if rs_req < ls_space:
            move_ids.add(data[rs][0])
            data[ls] = data[rs].copy()
            data[rs] = ["."] * rs_req
            data.insert(ls + 1, ["."] * (ls_space - rs_req))
            ls = 0
            # dont edit rs as we have inserted an item
            continue

        if rs_req > ls_space:
            ls +=1
            continue

    return data

def rejig(data):
    new_data = []
    for item in data:
        c = len(set(item))
        if c == 1:
            new_data.append(item)
        elif c == 2:
            dot = item.index(".")
            new_data.append(item[:dot])
            new_data.append(item[dot:])
        else:
            raise Exception()
    return new_data


@time_solution
def part_2():
    # This is real slow lol - 2144.724s
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [int(x) for x in data[0]]
    data = first_read(data)
    compressed = lump_compress(data)
    compressed = rejig(compressed)
    flat_comp = [x for x_list in compressed for x in x_list]
    flat_comp = [0 if x == "." else x for x in flat_comp]
    ans = check_sum(flat_comp)
    return ans


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")