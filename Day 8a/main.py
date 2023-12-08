import re
import json
import sys
import functools
file_path = 'input.txt'
line_pattern = r'(.*) = \((.*), (.*)\)'

#directions ="LLR"
directions = "LRLRRRLRRLRRRLRRRLLLLLRRRLRLRRLRLRLRRLRRLRRRLRLRLRRLLRLRRLRRLRRLRRRLLRRRLRRRLRRLRLLLRRLRRRLRLRRLRRRLRRLRLLLRRRLRRLRRLRRRLRRRLRRRLRLRLRLRRRLRRRLLLRRLLRRRLRLRLRRRLRRRLRRLRRRLRLRLLRRRLRLRRLRLRLRRLLLRRRLRRRLRRLRRLRLRRLLRRLRRRLRRRLLRRRLRRLRLLRRLRLRRLLRRRLLLLRRLRRRLRLRRLLRLLRRRLLRRLLRRRLRRRLRRLLRLRLLRRLLRLLLRRRR"

with open(file_path, 'r') as file:
    current_spot = 'AAA'
    spots = {}
    for line in file:
        line = line.strip()
        match = re.search(line_pattern, line)
        spot = match.group(1)
        left = match.group(2)
        right = match.group(3)

        spots[spot] = (left, right)

        # if not current_spot:
        #     current_spot = spot

    steps = 0
    while current_spot != 'ZZZ':
        for direction in directions:
            if direction == 'L':
                current_spot = spots[current_spot][0]
            else:
                current_spot = spots[current_spot][1]
            steps += 1

    print(f'Number of steps {steps}')