file_path = 'input.txt'

with open(file_path, 'r') as file:
    spring_records = []
    for line in file:
        line = line.strip()
        parts = line.split()
        groups = list([int(n) for n in parts[1].split(',')])
        spring_records.append([parts[0], groups])

    def satisfies(line, expected_spring_groups):
        group_i = 0
        count = 0
        for i in line:
            if i == '#':
                count += 1
            else:
                if count > 0:
                    if group_i < len(expected_spring_groups) and count == expected_spring_groups[group_i]:
                        group_i += 1
                    else:
                        return False
                count = 0

        if count > 0:
            if group_i < len(expected_spring_groups) and count == expected_spring_groups[group_i]:
                group_i += 1
            else:
                return False

        return group_i == len(expected_spring_groups)

    def solve(line, spring_groups):
        # Returns number of combinations that satisfy all spring groups
        first_unknown = line.find('?')
        if first_unknown == -1:
            # Check if all groups satisfied
            if satisfies(line, spring_groups):
                #print(f'{line}')
                return 1
            else:
                return 0
        else:
            line_with_spring = line.replace('?', '#', 1)
            line_with_blank = line.replace('?', '.', 1)
            return solve(line_with_spring, spring_groups) + solve(line_with_blank, spring_groups)

    total_count = 0
    for line, groups in spring_records:
        solutions = solve(line, groups)
        print(f'{line} had {solutions} solutions')
        total_count += solutions

    print(f'Total count was {total_count}')