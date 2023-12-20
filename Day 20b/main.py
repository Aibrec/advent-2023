import re
import copy
import queue
import math
from collections import deque

file_path = 'input.txt'
workflow_pattern = r'\b(\w+)\{(.*?)\}'

# High is True
# Low is False
LOW = False
HIGH = True

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
            type = 'broadcaster'
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
            modules[destination]['state'][module_name] = LOW

def apply_pulse(source_module_name, pulse, destination_module_name):
    module = modules[destination_module_name]
    next_pulse = None

    if module['type'] == '%':
        if pulse == LOW:
            module['state'] = not module['state']
            next_pulse = module['state']
    elif module['type'] == '&':
        module['state'][source_module_name] = pulse
        if pulse == LOW:
            # Just got a low, can't be all high, so there's at least one low and we send a High
            next_pulse = HIGH
        else:
            next_pulse = not all([last for last in module['state'].values()])
    elif module['type'] == 'output':
        module['last_received'] = next_pulse
    elif module['type'] == 'broadcaster':
        next_pulse = pulse
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

def print_module_state(num_presses):
    overall_state = ""
    for module_name, module in modules.items():
        local_state = ""
        if module['type'] == 'broadcaster':
            pass
        elif module['type'] == '%':
            if module['state']:
                local_state = "1"
            else:
                local_state = "0"
        elif module['type'] == '&':
            stable_list = sorted(module['state'].keys())
            for module_name in stable_list:
                if module['state'][module_name] == 'high':
                    local_state += "1"
                else:
                    local_state += "0"
        overall_state += local_state

    number_of_true = overall_state.count('1')
    print(f'{num_presses}: {overall_state} : {number_of_true} : len {len(overall_state)}')


def map_graph():
    for module_name in sorted(modules.keys()):
        type = modules[module_name]['type']
        if len(type) != 1:
            type = ""
        else:
            type = f"\\{type}"

        for target in sorted(modules[module_name]['destinations']):
            target_type = modules[target]['type']
            if len(target_type) != 1:
                target_type = ""
            else:
                target_type = f"\\{target_type}"
            print(f'\t"{type}{module_name}" -> "{target_type}{target}"')
    print("")

button_presses = 0
seen_polarities = {}
seen_sends = {}
for module in modules.keys():
    seen_sends[module] = {
        'calls': 0,
        'high': [],
        'low': [],
        'none': []
    }

num_pulses = {
    HIGH: 0,
    LOW: 0,
}

map_graph()

# Found these 4 by looking at the graph generated above
monitoring = set(['xd', 'vr', 'pf', 'ts'])
seen_sends_low = {}
for module in monitoring:
    seen_sends_low[module] = []

while True:
#for i in range(1000):
    #print_module_state(button_presses)
    button_presses += 1
    pulses = deque([('start', LOW, 'broadcaster')], 100)
    #pulses = [('start', LOW, 'broadcaster')]
    polarities = ""
    while pulses:
        pulse = pulses.popleft()
        #pulse = pulses.pop(0)
        num_pulses[pulse[1]] += 1
        if pulse[2] == 'rx' and pulse[1] == LOW:
            print(f'Sent low to rx after {button_presses} button presses')
            exit(1)

        # elif pulse[2] == 'rx':
        #     print(f"Sent '{pulse[1]}' to rx after {button_presses} button presses")
        #     print(f"State of dt {modules['dt']['state']}")
        #     print("")
        new_pulses = apply_pulse(*pulse)
        if pulse[2] in monitoring and new_pulses and new_pulses[0][1] == LOW:
            seen_sends_low[pulse[2]].append(button_presses)
            print(f"Saw low for {pulse[2]}")
            if all(seen_presses for seen_presses in seen_sends_low.values()):
                print(f"Seen a low for all 4! Lcm is {math.lcm(*[seen_presses[0] for seen_presses in seen_sends_low.values()])}")
                exit(1)


        #seen_sends[pulse[2]]['calls'] += 1
        # if new_pulses:
        #     seen_sends[pulse[2]][new_pulses[0][1]].append(seen_sends[pulse[2]]['calls'])
        # else:
        #     seen_sends[pulse[2]]['none'].append(seen_sends[pulse[2]]['calls'])
        # if new_pulses:
        #     polarity = "1" if new_pulses[0][1] == "high" else "0"
        #     #print(f"{pulse} caused {polarity} : {new_pulses}")
        #     polarities += polarity
        # else:
        #     print(f"{pulse} caused - {new_pulses}")
        pulses.extend(new_pulses)

    if button_presses % 100000 == 0:
        print(f'Done press {button_presses}')

    # if polarities in seen_polarities:
    #     seen_polarities[polarities].append(button_presses)
    # else:
    #     seen_polarities[polarities] = [button_presses]
    #     print(f"New polarities {button_presses}: {polarities}")
    #     polarity = 'just here to debug'

print(f"Done after {num_pulses}, {num_pulses[LOW] * num_pulses[HIGH]}")


