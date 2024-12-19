from aoc import aoc_read, time_solution

DAY = 17
TEST = False
SPLIT_LINES = False
import time


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    reg_a, reg_b, reg_c, program = [row.split(": ")[-1] for row in data]
    
    reg_a = int(reg_a)
    reg_b = int(reg_b)
    reg_c = int(reg_c)
    program = [int(x) for x in program.split(",")]

    MAX_IDX = len(program) - 1
    out = []

    # opcode, operand pair
    # instruction operand 

    idx_opcode = 0 
    idx_operand = 1
    while True:
        if idx_opcode > MAX_IDX or idx_operand > MAX_IDX:
            break
        opcode = program[idx_opcode]
        operand = program[idx_operand]

        illegal = False
        match operand:
            case 0 | 1 | 2 | 3:
                combo_operand = operand
            case 4:
                combo_operand = reg_a
            case 5:
                combo_operand = reg_b
            case 6:
                combo_operand = reg_c
            case 7:
                # Combo operand 7 is reserved and will not appear in valid programs.
                illegal = True
            case _:
                pass

        match opcode:
            case 0 if not illegal:
                reg_a = int(reg_a / (2**combo_operand))
            case 1:
                reg_b = reg_b ^ operand
            case 2 if not illegal:
                reg_b = combo_operand % 8
            case 3 if reg_a != 0:
                idx_opcode = operand - 2
            case 4: 
                reg_b = reg_b ^ reg_c
            case 5 if not illegal:
                out.append(combo_operand % 8)
            case 6 if not illegal:
                reg_b = int(reg_a / (2**combo_operand))
            case 7 if not illegal:
                reg_c = int(reg_a / (2**combo_operand))
            case _:
                pass

        idx_opcode += 2
        idx_operand = idx_opcode + 1
    
    return ','.join([str(x) for x in out])

def solve(reg_a, reg_b, reg_c, program, skip):
    MAX_IDX = len(program) - 1
    out = []
    out_len = 0

    # opcode, operand pair
    # instruction operand 

    idx_opcode = 0 
    idx_operand = 1
    while True:
        
        if idx_opcode > MAX_IDX or idx_operand > MAX_IDX:
            break
        # Add two each time.
        opcode = program[idx_opcode]
        operand = program[idx_operand]

        illegal = False
        match operand:
            case 0 | 1 | 2 | 3:
                combo_operand = operand
            case 4:
                combo_operand = reg_a
            case 5:
                combo_operand = reg_b
            case 6:
                combo_operand = reg_c
            case 7:
                illegal = True
            case _:
                pass

        match opcode:
            case 0 if not illegal:
                reg_a = int(reg_a / (2**combo_operand))
            case 1:
                reg_b = reg_b ^ operand
            case 2 if not illegal:
                reg_b = combo_operand % 8
            case 3 if reg_a != 0:
                    idx_opcode = operand - 2
            case 4: 
                reg_b = reg_b ^ reg_c
            case 5 if not illegal:
                out.append(combo_operand % 8)
                out_len += 1
                if skip and program[:out_len] != out:
                    break
            case 6 if not illegal:
                reg_b = int(reg_a / (2**combo_operand))
            case 7 if not illegal:
                reg_c = int(reg_a / (2**combo_operand))
            case _:
                pass
        
        idx_opcode += 2
        idx_operand = idx_opcode + 1
    return out

@time_solution
def part_2():
    # Brute force will be too slow (but works on test).
    # Back solve the calculation to limit what the values could be.

    # Lets start with A, 0, 0 for the codes.
    # How would this look if we apply the code.
    # ###
    # code : opeerand
    # ###
    # 2,4 -> B = A % 8
    # 1,3 -> B = B ^ 3
    # 7,5 -> C = A // (2**B)
    # 0,3 -> A = A // 8         [*]
    # 1,5 -> B = B ^ 5
    # 4,1 -> B = B ^ C
    # 5,5 -> out + (B mod 8)
    # 3,0 -> if A!= 0, go to start.
    
    # Conclusions:
    # P = len(program)
    # Therefore to get enough items in the output, from [*] mainly:
    # A > 8 ** (P) and A < 8 ** (P+1) []
    # 
    # I think there answer should therefore be of the form:
    # a * 8^P + b * 8^(P-1) + ... + y * 8 + z
    # where the coefficients are in 0-7.
    # Brute force solve for this by solving one coefficient at a time.
    # As the a coefficient determines the final value of the output program etc.

    # Due to how this is solved, it will only work on the full case and not the test.
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    reg_a, reg_b, reg_c, program = [row.split(": ")[-1] for row in data]
    reg_a = int(reg_a)
    reg_b = int(reg_b)
    reg_c = int(reg_c)
    program = [int(x) for x in program.split(",")]
    vals = [8**x for x in range(len(program))][::-1]
    

    solved = False
    attempts = [[]]
    # Find each digit in turn. Check to see if multiple digits can return the correct values.
    # Noting that when solving in turn like this, we are solving the first coefficient relates to final program values etc.
    # Sometimes there are multiple right answers for a given coefficient. Key track of all of these as
    # we can get to a state which won't work due to a 0. In which case drop the list.

    while True:
        next_attempts = []
        if attempts == []: 
            break

        for attempt in attempts:
            next_attempt = attempt.copy()
            found = len(attempt)
            if solved:
                break
            for a in range(1, 8):
                coeffs = attempt + [a]
                value = sum(a*b for a,b in zip(vals, coeffs))
                out = solve(value, reg_b, reg_c, program, False)

                if out == program:
                    # Check if we are finished.
                    next_attempts.append(next_attempt + [a])
                    solved = True
                    break
                
                if out[-found-1:] == program[-found-1:]:
                    # When cycling "a" this is the part we are solving for.
                    next_attempts.append(next_attempt + [a])

        # Update the attempts for the next check loop.
        attempts = next_attempts.copy()

    return value


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")