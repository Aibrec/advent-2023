import re
import json
import sys
import functools
file_path = 'input.txt'

card_to_num_mapping = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}
# 5 of a kind is worth 7, 4 is 6, full house 5, 3 is 4, two pair is 3, pair is 2, high card is 1
rank_to_hand_name = {
    7: 'five of a kind',
    6: 'four of a kind',
    5: 'full house',
    4: 'three of a kind',
    3: 'two pair',
    2: 'pair',
    1: 'high card'
}


def compare_card(a, b):
    a_rank = card_to_num_mapping[a]
    b_rank = card_to_num_mapping[b]
    if a_rank > b_rank:
        return 1

    if a_rank < b_rank:
        return -1

    return 0


def rank_hand(hand):
    count_type = {}
    for card in hand:
        count_type[card] = count_type.get(card, 0) + 1

    count_to_card = {}
    for card, count in count_type.items():
        if count not in count_to_card:
            count_to_card[count] = []
        count_to_card[count].append(card)

    # 5 of a kind is worth 7, 4 is 6, full house 5, 3 is 4, two pair is 3, pair is 2, high card is 1
    if 5 in count_to_card:
        return 7
    elif 4 in count_to_card:
        return 6
    elif 3 in count_to_card and 2 in count_to_card:
        return 5
    elif 3 in count_to_card:
        return 4
    elif 2 in count_to_card and len(count_to_card[2]) == 2:
        return 3
    elif 2 in count_to_card:
        return 2
    else:
        return 1

def compare_hands(a, b):
    a_rank = rank_hand(a)
    b_rank = rank_hand(b)
    if a_rank > b_rank:
        return 1

    if a_rank < b_rank:
        return -1

    for i in range(5):
        result = compare_card(a[i], b[i])
        if result != 0:
            return result

    return 0


with open(file_path, 'r') as file:
    hands = {}
    for line in file:
        line = line.strip().split()
        hand = line[0]
        value = int(line[1])
        hands[hand] = value

    sorted_hands = sorted(hands.keys(), key=functools.cmp_to_key(compare_hands))

    total_winnings = 0
    for i in range(len(sorted_hands)):
        hand = sorted_hands[i]
        value = hands[hand]
        winnings = value * (i+1)
        name = rank_to_hand_name[rank_hand(hand)]
        print(f"Hand {hand} got rank {i+1} and won {winnings} with {name}")
        total_winnings += winnings

    print(total_winnings)