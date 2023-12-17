import sys
import heapq

file_path = 'input.txt'

with open(file_path, 'r') as file:
    grid = []
    for line in file:
        line = line.strip()
        grid.append(list([int(n) for n in line]))

    # coord format is (y,x)
    # dir format is (0,1), (1,0), and the negatives
    # Point format is (coord, dir, steps_taken)

    goal = (len(grid)-1, len(grid[0]) - 1)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Path format is [coords]
    # Format is [point][score] = (score, path)
    # New format is [coord][dir][steps]
    best_paths = {
        (0, 0): {
            (0, 1): [(0, None), (0, None), (0, None), (0, None)],
            (0, -1): [(0, None), (0, None), (0, None), (0, None)],
            (1, 0): [(0, None), (0, None), (0, None), (0, None)],
            (-1, 0): [(0, None), (0, None), (0, None), (0, None)],
        }
    }

    default_best = (sys.maxsize, None)
    default_dir = [default_best, default_best, default_best, default_best]

    def min_score_to_goal(point):
        distance = abs(point[0][0] - goal[0]) + abs(point[0][1] - goal[1])
        score = best_paths[point[0]][point[1]][point[2]][0]
        return score + distance

    def same_point_fewer_steps(point):
        fewer_steps = [(point[0], point[1], i) for i in range(point[2])]
        return list(fewer_steps)

    def expand_point(point):
        coord, direction, steps_taken = point
        score = best_paths[point[0]][point[1]][point[2]][0]
        expanded = []
        for next_direction in directions:
            if next_direction == (direction[0]*-1, direction[1]*-1):
                continue  # Can't reverse direction

            next_coord = (coord[0] + next_direction[0], coord[1] + next_direction[1])
            if not (len(grid) > next_coord[0] >= 0) or not (len(grid[0]) > next_coord[1] >= 0):
                continue

            if direction == next_direction:
                next_steps_taken = steps_taken + 1
                if next_steps_taken > 3:
                    continue
            else:
                next_steps_taken = 1

            next_score = score + grid[next_coord[0]][next_coord[1]]
            next_point = (next_coord, next_direction, next_steps_taken)

            if next_coord not in best_paths:
                best_paths[next_coord] = {
                    next_direction: default_dir.copy()
                }

            if next_direction not in best_paths[next_coord]:
                best_paths[next_coord][next_direction] = default_dir.copy()

            for steps in range(next_steps_taken+1):
                if best_paths[next_coord][next_direction][steps][0] <= next_score:
                    # There's an existing path here with an equal or better score, and fewer steps taken. So continue
                    break
            else:
                # There's no existing path here with a better score or fewer steps, so we're the new best
                best_paths[next_coord][next_direction][next_steps_taken] = (next_score, point)
                expanded.append(next_point)
        return expanded

    points_to_expand = [(sys.maxsize, ((0, 0), (0, 1), 0))]  # (min score, points)
    min_goal_point = None
    min_goal_score = sys.maxsize
    while points_to_expand:
        point = heapq.heappop(points_to_expand)[1]
        new_points = expand_point(point)
        for p in new_points:
            if p[0] == goal:
                if best_paths[p[0]][p[1]][p[2]][0] < min_goal_score:
                    min_goal_score = best_paths[p[0]][p[1]][p[2]][0]
                    min_goal_point = p
                    points_to_expand = list([p for p in points_to_expand if p[0] < min_goal_score])
            else:
                min_possible_score = min_score_to_goal(p)
                if min_possible_score < min_goal_score:
                    heapq.heappush(points_to_expand, (min_score_to_goal(p), p))

        if min_goal_point:
            points_to_expand = list([p for p in points_to_expand if p[0] < min_goal_score])

    print(f'Min goal score was {min_goal_score}')

    path_to_goal = []
    score_to_goal = 0
    point = min_goal_point
    best_paths_final = {}
    while True:
        coord = point[0]
        if coord == (0, 0):
            break

        score_of_coord = grid[coord[0]][coord[1]]
        score_to_goal += score_of_coord
        path_to_goal.append(coord)
        best_paths_final[point] = best_paths[point[0]][point[1]][point[2]]
        next_point = best_paths[point[0]][point[1]][point[2]][1]
        point = next_point

    path_to_goal.reverse()
    print(f'Path to goal was: {path_to_goal}')
    print(f'Score to goal was: {score_to_goal}')



