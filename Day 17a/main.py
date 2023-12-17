import math
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
        point = points_to_expand.pop()[1]
        new_points = expand_point(point)
        for p in new_points:
            if p[0] == goal:
                if best_paths[p[0]][p[1]][p[2]][0] < min_goal_score:
                    min_goal_score = best_paths[p[0]][p[1]][p[2]][0]
                    min_goal_point = p
            else:
                heapq.heappush(points_to_expand, (min_score_to_goal(p), p))

        if min_goal_point:
            points_to_expand = list([p for p in points_to_expand if p[0] < min_goal_score])

    #score_to_goal = best_paths[goal[0]][goal[1]][0]
    # goal_options = []
    # best_score = sys.maxsize
    # best_path = None
    # for dir in directions:
    #     for steps_taken in range(1, 4):
    #         option = (goal, dir, steps_taken)
    #         if option in best_paths:
    #             score = best_paths[option][0]
    #             if best_score > score:
    #                 best_score = score
    #                 best_path = best_paths[option][1]
    #             goal_options.append((option, best_paths[option]))

    # best_path = list([p[0] for p in best_path])
    print(f'Min goal score was {min_goal_score}')



