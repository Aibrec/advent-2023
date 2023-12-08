import re
import json
import sys
import functools
import math
file_path = 'input.txt'
line_pattern = r'(.*) = \((.*), (.*)\)'

#directions ="LR"
directions = "LRLRRRLRRLRRRLRRRLLLLLRRRLRLRRLRLRLRRLRRLRRRLRLRLRRLLRLRRLRRLRRLRRRLLRRRLRRRLRRLRLLLRRLRRRLRLRRLRRRLRRLRLLLRRRLRRLRRLRRRLRRRLRRRLRLRLRLRRRLRRRLLLRRLLRRRLRLRLRRRLRRRLRRLRRRLRLRLLRRRLRLRRLRLRLRRLLLRRRLRRRLRRLRRLRLRRLLRRLRRRLRRRLLRRRLRRLRLLRRLRLRRLLRRRLLLLRRLRRRLRLRRLLRLLRRRLLRRLLRRRLRRRLRRLLRLRLLRRLLRLLLRRRR"

with open(file_path, 'r') as file:
    current_spots = []
    spots = {}
    for line in file:
        line = line.strip()
        match = re.search(line_pattern, line)
        spot = match.group(1)
        left = match.group(2)
        right = match.group(3)

        spots[spot] = (left, right)

        if spot[2] == 'A':
            current_spots.append(spot)

    def reached_end():
        for spot in current_spots:
            if spot[2] != 'Z':
                return False
        return True

    def apply_directions(spot):
        for direction in directions:
            if direction == 'L':
                spot = spots[spot][0]
            else:
                spot = spots[spot][1]
        return spot

    direct_map = {}
    for spot in spots.keys():
        direct_map[spot] = apply_directions(spot)

    def find_steps_until_z(spot):
        steps = 0
        while spot[2] != 'Z':
            spot = direct_map[spot]
            steps += len(directions)
        return steps

    print(f'Started with {len(current_spots)}: {current_spots}')
    steps_required = []
    for spot in current_spots:
        minimum_steps_requried = find_steps_until_z(spot)
        print(f'Spot {spot} requires {minimum_steps_requried} steps')
        steps_required.append(minimum_steps_requried)

    required_steps = math.lcm(*steps_required)
    print(f'lcm {required_steps}')
