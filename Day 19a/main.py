import re
import copy

file_path = 'input.txt'
workflow_pattern = r'\b(\w+)\{(.*?)\}'

with open(file_path, 'r') as file:
    workflows = {}
    destinations_by_workflow = {}
    reading_workflows = True
    workflows_with_A = []
    for line in file:
        if line == '\n':
            break

        if reading_workflows:
            match = re.match(workflow_pattern, line)
            name = match.group(1)
            rules = match.group(2).split(',')

            functions = []
            possible_destinations = set()
            for i, rule in enumerate(rules):
                if i == (len(rules)-1):
                    result = rule
                    property = None
                    comparison = None
                    value = None
                else:
                    condition, result = rule.split(':')
                    property = condition[0]
                    comparison = condition[1]
                    value = int(condition[2:])

                possible_destinations.add(result)
                functions.append((result, property, comparison, value))
            workflows[name] = functions
            destinations_by_workflow[name] = possible_destinations

workflows_by_destination = {}
for name, workflow in workflows.items():
    for rule in workflow:
        destination = rule[0]
        if destination not in workflows_by_destination:
            workflows_by_destination[destination] = set()
        workflows_by_destination[destination].add(name)

def valid_range(range):
    return range[1] >= range[0]
def limit_range_workflow(name, possible_part, required_result):
    workflow = workflows[name]
    valid_parts = []

    for func in workflow:
        result, property, comparison, value = func
        if result == required_result:
            # This is the result we're looking for, update the possible part to make this true
            # Work on a clone so we can keep going. There may be another rule that sends us to this result
            part = copy.deepcopy(possible_part)

            if comparison is None:
                pass
            elif comparison == '>':
                part[property][0] = max(part[property][0], value+1)
            elif comparison == '<':
                part[property][1] = min(part[property][1], value-1)

            if property is None or valid_range(part[property]):
                valid_parts.append((name, part))

        # This is not the result we're looking for, update the possible part to make this false
        if comparison is None:
            break  # Default can't be made false
        elif comparison == '>':
            possible_part[property][1] = min(possible_part[property][1], value)
        elif comparison == '<':
            possible_part[property][0] = max(possible_part[property][0], value)

    return valid_parts

# Format is (workflow, part)
# Part format is {x,m,a,s: [min_allowed, max_allowed]}
possible_ranges = []
#for workflow in workflows_by_destination['A']:
maximally_permissible_part = {}
for letter in 'xmas':
    maximally_permissible_part[letter] = [1, 4000]
possible_ranges.append(('A', maximally_permissible_part))

accepted_parts = []
while possible_ranges:
    destination_workflow, possible_part = possible_ranges.pop()
    if destination_workflow == 'in':
        accepted_parts.append(possible_part)
    else:
        for source_workflow in workflows_by_destination[destination_workflow]:
            limited_ranges = limit_range_workflow(source_workflow, copy.deepcopy(possible_part), destination_workflow)
            possible_ranges.extend(limited_ranges)

score = 0
for part in accepted_parts:
    possible_options = 1
    for letter in 'xmas':
        options_for_letter = part[letter][1] - part[letter][0] + 1
        possible_options = possible_options * options_for_letter
    score += possible_options
print(f'score: {score}')