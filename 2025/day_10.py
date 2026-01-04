import re
import scipy
import numpy as np
from collections import deque

from aoc import read, time_solution

DAY = 10


def clean(data):
    clean_data = []
    for line in data:
        pattern, *buttons, other = line.split(" ")
        pattern = pattern[1:-1]
        buttons = [[int(x) for x in re.findall(r"\d+", button)] for button in buttons]
        other = [int(x) for x in re.findall(r"\d+", other)]
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
    data = read(DAY, file_id)
    data = clean(data)
    total_presses = 0
    for _, buttons, goal in data:
        maxb = max(max(button) for button in buttons)
        buttons = [[1 if v in button else 0 for v in range(maxb + 1)] for button in buttons]

        # Solving Ax = b
        # A = Buttons
        # b = goal
        presses = np.array([1 for _ in buttons])
        buttons = np.matrix(buttons).T
        goal = np.array(goal)
        t = scipy.optimize.linprog(presses, A_eq=buttons, b_eq=goal, integrality=1)
        assert t.success
        total_presses += int(round(t.fun, 0))
    return total_presses


def row_reduce(A, b):
    # https://www.storyofmathematics.com/gauss-jordan-elimination/
    k_col = 0
    k_row = 0
    C = [a + [b] for a, b in zip(A, b)]
    n_rows, n_cols = len(C), len(C[0])
    while k_row < n_rows and k_col < n_cols - 1:
        max_value = max([abs(C[r][k_col]) for r in range(k_row, n_rows)])
        pivot_index = [r for r in range(k_row, n_rows) if abs(C[r][k_col]) == max_value][0]

        if C[pivot_index][k_col] == 0:
            k_col += 1
            continue

        C[k_row], C[pivot_index] = C[pivot_index], C[k_row]
        C[k_row] = [v / C[k_row][k_col] for v in C[k_row]]

        for i in range(k_row + 1, n_rows):
            C[i] = [round(v - C[i][k_col] * k, 9) for v, k in zip(C[i], C[k_row])]

        k_row += 1
        k_col += 1

    C = [[round(x, 9) for x in row] for row in C]
    A = [row[:-1] for row in C]
    b = [row[-1] for row in C]
    return A, b


def solve_reduced(A, b, max_pushes):
    variables = [f"a_{i}" for i in range(len(A[0]))]
    known_values = {}
    relationships = []
    n_row = len(A) - 1
    while n_row >= 0:
        coefficients = A[n_row]
        result = b[n_row]
        if set(coefficients) == set([0]) and result == 0:
            n_row -= 1
            continue
        to_solve = {a: c for a, c in zip(variables, coefficients) if c != 0}
        relationships.append((to_solve, result))
        n_row -= 1

    presses = itersolve(known_values, relationships, max_pushes, A, b)
    return presses


def itersolve(fixed_vals, relationships, max_pushes, A, b):
    # Use 1e100 for no solution so that min can be used.
    pushes = 1e100
    for v in fixed_vals.values():
        if v < - 0.1:
            return 1e100
        elif abs(round(v, 0) - v) > 0.1:
            return 1e100

    if not relationships:
        # No relationships remain - we have a potential solution.
        deltas = [sum(r * fixed_vals.get(f"a_{n}", 0) for n, r in enumerate(row)) - expected for row, expected in zip(A, b)]
        if all(abs(d) < 0.1 for d in deltas):
            return int(round(sum(fixed_vals.values()), 0))
        return 1e100

    # Simplify relationships by removing known values.
    while True:
        edited = False
        u_relationships = []
        for relationship in relationships:
            variables, constant = relationship
            unknown_variables = {a: c for a, c in variables.items() if a not in fixed_vals}
            u_constant = constant - sum(c * fixed_vals[a] for a, c in variables.items() if a in fixed_vals)

            if not unknown_variables and abs(u_constant) >= 0.1:
                return 1e100
            elif not unknown_variables:
                continue

            if len(unknown_variables) == 1:
                edited = True
                v = list(unknown_variables.keys())[0]
                a = unknown_variables[v]
                fixed_vals[v] = int(round(u_constant / a, 0))
                if fixed_vals[v] < -0.1:
                    return 1e100
            elif u_constant <= 0 and all(v <= 0 for v in unknown_variables.values()):
                edited = True
                u_constant *= -1
                unknown_variables = {k: -v for k, v in unknown_variables.items()}
            elif u_constant == 0 and all(v > 0.1 for v in unknown_variables.values()):
                edited = True
                for k in unknown_variables:
                    fixed_vals[k] = 0
                continue

            u_relationships.append((unknown_variables, u_constant))
        relationships = u_relationships

        if not edited:
            break

    if not relationships:
        return itersolve(fixed_vals, relationships, max_pushes, A, b)

    # Choose an equation to start iterating solutions for.
    # Sort by equation length, then equations with all positive coefficient, then equations with the highest total.
    relationships = sorted(relationships, key=lambda x: [len(x[0]), not (x[1] >= 0), -abs(x[1])])
    solving, sol = relationships[0]
    first_key = list(solving)[0]
    max_value = max_pushes[int(first_key.replace("a_", ""))]
    if sol > 0 and all(v >= 0 for v in solving.values()):
        max_value = min(max_value, int(round(sol / solving[first_key], 0) + 1))

    for v in range(max_value):
        guess = {first_key: v}
        pushes = min(pushes, itersolve(fixed_vals | guess, relationships, max_pushes, A, b))
    return pushes

@time_solution
def part_2b(file_id):
    data = read(DAY, file_id)
    data = clean(data)
    total_presses = 0
    for _, buttons, goal in data:
        maxb = max(max(button) for button in buttons)
        max_pushes = [min([goal[b] for b in button]) + 1 for button in buttons]
        buttons = [[1 if v in button else 0 for v in range(maxb + 1)] for button in buttons]

        # Solving Ax = b
        # A = Buttons
        # b = goal
        buttons = [list(line) for line in zip(*buttons)]
        buttons, goal = row_reduce(buttons, goal)
        solution = solve_reduced(buttons, goal, max_pushes)
        total_presses += solution
    return total_presses


if __name__ == "__main__":
    print("\nRunning Calculations")
    test_p1 = part_1("test")
    print(f"Solution to part 1 testcase: {test_p1}")
    assert test_p1 == 7

    solution_p1 = part_1("input")
    print(f"Solution to part 1: {solution_p1}")
    print("")

    test_p2 = part_2("test")
    print(f"Solution to part 2 testcase: {test_p2}")
    assert test_p2 == 33

    solution_p2 = part_2("input")
    print(f"Solution to part 2: {solution_p2}")
    print("")

    test_p2b = part_2b("test")
    print(f"Solution to part 2 testcase (no SciPy): {test_p2b}")
    assert test_p2b == 33

    solution_p2b = part_2b("input")
    print(f"Solution to part 2 (no SciPy): {solution_p2b}")
    assert solution_p2b == solution_p2
