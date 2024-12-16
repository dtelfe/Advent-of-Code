from aoc import aoc_read, time_solution

DAY = 7
TEST = False
SPLIT_LINES = False


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.replace(":","").split() for row in data]
    CALC_STORE = {}
    res = 0
    for row in data:
        goal = int(row[0])
        ops = [int(x) for x in row[1:]]
        potentials, CALC_STORE = return_totals(ops, CALC_STORE)
        if goal in potentials:
            res += goal
    return res

def return_totals(options, calc_store, part_2 = False):
    if tuple(options) in calc_store:
        return calc_store.get(tuple(options)), calc_store
    
    if len(options) == 1:
        return options, calc_store
    elif len(options) > 1:
        lv = options[-1]
        eo_calc, calc_store = return_totals(options[:-1], calc_store, part_2)
        

        if part_2:
            add_ops = [x + lv for x in eo_calc]
            mult_ops = [x * lv for x in eo_calc]
            cat_ops = [int(str(x) + str(lv)) for x in eo_calc]
            all_ops = list(set(add_ops + mult_ops + cat_ops))
        
        if not part_2:
            add_ops = [x + lv for x in eo_calc]
            mult_ops = [x * lv for x in eo_calc]
            all_ops = list(set(add_ops + mult_ops))

        calc_store[tuple(options)] = all_ops

        return all_ops, calc_store

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [row.replace(":","").split() for row in data]
    CALC_STORE = {}
    res = 0
    for row in data:
        goal = int(row[0])
        ops = [int(x) for x in row[1:]]
        potentials, CALC_STORE = return_totals(ops, CALC_STORE, True)
        if goal in potentials:
            res += goal
    return res


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
