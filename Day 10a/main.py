import re
from operator import add
file_path = 'input.txt'

line_length = 0
with open(file_path, 'r') as file:
    sketch = []
    for line in file:
        sketch.append(line.strip())
    line_length = len(sketch[0])

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

            path.append(next_location)

            previous_location = location
            location = next_location

            if sketch[location[0]][location[1]] == 'S':
                # We found a loop!
                print(f'Path was {path}')
                print(f'Answer is {(len(path) - 1) / 2}')
                exit(0)

        print('Test')

    print('No path found')





