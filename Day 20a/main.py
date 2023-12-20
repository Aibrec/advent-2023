import re
import copy

file_path = 'input.txt'
workflow_pattern = r'\b(\w+)\{(.*?)\}'

with open(file_path, 'r') as file:
    modules = {}
    for line in file:
        line = line.strip()
        name, destinations = line.split(' -> ')
        destinations = destinations.split(', ')

        if name[0] == '%':
            type = name[0]
            state = False  # False is off, True is on
            name = name[1:]
        elif name[0] == '&':
            type = name[0]
            state = {}
            name = name[1:]
        else:
            type = None
            state = None

        modules[name] = {
            'inputs': [],
            'destinations': destinations,
            'type': type,
            'state': state,
        }

for module_name, module in list(modules.items()):
    for destination in module['destinations']:
        if destination not in modules:
            modules[destination] = {
                'type': 'output',
                'inputs': [],
                'destinations': [],
                'last_received': None,
            }
        modules[destination]['inputs'].append(module_name)
        if modules[destination]['type'] == '&':
            modules[destination]['state'][module_name] = 'low'

def apply_pulse(source_module_name, pulse, destination_module_name):
    module = modules[destination_module_name]
    next_pulse = None
    if module['type'] is None:
        next_pulse = pulse
    elif module['type'] == '%':
        if pulse == 'low':
            module['state'] = not module['state']
            next_pulse = 'high' if module['state'] else 'low'
    elif module['type'] == '&':
        module['state'][source_module_name] = pulse
        if all([last == 'high' for last in module['state'].values()]):
            next_pulse = 'low'
        else:
            next_pulse = 'high'
    elif module['type'] == 'output':
        module['last_received'] = next_pulse
    else:
        raise TypeError('Unknown module type')

    if next_pulse is None:
        return []
    else:
        return list([(destination_module_name, next_pulse, next_destination_name) for next_destination_name in module['destinations']])


num_pulses = {
    'high': 0,
    'low': 0,
}
for i in range(1000):
    pulses = [('start', 'low', 'broadcaster')]
    while pulses:
        pulse = pulses.pop(0)
        num_pulses[pulse[1]] += 1
        new_pulses = apply_pulse(*pulse)
        #print(f"{pulse} caused {new_pulses}")
        pulses.extend(new_pulses)

print(f"Done after {num_pulses}, {num_pulses['low'] * num_pulses['high']}")


