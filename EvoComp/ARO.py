import numpy as np

MUTTYPE = 2
# GA: GeneticAlgorithm object
# parent: parent to reproduce
def ARO(GA, parent, iteration, low, high=None, maximum=False, *args, **kwargs):
  dtype = type(low)
  parent_len = len(parent)
  for i in range(iteration):
    if not high:
      high = low
      low = 0
    if high < low:
      raise ValueError("high < low")
    if dtype not in (int, float):
      raise ValueError("Wrong Datatype")

    parent_fitness = GA.fitness_function(parent, *args, **kwargs)

    larva = GA.mutation(parent, MUTTYPE, low, high)

    parents = np.asarray((parent,larva))
    bud = GA.crossover(parents, 3)
    bud_fitness1 = GA.fitness_function(bud[0], *args, **kwargs)
    bud_fitness2 = GA.fitness_function(bud[1], *args, **kwargs)
    # Get offspring with better fitness
    if maximum:
      bud = bud[0] if bud_fitness1 > bud_fitness2 else bud[1]
      bud_fitness = bud_fitness1 if bud_fitness1 > bud_fitness2 else bud_fitness2
    else:
      bud = bud[0] if bud_fitness1 < bud_fitness2 else bud[1]
      bud_fitness = bud_fitness1 if bud_fitness1 < bud_fitness2 else bud_fitness2
    # Get best
    if maximum and bud_fitness > parent_fitness:
      parent = bud
    elif not maximum and bud_fitness < parent_fitness:
      parent = bud

  return parent