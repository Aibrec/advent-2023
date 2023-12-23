import time
import networkx

start_time = time.time()
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
def get_adjacent_tiles(coord, ignore_set=set(), ignore_tile=None):
    adjacent_tiles = []
    for direction in directions:
        adjacent = apply_direction(coord, direction)
        if adjacent and adjacent not in ignore_set and adjacent != ignore_tile and forest[adjacent[0]][adjacent[1]] in '.^>v<':
            adjacent_tiles.append(adjacent)
    return adjacent_tiles

start = (0, forest[0].find('.'))
end = (len(forest)-1, forest[-1].find('.'))

seen_coords = set(start)
open_paths = [(start, apply_direction(start, (1,0)))]  # Hardcoded, the path starts with a down in the example and real data
forks = set([start, end])

connecting_paths = set()
graph = networkx.Graph()
graph.add_node(start)
while open_paths:
    starting_fork, start_of_path = open_paths.pop()
    path = set([start_of_path])

    previous = None
    current = start_of_path
    while len(adjacents := get_adjacent_tiles(current, path, starting_fork)) == 1:
        adjacent = adjacents[0]
        if adjacent in forks:
            # We've reached the end of the path, and it's a previously seen fork
            # So this is a path from starting_fork, taking len(path) steps, and ending on adjacent
            ending_fork = adjacent
            path.add(current)
            break

        previous = current
        current = adjacent
        path.add(previous)
    else:
        if len(adjacents) == 0:
            # Dead end, abandon this path
            continue
        else:
        #elif len(adjacents) > 0:
            ending_fork = current

    # We have a path from starting_fork, taking len(path) steps, and ending on ending_fork
    if ending_fork not in forks:
        forks.add(ending_fork)
        graph.add_node(ending_fork)
        for adjacent in get_adjacent_tiles(ending_fork):
            if adjacent not in path:
                # TODO: Still going to have bounces here where the other end of this path is queued up, so hacking around that we dedupe on full path
                open_paths.append((ending_fork, adjacent))

    starting_fork, ending_fork = list(sorted([starting_fork, ending_fork]))
    path_tuple = tuple(sorted(path))
    full_path = (starting_fork, ending_fork, path_tuple)
    if full_path not in connecting_paths:
        connecting_paths.add(full_path)
        graph.add_edge(starting_fork, ending_fork, weight=len(path)+1)

start_to_end_paths = []
open_paths = [(start, set([start]), 0, [start])]
while open_paths:
    coord, path, path_weight, ordered_path = open_paths.pop()

    edges = graph.edges(coord, 'weight')
    for a, b, edge_weight in edges:
        next = a
        if next == coord:
            next = b

        if next not in path:
            next_path = set(path)
            next_path.add(next)
            next_ordered_path = list(ordered_path)
            next_ordered_path.append(next)

            if next == end:
                start_to_end_paths.append((path_weight + edge_weight, next_ordered_path))
            else:
                open_paths.append((next, next_path, path_weight + edge_weight, next_ordered_path))

longest_path = max([length for length, path in start_to_end_paths])
# for length, path in sorted(start_to_end_paths):
#     print(f'Path length was {length}: {len(path)} : {path}')
#     longest_path = max(longest_path, length)
print(f'\nLongest path was {longest_path}')
print(f'Took {time.time() - start_time} seconds')
