import re
import json
import sys
file_path = 'input.txt'
map_name_pattern = r'(.*)-to-(.*) map:'

copies_of_cards = {}

with open(file_path, 'r') as file:
    card_id = 0
    seed_ranges = []
    line_num = 0
    total_values_to_check = 0

    maps = []
    current_map = []

    for line in file:
        line = line.strip()

        line_num += 1
        if line_num == 1:
            seed_numbers = list([int(num) for num in (line.split(':'))[1].split()])
            for i in range(0, len(seed_numbers), 2):
                seed_ranges.append((seed_numbers[i], seed_numbers[i+1]))
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
            'range': (values[1], values[2]),
            'destination': values[0],
        })

    if current_map:
        maps.append(current_map)

    def create_null_mappings(map):
        mappings_by_range_start = {}
        for mapping in map:
            mappings_by_range_start[mapping['range'][0]] = mapping

        sorted_range_starts = sorted(mappings_by_range_start.keys())
        end_of_last_range = 0
        ordered_map = []
        for range_start in sorted_range_starts:
            size_of_gap = range_start - end_of_last_range
            if size_of_gap > 0:
                missing_range = (end_of_last_range, size_of_gap)
                ordered_map.append({'range': missing_range, 'destination': missing_range[0]})
            ordered_map.append(mappings_by_range_start[range_start])
            end_of_last_range = range_start + mappings_by_range_start[range_start]['range'][1]

        # Finally add a mapping to infinity
        ordered_map.append({'range': (end_of_last_range, sys.maxsize), 'destination': end_of_last_range})
        return ordered_map

    ordered_maps = []
    for map in maps:
        ordered_maps.append(create_null_mappings(map))

    def find_overlap(a_start, a_length, b_start, b_length):
        overlap_start = max(a_start, b_start)
        overlap_end = min(a_start+a_length-1, b_start+b_length-1)

        if overlap_end < overlap_start:
            return None

        if overlap_end < a_start or overlap_start < b_start:
            return None

        if overlap_start > (a_start+a_length-1) or overlap_start > (b_start+b_length-1):
            return None

        length_of_overlap = overlap_end - overlap_start + 1
        return (overlap_start, length_of_overlap)

    # seed_ranges
    mapped_ranges = seed_ranges
    for map in ordered_maps:
        transformed_ranges = []
        for mapped_range in mapped_ranges:
            for mapping in map:
                # This could be more efficient as we kept the mapping ranges ordered and could stop when we walked off the end
                # Ranges are a tuple (start, length)
                overlap_with_mapping = find_overlap(mapped_range[0], mapped_range[1], mapping['range'][0], mapping['range'][1])
                if overlap_with_mapping:
                    map_offset = mapping['destination'] - mapping['range'][0]
                    transformed_start = (overlap_with_mapping[0] + map_offset)
                    transformed_range = overlap_with_mapping[1]
                    transformed_ranges.append((transformed_start, transformed_range))
        mapped_ranges = transformed_ranges

    lowest_end = sys.maxsize
    for transformed_range in transformed_ranges:
        if transformed_range[0] < lowest_end:
            lowest_end = transformed_range[0]

    print(f"Lowest end was {lowest_end}")
    #print(f"Maps are {json.dumps(maps, indent=2)}")