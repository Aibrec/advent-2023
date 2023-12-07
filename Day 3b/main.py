import re

file_path = 'input.txt'

line_length = 0
with open(file_path, 'r') as file:
    schematic = ""
    for line in file:
        line_length = len(line.strip())
        schematic += line.strip()

    stars = {}

    def find_adjacent_stars(i):
        adjacent_indexes = [i-line_length-1, i-line_length, i-line_length+1, i-1, i+1, i+line_length-1, i+line_length, i+line_length+1]
        local_stars = []
        for adj in adjacent_indexes:
            if adj >= 0 and adj < len(schematic):
                if schematic[adj] == "*":
                    local_stars.append(adj)
        return local_stars

    previous_digits = ""
    adjacent_stars = []
    for i, character in enumerate(schematic):
        if character.isdigit():
            previous_digits = previous_digits + character
            adjacent_stars.extend(find_adjacent_stars(i))
        else:
            if previous_digits and adjacent_stars:
                part_number = int(previous_digits)
                for star in adjacent_stars:
                    if star not in stars:
                        stars[star] = set()
                    stars[star].add(part_number)

            previous_digits = ""
            adjacent_stars = []

    sum = 0
    for star, parts in stars.items():
        if len(parts) == 2:
            parts = list(parts)
            sum += parts[0] * parts[1]

    print(f"Sum is {sum}")