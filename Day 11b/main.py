file_path = 'input.txt'


def findall(s, sub):
    pos = -1
    hits = []
    while (pos := s.find(sub, pos + 1)) > -1:
        hits.append(pos)
    return hits


with open(file_path, 'r') as file:
    universe = []
    columns_with_galaxy = set()
    empty_rows = set()
    for line in file:
        line = line.strip()
        universe.append(line)
        galaxies_x = findall(universe[-1], '#')
        if not galaxies_x:
            empty_rows.add(len(universe)-1)
        else:
            for x in galaxies_x:
                columns_with_galaxy.add(x)

    empty_columns = set(range(len(universe))) - columns_with_galaxy
    galaxy_locations = []
    for y, line in enumerate(universe):
        galaxies_x = findall(line, '#')
        for x in galaxies_x:
            galaxy_locations.append((y, x))

    def print_universe():
        for y, line in enumerate(universe):
            print(f'{y}: ', end="")
            for x, char in enumerate(line):
                if y in empty_rows or x in empty_columns:
                    print(f'X', end="")
                else:
                    print(f'{char}', end="")
            print("")

    def minimum_distance_between(a, b):
        # It's manhattan distance
        base_distance = (abs(a[0] - b[0]) + abs(a[1] - b[1]))

        # There's only 5/8 empties in the test set so I'm not bothering to do this in linear time
        y_start, y_end = sorted([a[0], b[0]])
        empty_rows_between = [y for y in empty_rows if y_end > y > y_start]

        x_start, x_end = sorted([a[1], b[1]])
        empty_columns_between = [x for x in empty_columns if x_end > x > x_start]

        multiplier = 1000000 - 1
        total_distance = base_distance + (multiplier * len(empty_columns_between)) + (multiplier * len(empty_rows_between))
        return total_distance

    total_distance = 0
    galaxy_pairs = [(a, b) for idx, a in enumerate(galaxy_locations) for b in galaxy_locations[idx + 1:]]
    for pair in galaxy_pairs:
        distance = minimum_distance_between(pair[0], pair[1])
        total_distance += distance

    print_universe()
    print(f'Total distance: {total_distance}')
