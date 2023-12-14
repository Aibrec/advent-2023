import copy
import functools
import re
import math
file_path = 'input.txt'

with open(file_path, 'r') as file:
    platform = []
    for line in file:
        line = line.strip()
        platform.append(tuple([c for c in line]))
    platform = tuple(platform)


    @functools.cache
    def rotate_clockwise(platform):
        #rotated_pattern = list([list([platform[y][x] for y in range(len(platform[0]))]) for x in range(len(platform))])
        rotated_pattern = []
        for x in range(len(platform)):
            rotated_pattern.append(tuple([platform[y][x] for y in reversed(range(len(platform)))]))
        return tuple(rotated_pattern)

    @functools.cache
    def tilt_north(platform):
        load = 0

        platform = list([list(line) for line in platform])
        for x in range(len(platform[0])):
            open_rock_y = 0
            for y in range(len(platform)):
                char = platform[y][x]
                if char == 'O':
                    load += len(platform) - open_rock_y
                    platform[y][x] = '.'
                    platform[open_rock_y][x] = 'O'
                    open_rock_y += 1
                elif char == '.':
                    continue
                elif char == '#':
                    open_rock_y = y + 1

        platform = tuple([tuple(line) for line in platform])
        return platform, load

    def score_platform(platform):
        load = 0
        for x in range(len(platform[0])):
            for y in range(len(platform)):
                char = platform[y][x]
                if char == 'O':
                    load += len(platform) - y
        return load

    @functools.cache
    def perform_cycle(platform):
        platform, load = tilt_north(platform)  # North

        platform = rotate_clockwise(platform)
        platform, load = tilt_north(platform)  # West

        platform = rotate_clockwise(platform)
        platform, load = tilt_north(platform)  # South

        platform = rotate_clockwise(platform)
        platform, load = tilt_north(platform)  # East

        platform = rotate_clockwise(platform)  # And now it's pointed like it arrived.

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