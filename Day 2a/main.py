import re

file_path = 'input.txt'
game_pattern = r'Game (\d+):(.*)'
color_pattern = r'((\d+) (green|red|blue))'

max_values = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

with open(file_path, 'r') as file:
    game_id = 0
    sum = 0
    for line in file:
        game_id = game_id + 1
        match = re.search(game_pattern, line)
        games = match.group(2)
        draws = games.split(';')
        for draw in draws:
            color_sets = re.findall(color_pattern, line)
            for color_set in color_sets:
                color = color_set[2]
                num_shown = int(color_set[1])
                if max_values[color] < num_shown:
                    break
            else:
                continue
            break
        else:
            sum = sum + game_id

    print(f"Sum is {sum}")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
