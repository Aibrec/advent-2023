import networkx
file_path = 'input.txt'

with open(file_path, 'r') as file:
    forest = []
    for line in file:
        line = line.strip()
        forest.append(line)

directions = [(1,0), (-1,0), (0,1), (0,-1)]
def apply_direction(coords, direction):
    next_coord = (coords[0]+direction[0], coords[1]+direction[1])
    if not (len(forest) > next_coord[0] >= 0) or not (len(forest[0]) > next_coord[1] >= 0):
        return None
    else:
        return next_coord

def apply_slope(coords, slope):
    if slope == '^':
        next_coord = apply_direction(coords, (-1,0))
    elif slope == '>':
        next_coord = apply_direction(coords, (0, 1))
    elif slope == 'v':
        next_coord = apply_direction(coords, (1, 0))
    elif slope == '<':
        next_coord = apply_direction(coords, (0, -1))
    else:
        raise ValueError('unknown slope')

    if not (len(forest) > next_coord[0] >= 0) or not (len(forest[0]) > next_coord[1] >= 0):
        return None
    return next_coord

graph = networkx.DiGraph()
seen = set()
slopes = []

start = (0, forest[0].find('.'))
end = (len(forest)-1, forest[-1].find('.'))

complete_paths = []
open_paths = [(start, set([start]))]
while open_paths:
    coord, path = open_paths.pop()

    for direction in directions:
        adjacent = apply_direction(coord, direction)
        if adjacent and adjacent not in path:
            if adjacent == end:
                # End of the road
                path.add(adjacent)
                complete_paths.append(path)

            new_path = set(path)
            # Maybe there are slopes to slopes? haven't looked
            while forest[adjacent[0]][adjacent[1]] in '^>v<':
                new_path.add(adjacent)
                adjacent = apply_slope(adjacent, forest[adjacent[0]][adjacent[1]])
                if not adjacent or adjacent in path:
                    break
            else:
                if forest[adjacent[0]][adjacent[1]] == '.':
                    new_path.add(adjacent)
                    open_paths.append((adjacent, new_path))

longest_path = -1
for path in complete_paths:
    length = len(path) - 1 # We have the start square in the path
    print(f'Path length was {length}')
    longest_path = max(longest_path, length)
print(f'\nLongest path was {longest_path}')
