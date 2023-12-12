import functools
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
    def solve(springs, spring_groups):
        group_size, springs, incomplete_group_size = get_spring_group(springs)
        if group_size:
            if not spring_groups or group_size != spring_groups[0]:
                return 0
            else:
                spring_groups = spring_groups[1:]

                # If there are no spring groups left, we've got a solution if there are no required springs left
                if not spring_groups:
                    if springs.find('#') == -1:
                        return 1
                    else:
                        return 0
        elif incomplete_group_size and incomplete_group_size > spring_groups[0]:
            return 0

        first_unknown = springs.find('?')
        if first_unknown == -1:
            while spring_groups:
                group_size, springs, incomplete_group_size = get_spring_group(springs)
                if group_size != spring_groups[0]:
                    return 0
                else:
                    spring_groups = spring_groups[1:]

            if springs.find('#') == -1:
                return 1
            else:
                return 0
        else:
            line_with_spring = springs.replace('?', '#', 1)
            line_with_blank = springs.replace('?', '.', 1)
            return solve(line_with_spring, spring_groups) + solve(line_with_blank, spring_groups)

    total_count = 0
    for line, groups in spring_records:
        solutions = solve(line, groups)
        print(f'{line} had {solutions} solutions')
        total_count += solutions

    print(f'Total count was {total_count}')