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

throw_location = list([Symbol(s, INT) for s in "abc"])
throw_velocity = list([Symbol(s, INT) for s in "def"])

constraints = []
domain = []
for coord, velocity in stones:
    t = Symbol(f't{len(domain)}', INT)
    domain.append(GE(t, Int(1)))
    for i in range(3):
        # coord[0] + velocity[0]*time = throw_location[0] + throw_velocity[0]*time
        lhs = coord[i] + velocity[i]*t
        rhs = Plus(throw_location[i], Times(throw_velocity[i], t))
        constraints.append(Equals(lhs, rhs))

formula = And(And(domain), And(constraints))
print(formula)

model = get_model(formula)
if model:
  print(model)
  print(f"a+b+c: {model.get_value(throw_location[0]).constant_value()+model.get_value(throw_location[1]).constant_value()+model.get_value(throw_location[2]).constant_value()}")
else:
  print("No solution found")

print(f'Took {time.time() - start_time} seconds')
