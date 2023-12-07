import re
import json
import sys
file_path = 'input.txt'
with open(file_path, 'r') as file:
    line_num = 0
    times = []
    distances = []
    for line in file:
        line = line.strip()
        line_num += 1

        if line_num == 1:
            times = list([int(num) for num in (line.split(':'))[1].split()])
            continue

        if line_num == 2:
            distances = list([int(num) for num in (line.split(':'))[1].split()])
            continue

    multipled_ways_to_win = 1
    for i in range(len(times)):
        time = times[i]
        ways_to_win = 0
        for hold_time in range(time+1):
            run_time = time - hold_time
            distance = run_time * hold_time
            if distance > distances[i]:
                ways_to_win += 1
        multipled_ways_to_win *= ways_to_win

    print(f'multipled_ways_to_win {multipled_ways_to_win}')