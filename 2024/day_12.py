from aoc import aoc_read, time_solution

DAY = 12
TEST = False
SPLIT_LINES = True

def return_regions(data):
    # Store the grid size
    ROWS = len(data) - 1
    COLUMNS = len(data[0]) - 1

    # Find the unique plants
    plants = set(plant for row in data for plant in row)

    # Find all the individual regions of connected areas.
    # Store them in a dictionary.
    # They key will be of the form "LETTER_NUMBER".
    # The number is assigned in order that the region of that letter is found.
    regions = {}
    for plant in plants:
        # Get the coordinates of all cells with this plant value.
        plant_locations = [[idx, idy] for idx, row in enumerate(data) for idy, cell in enumerate(row) if cell == plant]
        
        # Keep track if all coordinates have been assigned.
        SEEN_POINTS = []

        # ID Number
        plant_num = 0
    
        for start in plant_locations:
            if start in SEEN_POINTS:
                # Region already mapped.
                continue
            regions[f"{plant}_{plant_num}"] = {}
            
            search_region = [start]
            SEEN_POINTS.append(start)
            found = [start]

            while True:
                if search_region == []:
                    break
                base = search_region[0]
                for direction in [[1,0], [-1, 0], [0, -1], [0, 1]]:
                    search_cell = [a + b for a, b in zip(base, direction)]
                    
                    # Check that the coords are valid.
                    if search_cell[0] < 0 or search_cell[0] > ROWS:
                        continue
                    if search_cell[1] < 0 or search_cell[1] > COLUMNS:
                        continue

                    if data[search_cell[0]][search_cell[1]] == plant and search_cell not in found:
                        search_region.append(search_cell)
                        found.append(search_cell)
                        SEEN_POINTS.append(search_cell)
                del search_region[0]

            regions[f"{plant}_{plant_num}"] = found
            plant_num +=1
    return regions
    
@time_solution
def part_1():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    regions = return_regions(data)

    areas = {plant: len(region) for plant, region in regions.items()}
            
    # # Calculate the perimeters.
    perimeters = {}
    for plant, region in regions.items():
        perimeters[plant] = None
        perimeter = 0
        for cell in region:
            for direction in [[1,0], [-1, 0], [0, -1], [0, 1]]:
                neighbour = [a + b for a, b in zip(cell, direction)]

                if neighbour not in region:
                    perimeter += 1
        perimeters[plant] = perimeter

    solution = sum([areas[key] * perimeters[key] for key in areas.keys()])
    return solution
    
@time_solution
def part_2():
    data = aoc_read(DAY, TEST, SPLIT_LINES)
    regions = return_regions(data)

        
    # Calculate the areas
    areas = {plant: len(region) for plant, region in regions.items()}
            
    # Search through cells for each region. Check each direction to see if this takes us outside of the shape.
    # if so, store the cell outside the shape and the direction to get there as a single list.
    perimeters = {}
    for plant, region_points in regions.items():
        perimeter_points = []
        for cell in region_points:
            for direction in [[1,0], [-1, 0], [0, -1], [0, 1]]:
                neighbour = [a + b for a, b in zip(cell, direction)]
                if neighbour not in region_points:
                    perimeter_points.append(neighbour + direction)
        perimeters[plant] = perimeter_points

    # Cycle over all of the cells surrounding each area. These were found in the perimeters section.
    # For each cell, group them together with neighbouring cells which were found using the same direction.
    # These must therefore be bordering cells that are outside the main cell. And hence, form a side.
    # If the direction is different or they are not neighbours, then they are not the same side.
    sides_detailed = {plant: [] for plant in perimeters.keys()}
    
    for plant, region_points in perimeters.items():
        SEEN_POINTS = []
        plant_sides = []
        for edge_cell in region_points:
            if edge_cell in SEEN_POINTS:
                continue
            search_side = [edge_cell]
            full_side = [edge_cell]
            while True:
                if search_side == []:
                    break
                base = search_side[0]
                SEEN_POINTS.append(base)

                for direction in [[1, 0, 0, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 1, 0, 0]]:
                    neighbour = [a + b for a, b in zip(base, direction)]
                    if neighbour in region_points and neighbour not in SEEN_POINTS:
                        full_side.append(neighbour)
                        SEEN_POINTS.append(neighbour)
                        search_side.append(neighbour)
                # Delete elements once they have been checked.
                del search_side[0]
            
            # Store the found side.
            plant_sides.append(full_side)
        
        # Store the list of all the sides.
        sides_detailed[plant] = plant_sides

    # Note that we can also get back to p1 by doing:
    # perimeters = {plant: sum([len(side) for side in all_sides]) for plant, all_sides in sides.items()}

    sides = {plant: len(all_sides) for plant, all_sides in sides_detailed.items()}
    solution = sum([areas[key] * sides[key] for key in areas.keys()])
    return solution



if __name__ == "__main__":
    print("\nRunning Calculations")
    solution_p1 = part_1()
    print(f"Solution to part 1: {solution_p1}")
    print("---")
    solution_p2 = part_2()
    print(f"Solution to part 2: {solution_p2}")
