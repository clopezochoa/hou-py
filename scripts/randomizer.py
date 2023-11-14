import hou
from random import choice

def fix_repeated_values(node, mode, max_value):
  geo = node.geometry()
  if mode == 0:
      geo = geo.prims()
  else:
      geo = geo.points()
  unique_seeds = []
  duplicated_seeds = []
  for elem in geo:
      seed_val = elem.attribValue("seed")
      if seed_val in unique_seeds:
          duplicated_seeds.append((elem, seed_val))
      else:
          unique_seeds.append(seed_val)
      
  if len(duplicated_seeds) > 0:
      missing_numbers = list(set(range(0, max_value + 1)) - set(unique_seeds))
      for seed_obj in duplicated_seeds:
          candidate = choice(missing_numbers)
          seed_obj[0].setAttribValue('seed', float(candidate))
          missing_numbers.remove(candidate)
