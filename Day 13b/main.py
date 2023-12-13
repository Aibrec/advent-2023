import functools
import re
file_path = 'input.txt'

with open(file_path, 'r') as file:
    patterns = []
    current_pattern = []
    for line in file:
        line = line.strip()
        if not line:
            patterns.append(current_pattern)
            current_pattern = []
        else:
            current_pattern.append(line)

    if current_pattern:
        patterns.append(current_pattern)
        current_pattern = []

    def true_if_one_char_difference(a, b):
        if len(a) != len(b):
            return False

        differences_seen = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                differences_seen += 1
                if differences_seen > 1:
                    return False

        if differences_seen != 1:
            return False
        else:
            return True

    def find_vertical_reflection(pattern):
        bottom = pattern[0]
        for i in range(1, len(pattern)):
            top = ''.join([line for line in pattern[i:i+i]])
            if true_if_one_char_difference(bottom, top):
                return i
            else:
                bottom = pattern[i] + bottom

    def flip_pattern(pattern):
        flipped_pattern = list(["" for i in range(len(pattern[0]))])
        for i, line in enumerate(pattern):
            for i, char in enumerate(line):
                flipped_pattern[i] += char
        return flipped_pattern

    answer = 0
    for pattern in patterns:
        vertical_point = find_vertical_reflection(pattern)
        if vertical_point:
            print(f'Found vertical point {vertical_point}')
            answer += 100 * vertical_point
            continue

        reversed_vertical_point = find_vertical_reflection(list(reversed(pattern)))
        if reversed_vertical_point:
            print(f'Found reversed_vertical_point point {reversed_vertical_point}')
            answer += 100 * (len(pattern) - reversed_vertical_point)
            continue

        flipped_pattern = flip_pattern(pattern)

        horizontal_point = find_vertical_reflection(flipped_pattern)
        if horizontal_point:
            print(f'Found horizontal point {horizontal_point}')
            answer += horizontal_point
            continue

        reversed_horizontal_point = find_vertical_reflection(list(reversed(flipped_pattern)))
        if reversed_horizontal_point:
            print(f'Found reversed horizontal point {reversed_horizontal_point}')
            answer += len(flipped_pattern) - reversed_horizontal_point
            continue

        print(f'No flip found!')

    print(f'Answer is {answer}')