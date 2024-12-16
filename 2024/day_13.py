from aoc import aoc_read, time_solution

DAY = 13
TEST = False
SPLIT_LINES = False

def clean_up(data, p2=False):
    num_machines = int(len(data) / 3)
    
    machines = []

    for num in range(num_machines):
        but_a = data[num * 3 + 0].replace("Button A: ", "").replace("X+","").replace(" Y+", "")
        but_a = [int(v) for v in but_a.split(",")]

        but_b = data[num * 3 + 1].replace("Button B: ", "").replace("X+","").replace(" Y+", "")
        but_b = [int(v) for v in but_b.split(",")]

        prize = data[num * 3 + 2].replace("Prize: ", "").replace("X=","").replace(" Y=", "")
        if p2:
            prize = [int(v) + 10000000000000 for v in prize.split(",")]
        else:
            prize = [int(v) for v in prize.split(",")]
        
        machines.append([but_a, but_b, prize])
    return machines

def solve(v_a, v_b, goal, max_guesses=None):
    # Solve v_a * i + v_b * j = goal. 
    
    # Can move to matrix multiplication, however I had issues with floating points and ints
    # ultimately giving a different answer.
    
    float_j = (goal[0] * (v_a[1] / v_a[0]) - goal[1]) / ((v_a[1] / v_a[0]) * v_b[0] - v_b[1])
    j = int(round(float_j, 0)) 
    if abs(j - float_j) >= 0.1:
        return 0, 0

    if j < 0 or (max_guesses is not None and j > max_guesses):
        return 0, 0
    
    float_i = (goal[0] - v_b[0] * j) / v_a[0]
    i = int(round(float_i, 0)) 
    if abs(i - float_i) >= 0.1:
        return 0, 0

    if i < 0 or (max_guesses is not None and i > max_guesses):
        return 0, 0

    # Validate solution works on second coordinate.
    if v_a[1] *  i + v_b[1] * j != goal[1]:
        return 0, 0
    
    return i, j

@time_solution
def part_1():
    MAX_GUESSES = 100
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    machines = clean_up(data)
    tokens = 0

    for vec_a, vec_b, goal in machines:
        i, j = solve(vec_a, vec_b, goal, MAX_GUESSES)
        tokens += (i*3) + j
    return tokens


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    machines = clean_up(data, True)
    tokens = 0
    for vec_a, vec_b, goal in machines:
        i, j = solve(vec_a, vec_b, goal)
        tokens += (i*3) + j
    return tokens


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
