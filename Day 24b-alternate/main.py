import time
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

def apply_direction(coords, direction, ticks=200000000):
    next_coord = (coords[0]+direction[0]*ticks, coords[1]+direction[1]*ticks, coords[2]+direction[2]*ticks)
    return next_coord

def line_segment(coord, velocity):
    next_coord = apply_direction(coord, velocity)
    return LineString([coord, next_coord])

def subtract_coord(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

v_max = 100+ 1
v_min = -100

def compare_points(a,b):
    # Had rounding problems with shapely
    if int(a.x) == int(b.x):
        if int(a.y) == int(b.y):
            if int(a.z) == int(b.z):
                return True
    return False

test_stones = stones[:3]
for xd in range(v_min, v_max):
    for yd in range(v_min, v_max):
        for zd in range(v_min, v_max):
            # if xd == -3 and yd == 1 and zd == 2:
            #     print('Test correct')
            thrown_velocity = (xd,yd,zd)
            test_stones_in_thrown_stone_reference_frame = list([(coord, subtract_coord(v, thrown_velocity)) for coord, v in test_stones])
            test_line_segments = list([line_segment(coord, velocity) for coord, velocity in test_stones_in_thrown_stone_reference_frame])
            first_intersection = test_line_segments[0].intersection(test_line_segments[1])
            if type(first_intersection) is Point:
                second_intersection = test_line_segments[1].intersection(test_line_segments[2])
                if type(second_intersection) is Point:
                    if compare_points(first_intersection, second_intersection):
                        print(f'Starting point was: ({first_intersection.x}, {first_intersection.y}, {first_intersection.z}) with velocity {thrown_velocity}')
                        print(f"Sum is {int(first_intersection.x) + int(first_intersection.y) + int(first_intersection.z)}")
                        exit()

print(f'Took {time.time() - start_time} seconds')
