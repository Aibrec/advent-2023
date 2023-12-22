import re
import copy
import math
import functools
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

@functools.cache
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

@functools.cache
def squares_visitable_from(length, square, infinite=False):
    if length == 0:
        return {square}
    visitable_squares = set()
    for direction in directions:
        next = apply_direction(square, direction, infinite=infinite)
        if next and (get_plot(next) != '#'):
            visitable_from_this_square = squares_visitable_from(length-1, next)
            visitable_squares.update(visitable_from_this_square)
    return visitable_squares

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
for coord, distance in minimum_distances_from_start.items():
    if distance % 2 == 0:
        main_visitable_squares_even.add(coord)
    else:
        main_visitable_squares_odd.add(coord)

even_walkable_total = len(main_visitable_squares_even)
odd_walkable_total = len(main_visitable_squares_odd)

even_corners_walkable = [0,0,0,0]
odd_corners_walkable = [0,0,0,0]

# top left
row_length = 65
area = 0
for y in range(0, 65):
    line = ""
    for x in range(0, row_length):
        area += 1
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[0] += 1
        elif (y,x) in main_visitable_squares_odd:
            odd_corners_walkable[0] += 1
        line += yard[y][x]
    row_length -= 1
    #print(f"{y}: {line}")
print(f"Area was {area}\n")

# top right
area = 0
for y in range(0, 65):
    line = ""
    for x in range(66+y, 131):
        area += 1
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[1] += 1
        elif (y,x) in main_visitable_squares_odd:
            odd_corners_walkable[1] += 1
        line += yard[y][x]
    row_length -= 1
    #print(f"{y}: {line}")
print(f"Area was {area}\n")

# bottom right
row_length = 1
area = 0
for y in range(66, 131):
    line = ""
    for x in range(130, 130-row_length, -1):
        area += 1
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[2] += 1
        elif (y,x) in main_visitable_squares_odd:
            odd_corners_walkable[2] += 1
        line += yard[y][x]
    row_length += 1
    #print(f"{y}: {line}")
print(f"Area was {area}\n")

# bottom left
row_length = 1
area = 0
for y in range(66, 131):
    line = ""
    for x in range(0, row_length):
        area += 1
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[3] += 1
        elif (y,x) in main_visitable_squares_odd:
            odd_corners_walkable[3] += 1
        line += yard[y][x]
    row_length += 1
    #print(f"{y}: {line}")
print(f"Area was {area}\n")

#
# include_even_corners_walkable = [0,0,0,0]
# include_odd_corners_walkable = [0,0,0,0]
#
# # top left, to include
# row_length = 66
# area = 0
# for y in range(0, 66):
#     line = ""
#     for x in range(0, row_length):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             include_even_corners_walkable[0] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             include_odd_corners_walkable[0] += 1
#         line += yard[y][x]
#     row_length -= 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# # top right, to include
# area = 0
# for y in range(0, 66):
#     line = ""
#     for x in range(65+y, 131):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[1] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[1] += 1
#         line += yard[y][x]
#     row_length -= 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# # bottom right
# row_length = 1
# area = 0
# for y in range(66, 131):
#     line = ""
#     for x in range(130, 130-row_length, -1):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[2] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[2] += 1
#         line += yard[y][x]
#     row_length += 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")
#
# # bottom left
# row_length = 1
# area = 0
# for y in range(66, 131):
#     line = ""
#     for x in range(0, row_length):
#         area += 1
#         if (y,x) in main_visitable_squares_even:
#             even_corners_walkable[3] += 1
#         elif (y,x) in main_visitable_squares_odd:
#             odd_corners_walkable[3] += 1
#         line += yard[y][x]
#     row_length += 1
#     #print(f"{y}: {line}")
# print(f"Area was {area}\n")

# From notepad math, furthest we can go in a direction is 202300 full fields
# It's a taxicab circle, so each of the sides will have the same length in fields
max_path_length = 26501365
side_length = int((26501365 - 65) / 131)

# Total squares, 3+5+7... +(202300*2)+1 there's a formula for this but here's a loop
total_walkable = 0
even = 1
odd = 2
next_increase = 'even'
lines = 0
while True:
    total_walkable += (odd_walkable_total * odd) + (even_walkable_total * even)
    lines += 1

    if lines == 1:
        # Subtract for the bottom triangle
        total_walkable -= even_corners_walkable[2]
        total_walkable -= even_corners_walkable[3]

    # Subtract for the two outer edges
    if lines % 2 == 0:
        # On even, they cut off just the corner
        total_walkable -= even_corners_walkable[2]
        total_walkable -= even_corners_walkable[3]
    else:
        # On odd, they cut off all but a corner
        total_walkable -= (odd_walkable_total - odd_corners_walkable[0] - 130)
        total_walkable -= (odd_walkable_total - odd_corners_walkable[1] - 130)

    if even+odd == ((side_length*2)+1):
        break

    if next_increase == 'even':
        even += 2
        next_increase = 'odd'
    else:
        odd += 2
        next_increase = 'even'

# Add the center line
total_walkable += ((odd_walkable_total * odd) + (even_walkable_total * even))

# Subtract for the left triangle
total_walkable -= even_corners_walkable[0]
total_walkable -= even_corners_walkable[3]

# Subtract for the right triangle
total_walkable -= even_corners_walkable[1]
total_walkable -= even_corners_walkable[2]

# Now do the top of the structure
even = 1
odd = 2
next_increase = 'even'
lines = 0
while True:
    total_walkable += (odd_walkable_total * odd) + (even_walkable_total * even)
    lines += 1

    if lines == 1:
        # Subtract for the top triangle
        total_walkable -= even_corners_walkable[0]
        total_walkable -= even_corners_walkable[1]

    # Subtract for the two outer edges
    if lines % 2 == 0:
        # On even, they cut off just the corner
        total_walkable -= even_corners_walkable[1]
        total_walkable -= even_corners_walkable[0]
    else:
        # On odd, they cut off all but a corner
        total_walkable -= (odd_walkable_total - odd_corners_walkable[2] - 130)
        total_walkable -= (odd_walkable_total - odd_corners_walkable[3] - 130)

    if even+odd == ((side_length*2)+1):
        break

    if next_increase == 'even':
        even += 2
        next_increase = 'odd'
    else:
        odd += 2
        next_increase = 'even'

print(f'Final walkable squares {total_walkable}')
#608196733289489 was not right
#608193767979991 was right
visitables = []
# Just find some multiples and stick them in quadratic solver
for i in range(max_path_length):
    visited_squares = squares_visitable_from(i, start, infinite=True)
    print(f"{i}, {len(visited_squares)}")
    if (i-65) % 131 == 0:
        visitables.append(len(visited_squares))

def print_map(visited_squares):
    for y in range(len(yard)):
        line = ''
        for x in range(len(yard[0])):
            if (y,x) in visited_squares:
                line += 'O'
            else:
                line += yard[y][x]
        print(f'{y}: {line}')
    print('')
print_map(visited_squares)





