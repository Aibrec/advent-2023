import re
import json
import sys
import functools
import math
file_path = 'input.txt'
line_pattern = r'(.*) = \((.*), (.*)\)'

#directions ="LR"
directions = "LRLRRRLRRLRRRLRRRLLLLLRRRLRLRRLRLRLRRLRRLRRRLRLRLRRLLRLRRLRRLRRLRRRLLRRRLRRRLRRLRLLLRRLRRRLRLRRLRRRLRRLRLLLRRRLRRLRRLRRRLRRRLRRRLRLRLRLRRRLRRRLLLRRLLRRRLRLRLRRRLRRRLRRLRRRLRLRLLRRRLRLRRLRLRLRRLLLRRRLRRRLRRLRRLRLRRLLRRLRRRLRRRLLRRRLRRLRLLRRLRLRRLLRRRLLLLRRLRRRLRLRRLLRLLRRRLLRRLLRRRLRRRLRRLLRLRLLRRLLRLLLRRRR"
print(f'Directions have {len(directions)} steps')

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
        steps = len(directions)
        spot = direct_map[spot]
        while spot[2] != 'Z':
            spot = direct_map[spot]
            steps += len(directions)
        return steps, spot

    print(f'Started with {len(current_spots)}: {current_spots}')
    steps_required = []
    for spot in current_spots:
        minimum_steps_requried_to_end, end_spot = find_steps_until_z(spot)
        steps_required_from_z_to_next_z, second_end_spot = find_steps_until_z(end_spot)
        print(f'Spot {spot} requires {minimum_steps_requried_to_end} steps and ends on {end_spot}.')
        print(f'Spot {end_spot} requires {steps_required_from_z_to_next_z} steps and ends on {second_end_spot}.\n')
        # Every Z goes back to itself in the same number of steps neeed for the matching A to reach it, so that's nice of them.
        # If they didn't we would have to walk forward until a cycle formed, then find an lcm considering that. Glad we do not have to.
        steps_required.append(minimum_steps_requried_to_end)

    required_steps = math.lcm(*steps_required)
    print(f'lcm {required_steps}')
