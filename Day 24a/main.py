import time
import itertools
from shapely.geometry import LineString, Point

start_time = time.time()
file_path = 'input.txt'

with open(file_path, 'r') as file:
    stones = []
    for line in file:
        line = line.strip()
        coord, velocity = line.split('@')
        coord = list([int(i) for i in coord.split(',')])
        velocity = list([int(i) for i in velocity.split(',')])
        stones.append((coord, velocity))

def apply_direction(coords, direction, ticks=2000000000000000):
    next_coord = (coords[0]+direction[0]*ticks, coords[1]+direction[1]*ticks)
    return next_coord

lines = []
for coord, velocity in stones:
    coord = (coord[0], coord[1])
    next_coord = apply_direction(coord, velocity)
    lines.append(LineString([coord, next_coord]))

min_bound = 200000000000000
max_bound = 400000000000000
num_in_box = 0
for line1, line2 in itertools.combinations(lines, 2):
    intersection = line1.intersection(line2)
    if type(intersection) is Point:
        if max_bound >= intersection.x >= min_bound and max_bound >= intersection.y >= min_bound:
            num_in_box += 1

print(f'Num in box: {num_in_box}')
print(f'Took {time.time() - start_time} seconds')
