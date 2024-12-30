from aoc import aoc_read, time_solution

DAY = 23
TEST = False
SPLIT_LINES = False


@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    pairs = {}
    for row in data:
        comp_from = row[:2]
        comp_to = row[-2:]

        if comp_from not in pairs:
            pairs[comp_from] = []

        if comp_to not in pairs:
            pairs[comp_to] = []

        pairs[comp_from].append(comp_to)
        pairs[comp_to].append(comp_from)

    triples = []
    for key, values in pairs.items():
        for value in values:
            overlap = set(pairs[value]).intersection(set(values))
            if overlap != set():
                for item in overlap:
                    combo = sorted([key, value, item])
                    combo = tuple(combo)

                    if combo not in triples:
                        triples.append(combo)

    triples = sorted(triples)
    triples_check = ["t" in [x[0] for x in triple] for triple in triples]

    return triples_check.count(True)


def check_nodes(nodes, graph):
    for idx, node in enumerate(nodes):
        for node2 in nodes[idx:]:
            if node2 not in graph[node]:
                return False
    return True


def all_check_nodes(nodes, graph):
    ops = []
    for idx in range(len(nodes)):
        test_nodes = nodes.copy()
        del test_nodes[idx]

        if check_nodes(test_nodes, graph):
            return test_nodes

        ops.append(all_check_nodes(test_nodes, graph))
    return ops


def bk(graph, current_clique, candidates, excludes, cliques):
    # Bron-Kerbosch Algorithm
    if candidates == [] and excludes == []:
        cliques.append(current_clique)
        return

    for candidate in candidates.copy():
        new_candidates = [c for c in candidates if c in graph[candidate]]
        new_excludes = [e for e in excludes if e in graph[candidate]]
        bk(graph, current_clique + [candidate], new_candidates, new_excludes, cliques)
        candidates.remove(candidate)
        excludes.append(candidate)
    return cliques


@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    pairs = {}
    for row in data:
        comp_from = row[:2]
        comp_to = row[-2:]

        if comp_from not in pairs:
            pairs[comp_from] = []

        if comp_to not in pairs:
            pairs[comp_to] = []

        pairs[comp_from].append(comp_to)
        pairs[comp_to].append(comp_from)

    nodes = list(pairs.keys())
    solution = bk(pairs, [], nodes, [], [])
    best = max([len(x) for x in solution])
    solution = [x for x in solution if len(x) == best][0]

    lan_party = sorted(solution)
    return ",".join(lan_party)


if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
