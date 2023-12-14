import functools
import re
file_path = 'input.txt'

with open(file_path, 'r') as file:
    platform = []
    for line in file:
        line = line.strip()
        platform.append(line)

    load = 0
    for x in range(len(platform[0])):
        open_rock_pos = 0
        for y in range(len(platform)):
            char = platform[y][x]
            if char == 'O':
                load += len(platform) - open_rock_pos
                open_rock_pos += 1
            elif char == '.':
                continue
            elif char == '#':
                open_rock_pos = y + 1

    print(f'load is {load}')