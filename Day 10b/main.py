from operator import add
file_path = 'input.txt'

line_length = 0
with open(file_path, 'r') as file:
    sketch = []
    for line in file:
        sketch.append(f'.{line.strip()}.')
    line_length = len(sketch[0])
    sketch.insert(0, '.' * line_length)
    sketch.append('.' * line_length)

    for i, line in enumerate(sketch):
        start_location = line.find('S')
        if start_location != -1:
            start_location = [i, start_location]
            break

    valid_directions = {
        '|':  [(-1, 0), (1, 0)],
        '-': [(0, -1), (0, 1)],
        'L': [(-1, 0), (0, 1)],
        'J': [(-1, 0), (0, -1)],
        '7': [(1, 0), (0, -1)],
        'F': [(1, 0), (0, 1)],
        'S': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        '.': [],
    }

    def direction_to(a, b):
        return (b[0]-a[0], b[1]-a[1])

    def possible_from_location(location):
        symbol = sketch[location[0]][location[1]]
        return [list(map(add, location, direction)) for direction in valid_directions[symbol]]

    def follow_pipe(from_location, location):
        symbol = sketch[location[0]][location[1]]
        for next_spot in possible_from_location(location):
            if len(sketch) > next_spot[0] >= 0 and line_length > next_spot[1] >= 0:
                if next_spot != from_location:
                    return next_spot  # TODO: Doesn't work with S, doesn't matter in part a
        return None

    def find_symbol_to_connect(s, b, c):
        for symbol in valid_directions.keys():
            if symbol == 'S' or symbol == '.':
                continue

            possible_with_symbol = [list(map(add, s, direction)) for direction in valid_directions[symbol]]
            for possible_location in possible_with_symbol:
                if possible_location != b and possible_location != c:
                    break
            else:
                return symbol

    def locations_connected(a, b):
        possible_from_a = possible_from_location(a)
        for option in possible_from_a:
            if option == b:
                break
        else:
            return False

        possible_from_b = possible_from_location(b)
        for option in possible_from_b:
            if option == a:
                break
        else:
            return False

        return True

    for location in possible_from_location(start_location):
        path = [start_location, location]

        previous_location = start_location
        while locations_connected(previous_location, location):
            next_location = follow_pipe(previous_location, location)
            if not next_location:
                break

            if sketch[next_location[0]][next_location[1]] == 'S':
                print(f'Answer is {(len(path) - 1) / 2}')

                s_should_be = find_symbol_to_connect(path[0], path[1], path[-1])
                sketch[start_location[0]].replace('S', s_should_be)

                path_set = set()
                for location in path:
                    path_set.add((location[0], location[1]))

                def directions_can_slip_between_locations(a, b):
                    if a not in path_set or b not in path_set:
                        return []

                    if a[0] == b[0]:
                        if a[1] > b[1]:
                            a,b = b,a # We want a to be closer to the left

                        symbols = f'{sketch[a[0]][a[1]]}{sketch[b[0]][b[1]]}'

                        if symbols in {'||', '|L', '|F', 'J|', 'JL', 'JF', '7|', '7L', '7F'}:
                            return [(1,0), (-1,0)]

                    if a[1] == b[1]:
                        if a[0] > b[0]:
                            a,b = b,a # We want a to be closer to the top

                        symbols = f'{sketch[a[0]][a[1]]}{sketch[b[0]][b[1]]}'

                        if symbols in {'--', '-7', '-F', 'L-', 'L7', 'LF', 'J-', 'J7', 'JF'}:
                            return [(0,1), (0,-1)]

                    return []

                outside_spots = set()

                def flood_slipping_between(a, b, direction):
                    a_next = (a[0] + direction[0], a[1] + direction[1])
                    b_next = (b[0] + direction[0], b[1] + direction[1])

                    if directions := directions_can_slip_between_locations(a_next, b_next):
                        if direction in set(directions):
                            flood_slipping_between(a_next, b_next, direction)

                    if directions := directions_can_slip_between_locations(a, a_next):
                        # Choose the direction away from b
                        direction = direction_to(b, a)

                        if direction in set(directions):
                            flood_slipping_between(a, a_next, direction)

                    if directions := directions_can_slip_between_locations(b, b_next):
                        # Choose the direction away from a
                        direction = direction_to(a, b)

                        if direction in set(directions):
                            flood_slipping_between(b, b_next, direction)

                    if a_next not in path_set:
                        next_spots.append(a_next)

                    if b_next not in path_set:
                        next_spots.append(b_next)

                def flood_from_location(location):
                    if location in outside_spots:
                        return []

                    outside_spots.add(location)

                    # Go out in all directions, including diagonal, stop when reaching the edge or path symbols
                    next_spots = []
                    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1,), (1, 0), (1, -1)]:
                        next_location = (location[0]+direction[0], location[1]+direction[1])
                        if next_location in outside_spots:
                            continue

                        if not (len(sketch) > next_location[0] >= 0 and line_length > next_location[1] >= 0):
                            continue

                        if next_location in path_set:
                            if direction[0] != 0 and direction[1] != 0:
                                continue

                            adjacent_locations = []
                            if direction[0] != 0:
                                adjacent_locations = [(next_location[0], next_location[1]+1), (next_location[0], next_location[1]-1)]
                            elif direction[1] != 0:
                                adjacent_locations = [(next_location[0]+1, next_location[1]), (next_location[0]-1, next_location[1])]

                            for adjacent_location in adjacent_locations:
                                possible_slip_directions = set(directions_can_slip_between_locations(adjacent_location, next_location))
                                if direction in possible_slip_directions:
                                    flood_slipping_between(adjacent_location, next_location, direction)
                        else:
                            next_spots.append(next_location)

                    return next_spots


                next_spots = flood_from_location((0, 0))  # We added a ring of empty spaces around the map, so 0,0 is always clear
                while next_spots:
                    spot = next_spots.pop()
                    next_spots.extend(flood_from_location(spot))

                contained_spots = set()
                for y in range(len(sketch)):
                    for x in range(len(sketch[0])):
                        spot = (y,x)
                        if spot not in path_set and spot not in outside_spots:
                            contained_spots.add(spot)

                # Make a nice to look at sketch
                nice_sketch = []
                for y in range(len(sketch)):
                    line = ""
                    for x in range(len(sketch[0])):
                        if (y,x) in path_set:
                            line = f'{line}{sketch[y][x]}'
                        elif (y,x) in contained_spots:
                             line = f'{line}*'
                        else:
                            line = f'{line}.'
                    nice_sketch.append(line)
                    print(line)

                print(f'Contained spots: {len(contained_spots)} | {contained_spots}')
                exit(0)

            path.append(next_location)

            previous_location = location
            location = next_location





