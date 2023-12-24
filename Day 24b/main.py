import time
from pysmt.shortcuts import Symbol, GE, Plus, Times, Equals, And, Int, get_model
from pysmt.typing import INT

start_time = time.time()
file_path = 'input.txt'

with open(file_path, 'r') as file:
    stones = []
    for line in file:
        line = line.strip()
        coord, velocity = line.split('@')
        coord = list([int(i) for i in coord.split(',')])
        velocity = list([int(i) for i in velocity.split(',')])
        stones.append((coord, velocity))

t = Symbol('t', INT)
throw_location = list([Symbol(s, INT) for s in "abc"])
throw_velocity = list([Symbol(s, INT) for s in "def"])

coords_at_time = list([Plus(throw_location[i], Times(throw_velocity[i], t)) for i in range(3)])

constraints = []
for coord, velocity in stones:
    for i in range(3):
        lhs = coord[i] + velocity[i]*t
        constraints.append(Equals(lhs, coords_at_time[i]))
    # coord[0] + velocity[0]*time = throw_location[0] + throw_velocity[0]*time

domain = GE(t, Int(0))
formula = And(constraints)
print(formula)

model = get_model(formula)
if model:
  print(model)
else:
  print("No solution found")

print(f'Took {time.time() - start_time} seconds')
