import time
import functools
import sys
import heapq

start_time = time.time()

file_path = 'input.txt'
grid = []
with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        grid.append(list([int(n) for n in line]))

# coord format is (y,x)
# dir format is (0,1), (1,0), and the negatives
# Point format is (coord, dir, steps_taken, steps_required)

goal = (len(grid)-1, len(grid[0]) - 1)
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Path format is [coords]
# format is [coord][dir][steps]
best_paths = {}

for dir in directions:
    for i in range(11):
        best_paths[((0, 0), dir, i)] = (0, None)
for i in range(11):
    best_paths[((0, 0), (0, 0), i)] = (0, None)

def min_score_to_goal(point):
    # This is an underestimate due to the move 4 thing
    distance = abs(point[0][0] - goal[0]) + abs(point[0][1] - goal[1])
    score = best_paths[point][0]
    return score + distance

@functools.cache
def apply_direction(coord, direction):
    next_coord = (coord[0] + direction[0], coord[1] + direction[1])
    if not (len(grid) > next_coord[0] >= 0) or not (len(grid[0]) > next_coord[1] >= 0):
        return next_coord, None
    else:
        next_score = grid[next_coord[0]][next_coord[1]]
        return next_coord, next_score

@functools.cache
def apply_direction_4x(coord, direction):
    score = 0
    for i in range(4):
        coord, step_score = apply_direction(coord, direction)
        if step_score is None:
            score = None
            break
        else:
            score += step_score
    return coord, score

def expand_point(point):
    coord, direction, steps_taken = point
    score = best_paths[point][0]
    expanded = []
    for next_direction in directions:
        if next_direction == (direction[0]*-1, direction[1]*-1):
            continue  # Can't reverse direction

        if direction == next_direction:
            next_steps_taken = steps_taken + 1
            if next_steps_taken > 10:
                continue
            next_coord, add_score = apply_direction(coord, next_direction)
        else:
            next_steps_taken = 4
            next_coord, add_score = apply_direction_4x(coord, next_direction)

        if add_score is None:
            continue

        next_score = score + add_score
        next_point = (next_coord, next_direction, next_steps_taken)
        for fewer_steps in range(1, next_steps_taken+1):
            fewer_step_point = (next_coord, next_direction, fewer_steps)
            if fewer_step_point in best_paths:
                if best_paths[fewer_step_point][0] <= next_score:
                    # There's an existing path here with an equal or better score, and fewer steps taken. So continue
                    break
        else:
            # There's no existing path here with a better score or fewer steps, so we're the new best
            best_paths[next_point] = (next_score, point)
            expanded.append(next_point)
    return expanded

points_to_expand = [(sys.maxsize, ((0, 0), (0, 0), 0))]  # (min score, points)
min_goal_point = None
min_goal_score = sys.maxsize
while points_to_expand:
    point = heapq.heappop(points_to_expand)[1]
    new_points = expand_point(point)
    for p in new_points:
        if p[0] == goal:
            if best_paths[p][0] < min_goal_score:
                min_goal_score = best_paths[p][0]
                min_goal_point = p
                points_to_expand = list([p for p in points_to_expand if p[0] < min_goal_score])
        else:
            min_possible_score = min_score_to_goal(p)
            if min_possible_score < min_goal_score:
                heapq.heappush(points_to_expand, (min_score_to_goal(p), p))

end_time = time.time()
total_time = end_time - start_time
print(f'Min goal score was {min_goal_score}, took {round(total_time,2)}s')
