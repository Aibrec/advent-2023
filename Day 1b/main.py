import re

file_path = 'input.txt'
one_pattern = r'\b.*?(one|two|three|four|five|six|seven|eight|nine|\d)'
two_pattern = r'\b.*?(one|two|three|four|five|six|seven|eight|nine|\d).*(one|two|three|four|five|six|seven|eight|nine|\d)'

words_to_numbers = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    # Iterate through the file object
    sum = 0
    for line in file:
        match = re.search(two_pattern, line)
        if match:
            # Get the matched substring containing the first two consecutive digits
            first_digit = match.group(1)
            second_digit = match.group(2)
        else:
            match = re.search(one_pattern, line)
            if match:
                first_digit = match.group(1)
                second_digit = first_digit
            else:
                print(f"No match found for {line.strip()}")

        first_digit = words_to_numbers[first_digit]
        second_digit = words_to_numbers[second_digit]
        print(f"First two consecutive digits: {first_digit} {second_digit}")
        number = int(f"{first_digit}{second_digit}")
        sum += number

        print(f"Sum is {sum}")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
