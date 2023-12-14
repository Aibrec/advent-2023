import math
file_path = 'input.txt'

with open(file_path, 'r') as file:
    platform = []
    for line in file:
        line = line.strip()
        platform.append(tuple([c for c in line]))
    platform = tuple(platform)

    def rotate_clockwise(platform):
        return tuple([tuple([platform[y][x] for y in reversed(range(len(platform)))]) for x in range(len(platform[0]))])

    def tilt_north(platform):
        platform = list([list(line) for line in platform])
        for x in range(len(platform[0])):
            open_rock_y = 0
            for y in range(len(platform)):
                char = platform[y][x]
                if char == 'O':
                    platform[y][x] = '.'
                    platform[open_rock_y][x] = 'O'
                    open_rock_y += 1
                elif char == '.':
                    continue
                elif char == '#':
                    open_rock_y = y + 1

        platform = tuple([tuple(line) for line in platform])
        return platform

    def score_platform(platform):
        return sum([(len(platform) - y) * line.count('O') for y, line in enumerate(platform)])

    def perform_cycle(platform):
        for i in range(4):
            platform = tilt_north(platform)  # North
            platform = rotate_clockwise(platform)
        return platform

    def print_platform(platform):
        for n, line in enumerate(platform):
            print(f"{len(platform) - n}: {repr(''.join(list(line)))}")
        print('')

    target = 1000000000
    seen_platforms = {}
    n = 0
    skipped_ahead = False
    steps_after_skip = 0
    while n < target:
        if not skipped_ahead:
            if platform not in seen_platforms:
                seen_platforms[platform] = n
            else:
                print_platform(platform)
                print(f'Found a pattern seen on {seen_platforms[platform]} the reoccurs on {n} and scores {score_platform(platform)}')
                loops_between_repeats = n - seen_platforms[platform]
                loops_remaining = target - n
                loops_we_can_skip = math.floor(loops_remaining / loops_between_repeats)
                n = n + (loops_we_can_skip * loops_between_repeats)
                print(f'Skipped to loop {n}')
                skipped_ahead = True
        else:
            steps_after_skip += 1
            print(f'Taking step {steps_after_skip} after skip')

        platform = perform_cycle(platform)
        n += 1
        if n % (target/10000) == 0:
            print(f'Done n {n}, {round(n/target, 4)}')

    print_platform(platform)
    print(f'After {n} cycles, load is {score_platform(platform)}')