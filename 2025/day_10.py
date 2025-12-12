import scipy
import numpy as np
from collections import deque

from aoc import read, time_solution

DAY = 10


def clean(data):
    clean_data = []
    for line in data:
        pattern, *buttons, other = line.split(" ")
        pattern = pattern.replace("[", "").replace("]", "")
        buttons = " ".join(buttons)
        buttons = [list(map(int, button.split(","))) for button in buttons.replace("(", "").replace(")", "").split(" ")]
        other = list(map(int, other.replace("{", "").replace("}", "").split(",")))
        clean_data.append((pattern, buttons, other))
    return clean_data


# @time_solution
def part_1(file_id):
    data = read(DAY, file_id)
    data = clean(data)
    total_presses = 0
    for pattern, buttons, _ in data:
        goal = tuple([n for n, v in enumerate(pattern) if v == "#"])
        seen = {}
        queue = deque([(0, ())])
        solution = -1
        while queue:
            n, current = queue.popleft()
            if current == goal and n > 0:
                solution = n
                break

            to_add = [g for g in goal if g not in current]
            to_remove = [g for g in current if g not in goal]

            to_push = [button for button in buttons if any([b in to_add or b in to_remove for b in button])]
            for push in to_push:
                adding = set([p for p in push if p not in current])
                removing = set([p for p in current if p in push])

                result = tuple(sorted((set(current) | adding) - removing))
                if result in seen and (n + 1) >= seen[result]:
                    continue

                seen[result] = n + 1
                queue.append((n + 1, result))
        assert solution != -1

        total_presses += solution
    return total_presses


# @time_solution
def part_2(file_id):
    #TODO: Solve without Scipy.
    data = read(DAY, file_id)
    data = clean(data)
    total_presses = 0
    for _, buttons, goal in data:
        maxb = max(max(button) for button in buttons)
        buttons = [[1 if v in button else 0 for v in range(maxb + 1)] for button in buttons]

        presses = np.transpose(np.array([1 for _ in buttons]))
        buttons = np.transpose(np.array(buttons))
        goal = np.transpose(np.array(goal))
        t = scipy.optimize.linprog(presses, A_eq=buttons, b_eq=goal, integrality=1)
        assert t.success
        total_presses += int(round(t.fun, 0))
    return total_presses


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    assert test_p1 == 7
    print(f"Solution to part 1 testcase: {test_p1}")
    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")

    print("")
    test_p2 = part_2("test")
    print(f"Solution to part 2 testcase: {test_p2}")
    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
