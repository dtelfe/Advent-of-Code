from aoc import aoc_read, time_solution
from copy import copy, deepcopy

DAY = 24
TEST = False
SPLIT_LINES = False

# This problem is solved by
# - Looking for issues by checking sample simple binary numbers.
# - Inspecting the gates for the issue z codes.

@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)[:-1]
    wire_values, gates = cleanse(data)
    result = simulate(wire_values, gates)
    return result

def cleanse(data):
    split_point = data.index("")

    wire_values = data[:split_point]
    wire_values = [item.split(": ") for item in wire_values]
    wire_values = {wire: int(value) for wire, value in wire_values}

    gates = data[split_point+1:]
    gates = [gate.split(" ") for gate in gates]
    gates = {tuple(gate): False for gate in gates}
    return wire_values, gates

def simulate(wire_values, gates):
    while True:
        any_edit = False
        for instruction, done in gates.items():
            if any_edit or done:
                continue
            wire_values, edit = operate(instruction, wire_values)
            if edit:
                gates[instruction] = edit
                any_edit = True

        if not any_edit:
            break
    return get_nums(wire_values, "z")

def get_nums(wire_values, letter):
    num = {int(wire[1:]): value for wire, value in wire_values.items() if wire[0] == letter}
    num = sorted(num.items(), reverse=True)
    num = [str(x[1]) for x in num]
    num = ''.join(num)
    return int(num, 2)

def operate(instruction, wire_values):
    i_1 = instruction[0]
    op = instruction[1]
    i_2 = instruction[2]
    output = instruction[-1]

    if (i_1 not in wire_values.keys()) or (i_2 not in wire_values.keys()):
        return wire_values, False

    if op == "AND":
        result = wire_values[i_1] and wire_values[i_2]
    elif op == "OR":
        result = wire_values[i_1] or wire_values[i_2]
    elif op == "XOR":
        result = wire_values[i_1] ^ wire_values[i_2]
    else:
        assert False

    if output not in wire_values:
        wire_values[output] = 0
    
    wire_values[output] = result

    return wire_values, True

def correct(corrections, c_gates):
    c_gates = deepcopy(c_gates)
    for key, new_value in corrections.items():
        gate_keys = list(c_gates.keys())
        change_point = gate_keys.index(key)
        c_gates = {k: c_gates[k] for k in gate_keys[:change_point]} | {new_value: False} | {k: c_gates[k] for k in gate_keys[change_point+1:]}
    return c_gates

def solve(wire_values, gates):
    result = simulate(wire_values, gates)
    x = get_nums(wire_values, "x")
    y = get_nums(wire_values, "y")
    diff = (x + y) - result
    # print(f"\n{x} + {y} = {result} ({-diff})")
    return diff

def create_corrections(list_of_swaps, gates):
    corrections = {}
    for a, b in list_of_swaps:
        a_alt = tuple(list(a[:-1]) + [b[-1]])
        b_alt = tuple(list(b[:-1]) + [a[-1]])
        corrections[a] = a_alt
        corrections[b] = b_alt    
    return corrections

def check_bin_nums(data, corrections = None):
    single_gates = []
    store = {}
    for pt in range(0, 44 + 1):
        wire_values, gates = cleanse(data)
        if corrections is not None:
            gates = correct(corrections, gates)
        wire_values = {k: 0 for k in wire_values}
        if pt < 10:
            s_pt = "0" + str(pt)
        else:
            s_pt = str(pt)

        wire_values["x" + s_pt] = 1
        wire_values["y" + s_pt] = 1
        base_diff = solve(wire_values, gates)
        if base_diff != 0:
            bin_diff = str(bin(base_diff))
            sssss = bin_diff.index("b")
            bin_diff = bin_diff[sssss+1:]
            bit_diff = len(bin_diff) - 1 - [*bin_diff].index('1')
            print(f"Base diff {pt} {base_diff} | {bin_diff} | {[*bin_diff].count('1')} | {bit_diff}")
            
            str_bit_diff = str(bit_diff)
            if len(str_bit_diff) == 1:
                str_bit_diff = "z0" + str_bit_diff
            else:
                str_bit_diff = "z" + str_bit_diff

            if str_bit_diff not in single_gates:
                single_gates.append(str_bit_diff)
                store[pt] = str_bit_diff
    return store, single_gates

def print_gate_analysis(gates, gates_to_analyse):
    full = {}
    previous = []
    for single in gates_to_analyse:
        final_check_gates = expand([single], gates)
        full[single] = [x for x in final_check_gates if x not in previous]
        previous = final_check_gates

    # Inspect the issue points.
    for k, v in full.items():
        print(f"\n{k}")
        for vv in v:
            print(vv)
    return full

@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)[:-1]
    wire_values, gates = cleanse(data)

    SWAPS = [
        [('wvr', 'XOR', 'jgw', '->', 'fkp'), ('bpp', 'OR', 'ghf', '->', 'z06')], # by inspecting z06
        [('jpp', 'XOR', 'stv', '->', 'ngr'), ('stv', 'AND', 'jpp', '->', 'z11')], # by inspecting z11
        [('mgq', 'XOR', 'tpf', '->', 'mfm'), ('y31', 'AND', 'x31', '->', 'z31')], # by inspecting z31
        [('y38', 'XOR', 'x38', '->', 'krj'), ('y38', 'AND', 'x38', '->', 'bpt')] # by inspecting z38
    ]
    corrections = create_corrections(SWAPS, gates)
    gates = correct(corrections, gates)

    # Check addition of each of the binary pairs: 1 + 1, 10 + 10, 100 + 100, ....
    # See what the difference is a keep track of the location of the difference.
    print("\n----\nBasic Add Checks\n----")
    store, single_gates = check_bin_nums(data, None)
    
    # For an issue gate, ex z05. Look at the gates prior to this to look for an error.
    # e.g. passing 
    # single_gates = ["z03", "z04", "z05", "z06"]
    single_gates = ["z08", "z09", "z10", "z11", "z12"]
    # single_gates = ["z28", "z29", "z30", "z31", "z32"]
    # single_gates = ["z35", "z36", "z37", "z38", "z39"]
    print("\n----\nGate Analysis\n----")
    print_gate_analysis(gates, single_gates)

    # This gate analysis only shows the new codes relative to the previous step. 
    # (The first code will show all, and hence will go all the way back to x00 and y00.)
    # As these gates work in layers and share a lot of repeated code.

    # Explanation of noted patterns. Explained for z10:
    # z10 should be created from a XOR statements. i.e. aaa XOR bbb -> z10.
    # one of these should come from the XOR of x10 and y10. i.e. x10 XOR y10 -> aaa.
    # The other should come from an OR statement. i.e. ccc OR ddd -> bbb
    # Now one of these should come from the and of the previous step. i.e. x09 AND y09 -> ccc
    # The other should be the AND application of the previous z step. i.e. if eee XOR fff -> z09, then eee AND fff -> ddd

    # Validate swaps
    print("\n----\nCheck swaps on the binary number samples.\n----")
    data = aoc_read(DAY, TEST, SPLIT_LINES, False)[:-1]
    corrections = create_corrections(SWAPS, gates)
    store, single_gates = check_bin_nums(data, corrections)
    # If no issues are printed, then it is corrected for the sample binary numbers.
    print("----\nEnd of issues.")
    

    result = [[x[-1] for x in pair] for pair in SWAPS]
    result = [item for pair in result for item in pair]
    return ",".join(sorted(result))


def expand(single_gates, gates):
    final_check_gates = []
    while True:
        base = len(single_gates)
        check_points = []
        for check_gate in single_gates:
            for gate in gates:
                if check_gate == gate[-1]:
                    check_points.append(gate)
                    if gate not in final_check_gates:
                        final_check_gates.append(gate)
        
        for pt in check_points:
            for pt in check_points:
                if pt[0] not in single_gates:
                    single_gates.append(pt[0])
                if pt[2] not in single_gates:
                    single_gates.append(pt[2])
        
        if len(single_gates) == base:
            break
    return final_check_gates

if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")