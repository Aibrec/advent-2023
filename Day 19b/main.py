import re
file_path = 'input.txt'
workflow_pattern = r'\b(\w+)\{(.*?)\}'

with open(file_path, 'r') as file:
    workflows = {}
    parts = []
    reading_workflows = True
    for line in file:
        if line == '\n':
            reading_workflows = False
            continue

        if reading_workflows:
            match = re.match(workflow_pattern, line)
            name = match.group(1)
            rules = match.group(2).split(',')

            lambdas = []
            for i, rule in enumerate(rules):
                if i == (len(rules)-1):
                    # Last rule
                    lambdas.append(lambda part,rule=rule: rule)
                else:
                    condition, result = rule.split(':')
                    property_name = condition[0]
                    comparison = condition[1]
                    value = int(condition[2:])

                    if comparison == '>':
                        lambdas.append(lambda part,property_name=property_name,value=value,result=result: result if part[property_name] > value else None)
                    elif comparison == '<':
                        lambdas.append(lambda part,property_name=property_name,value=value,result=result: result if part[property_name] < value else None)
                    else:
                        raise ValueError('Unknown comparison')
            workflows[name] = lambdas
        else:
            part = {}
            properties = (line.strip())[1:-1].split(',')
            for property in properties:
                name, value = property.split('=')
                part[name] = int(value)
            parts.append(part)

def apply_workflow(name, part):
    workflow = workflows[name]
    for func in workflow:
        result = func(part)
        if result is None:
            continue
        else:
            return result

result = 0
for part in parts:
    workflow = 'in'
    while workflow != 'A' and workflow != 'R':
        print(f'{part} going to {workflow}')
        workflow = apply_workflow(workflow, part)
    print(f'\t{part} was {workflow}')
    if workflow == 'A':
        result += sum(part.values())


print(f'result: {result}')