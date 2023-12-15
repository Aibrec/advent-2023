import math
file_path = 'input.txt'

with open(file_path, 'r') as file:
    steps = []
    for line in file:
        line = line.strip()
        steps = line.split(',')
    def helper_algorithm(string):
        value = 0
        for char in string:
            value = ((value + ord(char)) * 17) % 256
        return value
    def splitter(string):
        if string[-1] == '-':
            label = string[:-1]
            operation = '-'
            strength = None
        elif string[-2] == '=':
            label = string[:-2]
            operation = '='
            strength = string[-1]
        else:
            raise ValueError('Probably a 2 length strength')

        box_num = helper_algorithm(label)
        return box_num, label, operation, strength

    boxes = list({'order': [], 'labels': {}} for i in range(256))

    def print_boxes(boxes):
        for i, box in enumerate(boxes):
            string_version = f""
            if box['labels']:
                for label in box['order']:
                    if label is None:
                        continue

                    if label in box['labels']:
                        power, position = box['labels'][label]
                        string_version = f"{string_version}[{label} {power}] "
            if string_version:
                print(f"Box {i}: {string_version}")
        print("")

    def focusing_power(boxes):
        total_power = 0
        for box_num, box in enumerate(boxes):
            string_version = f""
            box_power = 0
            if box['labels']:
                slot_number = 1
                for label in box['order']:
                    if label is None:
                        continue

                    if label in box['labels']:
                        focal_length, position = box['labels'][label]
                        focusing_power = (box_num+1) * slot_number * int(focal_length)
                        box_power += focusing_power
                        string_version = f"{string_version}[{label} {focal_length} {focusing_power}] "
                        slot_number += 1
            if string_version:
                print(f"Box {box_num}, power {box_power}: {string_version}")
                total_power += box_power
        print(f"Total power was: {total_power}")
        return total_power

    total = 0
    for step in steps:
        box_num, label, operation, strength = splitter(step)
        box = boxes[box_num]
        if operation == '=':
            if label not in box['labels']:
                box['order'].append(label)  # So we're keeping these lists in reverse
                box['labels'][label] = [strength, len(box['order']) - 1]
            else:
                box['labels'][label][0] = strength
        else:
            #opertion is '-'
            if label in box['labels']:
                box_spot = box['labels'][label][1]
                del box['labels'][label]
                box['order'][box_spot] = None
                # Just leaving tit in the list though

        print(f"After {step}:")
        print_boxes(boxes)

    print(f"Finally:")
    focusing_power(boxes)


