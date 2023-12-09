import re
import json
import sys
import functools
import math
file_path = 'input.txt'
line_pattern = r'(.*) = \((.*), (.*)\)'

with open(file_path, 'r') as file:
    histories = []
    for line in file:
        line = line.strip()
        history = (list([int(n) for n in line.split()]))
        histories.append([history])

    def calculate_next_line(history):
        next_line = []
        non_zero_present = False
        for i in range(1, len(history)):
            new_value = history[i] - history[i-1]
            if new_value != 0:
                non_zero_present = True
            next_line.append(new_value)
        return next_line, non_zero_present

    def extrapolate_history(history):
        for i in range(len(history)-2, -1, -1):
            # Last value adds the value in the row below it
            last_value_from_row_below = history[i+1][-1]
            last_in_current = history[i][-1]
            history[i].append(last_in_current + last_value_from_row_below)

    for i in range(len(histories)):
        line = histories[i][0]
        non_zero_present = True
        while non_zero_present:
            print(f'Line: {line}')
            next_line, non_zero_present = calculate_next_line(line)
            histories[i].append(next_line)
            line = next_line
        print(f'Line: {line}\n')

    sum_of_new_values = 0
    for history in histories:
        extrapolate_history(history)
        sum_of_new_values += history[0][-1]
        for line in history:
            print(f'Extrapolated: {line}')
        print('\n')

    print(f'Sum of new values: {sum_of_new_values}')
    #print(json.dumps(histories, indent=2))