from aoc import aoc_read, time_solution

DAY = 5
TEST = False
SPLIT_LINES = False


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    
    rules = [x for x in data if "|" in x]
    rules = [[int(y) for y in x.split("|")] for x in rules]
    
    updates = [x for x in data if "|" not in x]
    updates = [[int(y) for y in x.split(",")] for x in updates]
    

    # Determine if the set is in the correct order.
    # If so, then keep track of the middle page order.
    mid_pages = []
    for update_set in updates:
        passing = True
        for idx, p1 in enumerate(update_set):
            for p2 in update_set[idx+1:]:
                # if any pair is out of order, then the row fails.
                if [p2, p1] in rules:
                    passing = False
        
        if passing:
            middle = update_set[len(update_set)//2]
            mid_pages.append(middle)
    return sum(mid_pages)


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    
    rules = [x for x in data if "|" in x]
    rules = [[int(y) for y in x.split("|")] for x in rules]
    
    updates = [x for x in data if "|" not in x]
    updates = [[int(y) for y in x.split(",")] for x in updates]
    

    # Determine if the set is in the correct order.
    # If so, then keep track of the middle page order.
    mid_pages = []
    for update_set in updates:
        passing = True
        for idx, p1 in enumerate(update_set):
            for p2 in update_set[idx+1:]:
                # if any pair is out of order, then the row fails.
                if [p2, p1] in rules:
                    passing = False
        
        if not passing:
            # reorder 
            rel_rules = [rule for rule in rules if rule[0] in update_set and rule[1] in update_set]
            # see how many times the page shows on the left.
            # use this to determine order.
            left_sides = {v: sum([rule[0] == v for rule in rel_rules]) for v in update_set}
            ls_inv = {v:k for k,v in left_sides.items()}
            ordered_keys = sorted(left_sides.values(), reverse=True)

            re_ordered_set = [ls_inv.get(x) for x in ordered_keys]
            middle = re_ordered_set[(len(re_ordered_set)//2)]
            mid_pages.append(middle)
    return sum(mid_pages)


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
