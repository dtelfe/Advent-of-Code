from aoc import aoc_read, time_solution

DAY = 11
TEST = False
SPLIT_LINES = False


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = [int(x) for x in data[0].split()]
    BLINKS = 25

    for _ in range(BLINKS):
        new_data = []
        for stone in data:
            if stone == 0:
                new_data.append(1)
                continue
                
            number_length = len(str(stone))
            if number_length % 2 == 0:
                mid = int(number_length / 2)
                stone_1 = int(str(stone)[:mid])
                stone_2 = int(str(stone)[mid:])
                new_data += [stone_1, stone_2]
                continue

            new_data.append(stone * 2024)

        data = new_data.copy()
    return len(new_data)

def blink(stone):
    if stone == 0:
        return [1]
    number_length = len(str(stone))
    if number_length % 2 == 0:
        mid = int(number_length / 2)
        stone_1 = int(str(stone)[:mid])
        stone_2 = int(str(stone)[mid:])
        return [stone_1, stone_2]
    return [stone * 2024]

@time_solution
def part_2():
    # Store in a dictionary and keep count of how many stones with this value.
    # Then each value only need to be calculated once.
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    data = {int(x): 1 for x in data[0].split()}
    BLINKS = 75

    for _ in range(BLINKS):
        new_data = {}
        for stone, count in data.items():
            replacements = blink(stone)

            for new_stone in replacements:
                if new_stone in new_data:
                    new_data[new_stone] += count
                else:
                    new_data[new_stone] = count            

        # Update the main data store for the next loop.
        data = new_data.copy()
    return sum(new_data.values())


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
