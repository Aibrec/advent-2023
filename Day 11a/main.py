from operator import add
file_path = 'input.txt'

line_length = 0


def findall(s, sub):
    pos = -1
    hits = []
    while (pos := s.find(sub, pos + 1)) > -1:
        hits.append(pos)
    return hits

with open(file_path, 'r') as file:
    universe = []
    columns_with_galaxy = set()
    for line in file:
        universe.append(f'{line.strip()}')
        galaxies_x = findall(universe[-1], '#')
        if not galaxies_x:
            # No galaxies, double the line
            universe.append(f'{line.strip()}')
        else:
            for x in galaxies_x:
                columns_with_galaxy.add(x)

    def print_universe():
        for i, line in enumerate(universe):
            print(f'{i}: {line}')

    columns_to_double = list(set(range(len(universe))) - columns_with_galaxy)
    columns_to_double.sort(reverse=True)
    galaxy_locations = []
    for y, line in enumerate(universe):
        for column in columns_to_double:
            line = line[:column] + '.' + line[column:]
        universe[y] = line

        galaxies_x = findall(line, '#')
        for x in galaxies_x:
            galaxy_locations.append((y, x))

    def minimum_distance_between(a, b):
        # It's manhattan distance
        return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

    total_distance = 0
    galaxy_pairs = [(a, b) for idx, a in enumerate(galaxy_locations) for b in galaxy_locations[idx + 1:]]
    for pair in galaxy_pairs:
        distance = minimum_distance_between(pair[0], pair[1])
        total_distance += distance

    print_universe()
    print(f'Total distance: {total_distance}')
