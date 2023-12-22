import heapq
file_path = 'input.txt'

with open(file_path, 'r') as file:
    falling_blocks = []
    max_x = 0
    max_y = 0
    for line in file:
        line = line.strip()
        left, right = line.split('~')
        left = tuple([int(i) for i in left.split(',')])
        right = tuple([int(i) for i in right.split(',')])
        heapq.heappush(falling_blocks, (min(left[2], right[2]), (left, right)))
        max_x = max(max_x, left[0], right[0])
        max_y = max(max_y, left[1], right[1])

def get_direction_of_block(block):
    dir_units = [0,0,0]
    non_zero_count = 0
    for i in range(3):
        dir = block[1][i] - block[0][i]
        if dir > 0:
            dir = 1
            non_zero_count += 1
        elif dir < 0:
            dir = -1
            non_zero_count += 1
        dir_units[i] = dir

    if non_zero_count > 1:
        raise ValueError("f")

    return tuple(dir_units)


def apply_direction(coords, direction):
    return (coords[0]+direction[0], coords[1]+direction[1], coords[2]+direction[2])


blocks_by_what_they_are_resting_on = {}
whats_resting_on_blocks_by_blocks = {}
grounded_blocks = {}

grid = []
for x in range(max_x+1):
    grid.append([[]])
    for y in range(max_y+1):
        grid[x].append([])

def drop_cube(block):
    # Assumes that blocks are straight
    cubes = []
    dir = get_direction_of_block(block)
    cube = block[0]
    while cube != block[1]:
        cubes.append(cube)
        cube = apply_direction(cube, dir)
    cubes.append(cube)

    # We can ignore the height of the block as we drop from the top
    cubes = list([(coord[0], coord[1]) for coord in cubes])
    resting_height = 0

    for cube in cubes:
        grid_column = grid[cube[0]][cube[1]]
        next_index_in_column = len(grid_column)
        if next_index_in_column > resting_height:
            resting_height = next_index_in_column

    blocks_by_what_they_are_resting_on[block] = set()
    for cube in cubes:
        grid_column = grid[cube[0]][cube[1]]
        while len(grid_column) < resting_height:
            grid_column.append(None)

        grid_column.append(block)

        if len(grid_column) > 1 and grid_column[-2] != None:
            block_we_are_resting_on = grid_column[-2]
            if block_we_are_resting_on == block:
                continue

            if block_we_are_resting_on not in whats_resting_on_blocks_by_blocks:
                whats_resting_on_blocks_by_blocks[block_we_are_resting_on] = set()
            whats_resting_on_blocks_by_blocks[block_we_are_resting_on].add(block)
            blocks_by_what_they_are_resting_on[block].add(block_we_are_resting_on)

highest_z_seen = 0
count = 0
while falling_blocks:
    count += 1
    original_height, lowest_block = heapq.heappop(falling_blocks)

    # if lowest_block[0][2] < highest_z_seen or lowest_block[1][2] < highest_z_seen:
    #     raise ValueError('went backward')
    highest_z_seen = max(highest_z_seen, lowest_block[0][2], lowest_block[1][2])

    print(f"{lowest_block[0]}~{lowest_block[1]}")
    drop_cube(lowest_block)
print("")


disintegratable = []
for block in blocks_by_what_they_are_resting_on.keys():
    blocks_resting_on_this_one = whats_resting_on_blocks_by_blocks.get(block, [])
    if not blocks_resting_on_this_one:
        disintegratable.append(block)
        continue

    for block_resting_on_this_one in blocks_resting_on_this_one:
        if len(blocks_by_what_they_are_resting_on[block_resting_on_this_one]) == 1:
            break
        elif len(blocks_by_what_they_are_resting_on[block_resting_on_this_one]) == 0:
            raise ValueError('How')
    else:
        disintegratable.append(block)

print(f"disintegratable blocks: {disintegratable}")
print(f"Num {len(disintegratable)}")
print("done")