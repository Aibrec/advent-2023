from shapely import Polygon
file_path = 'input.txt'

letter_to_dir = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

adjustments = {
    ((1, 0), (0, 1)): (-0.5, 0.5),  # Down then right
    ((1, 0), (0, -1)): (0.5, 0.5),  # Down then left
    ((-1, 0), (0, 1)): (-0.5, -0.5),  # Up Right
    ((-1, 0), (0, -1)): (0.5, -0.5),  # Up Left
    ((0, 1), (1, 0)): (-0.5, 0.5),  # Right then down
    ((0, 1), (-1, 0)): (-0.5, -0.5),  # Right then up
    ((0, -1), (1, 0)): (0.5, 0.5),  # Left then down
    ((0, -1), (-1, 0)): (0.5, -0.5),  # Left then up
}

def move_to_outside_corner(point, dir_in, dir_out):
    adjustment = adjustments[(dir_in, dir_out)]
    new_point = (point[0] + adjustment[0], point[1] + adjustment[1])
    return new_point

with open(file_path, 'r') as file:
    raw_coords = []
    coords = []
    outside = 0
    previous_dir = letter_to_dir['U']
    previous_coord = (0.5,0.5)
    for line in file:
        line = line.strip()
        parts = line.split()

        dir = letter_to_dir[parts[0]]
        distance = int(parts[1])

        raw_coords.append(previous_coord)
        adjusted_previous_coord = move_to_outside_corner(previous_coord, previous_dir, dir)
        coords.append(adjusted_previous_coord)

        previous_dir = dir
        previous_coord = (previous_coord[0] + dir[0]*distance, previous_coord[1] + dir[1]*distance)

coords.append(coords[0])
polygon = Polygon(coords)
area = polygon.area
print(f'Roords were {raw_coords}')
print(f'Coords were {coords}')
print(f'Area is {area}')