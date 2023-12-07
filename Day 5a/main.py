import re
import json
import sys
file_path = 'input.txt'
map_name_pattern = r'(.*)-to-(.*) map:'

copies_of_cards = {}

with open(file_path, 'r') as file:
    card_id = 0
    seeds = 0
    line_num = 0

    maps = []
    current_map = []

    for line in file:
        line = line.strip()

        line_num += 1
        if line_num == 1:
            seeds = list([int(num) for num in (line.split(':'))[1].split()])
            continue

        if not line:
            if current_map:
                maps.append(current_map)
            current_map = []
            continue

        match = re.search(map_name_pattern, line)
        if match:
            # If we need the names for part b deal with it then
            continue

        values = list([int(num) for num in line.split()])
        current_map.append({
            'source': values[1],
            'destination': values[0],
            'range': values[2] - 1,
        })

    if current_map:
        maps.append(current_map)

    lowest_end = sys.maxsize

    print(f"Seeds are {seeds}")
    for seed in seeds:
        current_value = seed
        for map in maps:
            for mapping in map:
                if mapping['range'] >= current_value - mapping['source'] >= 0:
                    new_value = current_value - mapping['source'] + mapping['destination']
                    #print(f"Mapped {current_value} to {new_value}")
                    current_value = new_value
                    break
            else:
                #print(f"No mapping found for {current_value}")
                current_value = current_value
        print(f"Seed {seed} mapped to {current_value}")

        if current_value < lowest_end:
            lowest_end = current_value

    print(f"Lowest end was {lowest_end}")
    #print(f"Maps are {json.dumps(maps, indent=2)}")