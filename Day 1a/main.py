import re

file_path = 'input.txt'
one_pattern = r'\b.*?(\d)'
two_pattern = r'\b.*?(\d).*(\d)'

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

        print(f"First two consecutive digits: {first_digit} {second_digit}")
        number = int(f"{first_digit}{second_digit}")
        sum += number

        print(f"Sum is {sum}")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
