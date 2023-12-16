import math
file_path = 'input.txt'

with open(file_path, 'r') as file:
    grid = []
    for line in file:
        line = line.strip()
        grid.append(line)

    energized_tiles = set()

    def show_energized():
        header = ""
        for x in range(len(grid[0])):
            header += f"{x}"
        print(f"   {header} {header}")

        for y, line in enumerate(grid):
            lit_line = ""
            for x, char in enumerate(line):
                if (y,x) in energized_tiles:
                    lit_line += '#'
                else:
                    lit_line += '.'
            print(fr"{y}: {lit_line} {line}")
        print('')

    def apply_tile(direction, grid_loc):
        tile = grid[grid_loc[0]][grid_loc[1]]
        if tile == '/':
            return [(-1*direction[1], -1*direction[0])]
        elif tile == '\\':
            return [(1*direction[1], 1*direction[0])]
        elif tile == '|':
            if direction[1] == 0:
                return [direction]
            else:
                return [(1,0), (-1,0)]
        elif tile == '-':
            if direction[0] == 0:
                return [direction]
            else:
                return [(0,1), (0,-1)]
        else:
            print("Asked to apply '.'")
            return [direction]

    def follow_light(direction, start):
        # Direction is (1,0), (-1,0), etc
        # TODO: Store this as ranges, overlap at end?
        location = start
        while True:
            location = (location[0] + direction[0], location[1] + direction[1])
            if not (len(grid) > location[0] >= 0) or not (len(grid[0]) > location[1] >= 0):
                # Walked off the grid, we're done
                return []
            energized_tiles.add(location)
            tile = grid[location[0]][location[1]]
            if tile != '.':
                break

        new_directions = apply_tile(direction, location)
        return [(direction, location) for direction in new_directions]

    beams = [((0, 1), (0, -1))]
    seen_beams = set()
    while beams:
        beam = beams.pop()
        if beam in seen_beams:
            continue
        seen_beams.add(beam)
        new_beams = follow_light(beam[0], beam[1])
        beams.extend(new_beams)

        print(f'Finished beam {beam}, it made new beams {new_beams}')
        show_energized()

    print(f"Num squares lit {len(energized_tiles)}")


