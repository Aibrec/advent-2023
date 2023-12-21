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
        if next and (get_plot(next) == '.'):
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
                if get_plot(next) == '.':
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

# All paired left to right
top_left_corner = ((65,0), (0,65))
top_right_corner = ((0,65), (65,130))
bottom_left_corner = ((65,0), (130,65))
bottom_right_corner = ((130,65), (65,130))
corners = [top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner]
blocked_squares_in_corner = [0,0,0,0]

# There haven't been tested or validated

even_corners_walkable = [0,0,0,0]
odd_corners_walkable = [0,0,0,0]

# top left
for y in range(0, 65+1):
    for x in range(0, 65+1 - y):
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[0] += 1
        elif (y,x) in main_visitable_squares_even:
            odd_corners_walkable[0] += 1

# top right
for y in range(0, 65+1):
    for x in range(65, 130+1 - y):
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[1] += 1
        elif (y,x) in main_visitable_squares_even:
            odd_corners_walkable[1] += 1

# bottom right
for y in range(130, 65-1, -1):
    for x in range(65, y+1):
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[2] += 1
        elif (y,x) in main_visitable_squares_even:
            odd_corners_walkable[2] += 1

# bottom left
for y in range(130, 65-1, -1):
    for x in range(0, 130+1 - y):
        if (y,x) in main_visitable_squares_even:
            even_corners_walkable[3] += 1
        elif (y,x) in main_visitable_squares_even:
            odd_corners_walkable[3] += 1


# From notepad math, furthest we can go in a direction is 202300 full fields
# It's a manhatten circle, so each of the sides will have the same length in fields
# From notepad, the area cut off by the SE goes (-br_corner, all_stones - tl_corner, -br_corner, and repeats until ending in -br_corner). It repeats once for each unit of length in the side, so here it'll be 202300
max_path_length = 26501365
side_length = (26501365 - 65) / 131

walkable_removed_by_top = even_corners_walkable[0] + even_corners_walkable[1]
walkable_removed_by_right = even_corners_walkable[1] + even_corners_walkable[2]
walkable_removed_by_bottom = even_corners_walkable[2] + even_corners_walkable[3]
walkable_removed_by_left = even_corners_walkable[3] + even_corners_walkable[0]

removed_by_top_left_side = (((odd_walkable_total - odd_corners_walkable[2]) + (even_corners_walkable[0])) * side_length) + even_corners_walkable[0]
removed_by_top_right_side = (((odd_walkable_total - odd_corners_walkable[1]) + (even_corners_walkable[3])) * side_length) + even_corners_walkable[1]
removed_by_bottom_right_side = (((odd_walkable_total - odd_corners_walkable[2]) + (even_corners_walkable[0])) * side_length) + even_corners_walkable[2]
removed_by_bottom_left_side = (((odd_walkable_total - odd_corners_walkable[3]) + (even_corners_walkable[1])) * side_length) + even_corners_walkable[3]

total_walkable = 0
# Total squares, 3+5+7... +(202300*2)+1 there's a formula for this and I can't be bothered
even = 1
odd = 2
next_increase = 'even'
lines = 0
while True:
    total_walkable += (odd_walkable_total * odd) + (even_walkable_total * even)
    lines += 1

    if even+odd == ((side_length*2)+1):
        break

    if next_increase == 'even':
        even += 2
        next_increase = 'odd'
    else:
        odd += 2
        next_increase = 'even'

total_walkable += total_walkable + ((odd_walkable_total * odd) + (even_walkable_total * even))

to_remove = sum([removed_by_top_left_side, removed_by_top_right_side, removed_by_bottom_right_side, removed_by_bottom_left_side])
final = total_walkable - to_remove
print(f'Final walkable squares {final}')

#608192961611979 was not right

visitables = []
# Just find some multiples and stick them in quadratic solver #Correct answer was 608193767979991
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





