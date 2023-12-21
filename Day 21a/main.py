import re
import copy
import queue
import math
import functools
from collections import deque

file_path = 'input.txt'

with open(file_path, 'r') as file:
    yard = []
    for line in file:
        line = line.strip()
        yard.append(list([*line]))

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
def apply_direction(coord, direction):
    next_coord = (coord[0] + direction[0], coord[1] + direction[1])
    if not (max_y > next_coord[0] >= 0) or not (max_x > next_coord[1] >= 0):
        return None
    else:
        return next_coord

@functools.cache
def squares_visitable_from(length, square):
    if length == 0:
        return {square}
    visitable_squares = set()
    for direction in directions:
        next = apply_direction(square, direction)
        if next and (yard[next[0]][next[1]] == '.'):
            visitable_from_this_square = squares_visitable_from(length-1, next)
            visitable_squares.update(visitable_from_this_square)
    return visitable_squares


# len, current_square, set of visited squares
paths = [(0, start)]
max_path_length = 64
#for i in range(max_path_length):
visited_squares = squares_visitable_from(max_path_length, start)


# while paths:
#     path = paths.pop()
#     new_paths = extend_path(*path)
#     for path in new_paths:
#         if path[0] == max_path_length:
#             visited_squares.add(path[1])
#         else:
#             paths.append(path)
#     #print(f'paths remaining: {len(paths)}')

print(f"Done and visited {len(visited_squares)}")


