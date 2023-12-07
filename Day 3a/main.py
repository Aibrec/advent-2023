import re

file_path = 'input.txt'

line_length = 0
with open(file_path, 'r') as file:
    schematic = ""
    for line in file:
        line_length = len(line.strip())
        schematic += line.strip()

    def check_adjacent(i):
        adjacent_indexes = [i-line_length-1, i-line_length, i-line_length+1, i-1, i+1, i+line_length-1, i+line_length, i+line_length+1]
        for adj in adjacent_indexes:
            if adj >= 0 and adj < len(schematic):
                c = schematic[adj]
                if is_symbol(c):
                    return True
        return False

    def is_symbol(c):
        return c != '.' and not c.isdigit()

    sum = 0
    previous_digits = ""
    valid_part = False
    for i, character in enumerate(schematic):
        if character.isdigit():
            previous_digits = previous_digits + character
            if not valid_part:
                valid_part = check_adjacent(i)
        else:
            if previous_digits and valid_part:
                part_number = int(previous_digits)
                print(f"Valid part: {part_number}")
                sum += part_number

            previous_digits = ""
            valid_part = False

    print(f"Sum is {sum}")