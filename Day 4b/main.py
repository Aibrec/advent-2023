import re

file_path = 'input.txt'
card_pattern = r'Card (\d+):(.*)'

copies_of_cards = {}

with open(file_path, 'r') as file:
    card_id = 0
    total_scratch_cards = 0
    for line in file:
        card_id += 1
        game = (line.split(':')[1]).split('|')
        winning_numbers = set([int(num) for num in game[0].split()])
        got_numbers = list([int(num) for num in game[1].split()])
        num_matches = 0
        for number in got_numbers:
            if number in winning_numbers:
                num_matches += 1

        copies = copies_of_cards.get(card_id, 0) + 1
        total_scratch_cards += copies

        if num_matches > 0:
            for i in range(1, num_matches+1):
                won_card = card_id + i
                copies_of_cards[won_card] = copies_of_cards.get(won_card, 0) + copies

    print(f"total_scratch_cards is {total_scratch_cards}")

