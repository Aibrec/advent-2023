import functools
import re
file_path = 'input.txt'

with open(file_path, 'r') as file:
    spring_records = []
    for line in file:
        line = line.strip()
        parts = line.split()
        springs = '?'.join([parts[0]] * 5)
        groups = tuple([int(n) for n in parts[1].split(',')]) * 5
        spring_records.append([springs, groups])

    def get_spring_group(line):
        group_size = 0
        line = line.strip('.')

        for i, char in enumerate(line):
            if char == '.':
                return group_size, line[i+1:], None
            elif char == '?':
                return 0, line, group_size
            else:
                group_size += 1

        return group_size, "", None

    @functools.cache
    def satisfies(springs, expected_spring_groups):
        springs = re.sub(r'\.+', '.', springs.strip('.'))
        expected_springs = '.'.join([n * '#' for n in expected_spring_groups])
        return springs == expected_springs

    @functools.cache
    def solve(springs, spring_groups):
        group_size, springs, incomplete_group_size = get_spring_group(springs)
        if group_size:
            if group_size != spring_groups[0]:
                return 0
            else:
                spring_groups = spring_groups[1:]

                # If there are no spring groups left, we've got a solution if there are no required springs left
                if not spring_groups:
                    return springs.find('#') == -1
        elif incomplete_group_size and incomplete_group_size > spring_groups[0]:
            return 0

        if springs.find('?') == -1:
            return satisfies(springs, spring_groups)
        else:
            return solve(springs.replace('?', '#', 1), spring_groups) + solve(springs.replace('?', '.', 1), spring_groups)

    total_count = 0
    for line, groups in spring_records:
        solutions = solve(line, groups)
        print(f'{line} had {solutions} solutions')
        total_count += solutions

    print(f'Total count was {total_count}')