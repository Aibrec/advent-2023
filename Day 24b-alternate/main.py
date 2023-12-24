import time
from shapely.geometry import LineString, Point

start_time = time.time()
file_path = 'input.txt'

# Let's consider from the perspective of the stone. It stays at some spot and does not move
# For simplicity, let's say it stays at 0,0, 0
#
# So another stone starts at 19,13,30 and that is it's position relative to us
# 	It continues -2,1,-2 and that remains relative to us if we are not moving
#
# What if our 'thrown' stone is moving at 1,1,1?
# 	t0: 19,13,30 : 0,0,0
# 	t1: 17,14,28 : 1,1,1
# 		Relative to us that is 16,13,27
#
# 	So its relative velocity is actually
# 		-3,0,-3 . So to get relative velocity we subtract our thrown velocity
#
# 	For what thrown velocity will we hit the rock? Or, for what thrown velocity will the rock cross 0,0,0 at some T
#
# 	So in general we can ask,  what velocity can we add to 3 numbers to get an intersection?
#
#
#
# What if our thrown stone started at 5,4,3
# 	t0: 19,13,30 : 5,4,3 | so relative to us, it's 14,9,27
# 	t1: 17,14,28 : 6,5,4 | so relative to us it's 11,9,24
#
# 	So it's relative velocity is -3,0,-3
# 		so the relative velocity is the same regardless of where we start

with open(file_path, 'r') as file:
    stones = []
    for line in file:
        line = line.strip()
        coord, velocity = line.split('@')
        coord = list([int(i) for i in coord.split(',')])
        velocity = list([int(i) for i in velocity.split(',')])
        stones.append((coord, velocity))

def apply_direction(coords, direction, ticks=1000000000000):
    next_coord = (coords[0]+direction[0]*ticks, coords[1]+direction[1]*ticks, coords[2]+direction[2]*ticks)
    return next_coord

def line_segment(coord, velocity):
    next_coord = apply_direction(coord, velocity)
    return LineString([coord, next_coord])

def subtract_coord(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

v_max = 300+1
v_min = -10

tolerance = 0.01
def compare_points(a,b):
    # Had rounding problems with shapely
    if abs(a.x - b.x) < tolerance:
        if abs(a.y - b.y) < tolerance:
            if abs(a.z - b.z) < tolerance:
                return True
    return False

test_stones = stones[:3]
for xd in range(v_min, v_max):
    for yd in range(v_min, v_max):
        for zd in range(v_min, v_max):
            thrown_velocity = (xd,yd,zd)
            test_stones_in_thrown_stone_reference_frame = list([(coord, subtract_coord(v, thrown_velocity)) for coord, v in test_stones])

            test_line_segments = list([line_segment(coord, velocity) for coord, velocity in test_stones_in_thrown_stone_reference_frame])
            first_intersection = test_line_segments[0].intersection(test_line_segments[1])
            if type(first_intersection) is Point:
                second_intersection = test_line_segments[1].intersection(test_line_segments[2])
                if type(second_intersection) is Point:
                    if compare_points(first_intersection, second_intersection):
                        print(f'Possibly point was: ({first_intersection.x}, {first_intersection.y}, {first_intersection.z}) with velocity {thrown_velocity}. Sum is {int(first_intersection.x) + int(first_intersection.y) + int(first_intersection.z)}')

print(f'Took {time.time() - start_time} seconds')
