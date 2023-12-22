from collections import deque
file_path = 'input.txt'

with open(file_path, 'r') as file:
    yard = []
    for line in file:
        line = line.strip()
        yard.append(list([*line]))

num_unwalkable = 0
for y in range(len(yard)):
    num_unwalkable += yard[y].count('#')

start = None
for y in range(len(yard)):
    for x in range(len(yard[0])):
        if yard[y][x] == 'S':
            start = (y, x)
            yard[y][x] = '.'
            break

    if start:
        break
else:
    raise ValueError('No start square')

max_y = len(yard)
max_x = len(yard[0])

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def apply_direction(coord, direction, num=1, infinite=False):
    next_coord = (coord[0] + direction[0]*num, coord[1] + direction[1]*num)
    if not infinite:
        if not (max_y > next_coord[0] >= 0) or not (max_x > next_coord[1] >= 0):
            return None
    return next_coord

def get_plot(coord):
    y = coord[0] % max_y
    x = coord[1] % max_x
    return yard[y][x]

def flood_fill_min_paths(starting_square):
    minimum_distances = {
        starting_square: 0,
    }

    squares_to_expand = deque([starting_square])
    while squares_to_expand:
        square = squares_to_expand.popleft()
        for direction in directions:
            next = apply_direction(square, direction, infinite=False)
            if next and next not in minimum_distances:
                if get_plot(next) != '#':
                    squares_to_expand.append(next)
                    minimum_distances[next] = minimum_distances[square] + 1

    return minimum_distances

minimum_distances_from_start = flood_fill_min_paths(start)
main_visitable_squares_even = set()
main_visitable_squares_odd = set()

even_diamond_tiles = set()
odd_diamond_tiles = set()

odd_corner_tiles = set()
even_corner_tiles = set()
for coord, distance in minimum_distances_from_start.items():
    if distance % 2 == 0: # I got even and odd backward and am leaving it to avoid renaming all the variables
        main_visitable_squares_odd.add(coord)
        if distance > 65:
            odd_corner_tiles.add(coord)
        else:
            odd_diamond_tiles.add(coord)
    else:
        main_visitable_squares_even.add(coord)
        if distance > 65:
            even_corner_tiles.add(coord)
        else:
            even_diamond_tiles.add(coord)

def print_map(visited_squares):
    for y in range(len(yard)):
        line = ''
        for x in range(len(yard[0])):
            if (y,x) in visited_squares:
                line += 'O'
            else:
                line += yard[y][x]
        print(f':{line}')
    print('')

print_map(even_diamond_tiles)

even_walkable_total = len(main_visitable_squares_even)
odd_walkable_total = len(main_visitable_squares_odd)
def sort_corners(corner_tiles):
    corners = [set(), set(), set(), set()]
    for coord in corner_tiles:
        vertical = 'top' if coord[0] < 65 else 'bottom'
        horizontal = 'left' if coord[0] < 65 else 'right'

        if vertical == 'top' and horizontal == 'left':
            corners[0].add(coord)
        elif vertical == 'top' and horizontal == 'right':
            corners[1].add(coord)
        elif vertical == 'bottom' and horizontal == 'right':
            corners[2].add(coord)
        elif vertical == 'bottom' and horizontal == 'left':
            corners[3].add(coord)
        else:
            raise ValueError("More than 65 away and doesn't go in a corner")
    return corners

odd_corners = sort_corners(odd_corner_tiles)
even_corners = sort_corners(even_corner_tiles)

even_corners_walkable = [0,0,0,0]
odd_corners_walkable = [0,0,0,0]
for i in range(4):
    even_corners_walkable[i] = len(even_corners[i])
    odd_corners_walkable[i] = len(odd_corners[i])

even_diamond_walkable = len(even_diamond_tiles)
odd_diamond_walkable = len(odd_diamond_tiles)

max_path_length = 26501365
side_length = int((max_path_length - 65) / 131)

total_walkable = 0

# Add the bottom triangle line
total_walkable += even_diamond_walkable + even_corners_walkable[0] + even_corners_walkable[1]
# And squares beside it
total_walkable += odd_corners_walkable[1]
total_walkable += odd_corners_walkable[0]

even = 0
odd = 1
lines = 0
while True:
    total_walkable += (odd_walkable_total * odd) + (even_walkable_total * even)
    lines += 1

    # Add the left
    total_walkable += even_diamond_walkable + even_corners_walkable[0] + even_corners_walkable[1] + even_corners_walkable[2]
    total_walkable += odd_corners_walkable[1]

    # Add the right
    total_walkable += even_diamond_walkable + even_corners_walkable[0] + even_corners_walkable[1] + even_corners_walkable[3]
    total_walkable += odd_corners_walkable[0]

    if even+odd+4 == ((side_length*2)+1):
        break

    even += 1
    odd += 1

# Add the center line
total_walkable += ((odd_walkable_total * (odd+1)) + (even_walkable_total * (even+1)))

# Add the left triangle
total_walkable += even_diamond_walkable + even_corners_walkable[1] + even_corners_walkable[2]

# Add the right triangle
total_walkable += even_diamond_walkable + even_corners_walkable[0] + even_corners_walkable[3]

# Now do the top of the structure

# Add the top triangle line
total_walkable += even_diamond_walkable + even_corners_walkable[2] + even_corners_walkable[3]
# And squares beside it
total_walkable += odd_corners_walkable[2]
total_walkable += odd_corners_walkable[3]

even = 0
odd = 1
lines = 0
while True:
    total_walkable += (odd_walkable_total * odd) + (even_walkable_total * even)
    lines += 1

    # Add the left
    total_walkable += even_diamond_walkable + even_corners_walkable[1] + even_corners_walkable[2] + even_corners_walkable[3]
    total_walkable += odd_corners_walkable[2]

    # Add the right
    total_walkable += even_diamond_walkable + even_corners_walkable[0] + even_corners_walkable[2] + even_corners_walkable[3]
    total_walkable += odd_corners_walkable[3]

    if even + odd + 4 == ((side_length * 2) + 1):
        break

    even += 1
    odd += 1

print(f'Final walkable squares {total_walkable}')
#608193767979991




