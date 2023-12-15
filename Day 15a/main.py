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

    total = 0
    for step in steps:
        value = helper_algorithm(step)
        total += value
        print(f'After {step} = {value}, {total}')
