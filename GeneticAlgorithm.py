import numpy as np 


class GeneticAlgorithm:
  fitness_function = None
  CROSSTYPES = 4

	# low: lower bound of range unless high=None.
  # high: upper excluded bound of range.
  #       If high isnone, then low becomes upper bound
  #       and lower bound becomes 0
  # size: a number (or tuple). Size of chromosome
  # type of chromosome whether int or float is dependent on the value of the range
  # For now it only supports uniform distribution
  def initialize_population(self, length, popsize, low, high=None):
    dtype=type(low)
    population = np.zeros(shape=(popsize,length), dtype=dtype)
    if not high:
      high = low
      low = 0
    if high < low:
      raise ValueError("high < low")
    for i in range(popsize):
      if dtype == int:
        population[i] = np.random.randint(low=low, high=high, size=length)
      elif dtype == float:
        population[i] = np.random.uniform(low=low, high=high, size=length)
    return population


  # population: current population
  # tour_size: tournament size
  # top: top n scorer of the tournament to take
  # maximum: False if minimizing fitness, True if maximizing fitness
  # args and kwargs: additional fitness function parameters
  def tournament(self, population, tour_size, top, maximum=False, *args, **kwargs):
    # draw random mates from the population of size tour_size without replacement
    chrom_len = len(population[0])
    mates = np.random.choice(len(population), tour_size, replace=False)
    parents =  np.zeros(shape=(top,chrom_len),dtype=type(population[0][0]))
    mate_fitness = dict()
    # keys are mates and values are their respective fitness score
    for mate in mates:
      mate_fitness[mate] = fitness_function(population[mate], *args, **kwargs)
    # list of mates sorted by fitness
    mate_rank = sorted(mate_fitness, key=mate_fitness.__getitem__, reverse=maximum)
    for i in range(top):
      parents[i] = population[mate_rank[i]]
    return parents



  # parents: parent chromosomes
  # crosstype: currently supported subtypes
  # 1: single point
  # 2: two point
  # 3: uniform
  # 4: choose any of the 3 randomly   
  def crossover(self, parents, crosstype):
    if len(parents) > 2:
      raise ValueError("WTF is wrong with you? Can't have child with \
                        3 parents! Kidding, not yet supported :P")
    elif len(parents) == 2:
      chrom_len = len(parents[0])
      offsprings =  np.zeros(shape=(len(parents),chrom_len),dtype=type(parents[0][0]))
      if crosstype == self.CROSSTYPES:
        crosstype = np.random.randint(1,self.CROSSTYPES)
      if crosstype == 1:
        point = np.random.randint(1,chrom_len)
        print(point)
        offsprings[0] = parents[0]
        offsprings[0][point:] = parents[1][point:]
        offsprings[1] = parents[1]
        offsprings[1][point:] = parents[0][point:]
      elif crosstype == 2:
        points = np.random.choice(chrom_len, 2, replace=False)
        points.sort()
        print(points)
        offsprings[0] = parents[0]
        offsprings[0][points[0]:points[1]] = parents[1][points[0]:points[1]]
        offsprings[1] = parents[1]
        offsprings[1][points[0]:points[1]] = parents[0][points[0]:points[1]]
      elif crosstype == 3:
        crossrate = np.random.uniform(size=chrom_len)
        print(crossrate)
        offsprings[0] = parents[0]
        offsprings[0][crossrate>0.5] = parents[1][crossrate>0.5]
        offsprings[1] = parents[1]
        offsprings[1][crossrate>0.5] = parents[0][crossrate>0.5]
      else:
        raise ValueError("Invalid Crosstype!")
    return offsprings


  # chromosome: the chromosome to mutate
  #muttype: 1: simple pointwise mutation (SNP), 2: uniform mutation
  def mutation(self, chromosome, muttype, low, high=None):
    dtype = type(low)
    chrom_len = len(chromosome)
    
    if not high:
      high = low
      low = 0
    if high < low:
      raise ValueError("high < low")
    if dtype not in (int, float):
      raise ValueError("Wrong Datatype")

    if muttype == 1:
      snp_loc = np.random.randint(chrom_len)
      print(snp_loc)
      if dtype == int:
        if low == 0 and high == 2: # binary lang flip it
          chromosome[snp_loc] = 1 if chromosome[snp_loc] == 0 else 0
        else:
          snp_range = np.arange(low,high)
          # To ensure it is not the same as previous nucleotide
          snp = np.random.choice(snp_range, 2, replace=False)
          chromosome[snp_loc] = snp[0] if not snp[0] == chromosome[snp_loc] else snp[1]
      elif dtype == float:
        snp = np.random.uniform(low, high)
        # To ensure it is not the same as previous nucleotide
        while snp == chromosome[snp_loc]:
          snp = np.random.uniform(low, high)
        chromosome[snp_loc] = snp
    
    elif muttype == 2:
      mutrate = np.random.uniform(size=chrom_len)
      print(mutrate)
      mut_loc = chromosome[mutrate>0.5]
      mut_len = len(mut_loc)
      if dtype == int:
        if low == 0 and high == 2: # binary lang flip it
          for i in range(len(mut_loc)):
            mut_loc[i] = 1 if mut_loc[i]==0 else 0
          chromosome[mutrate>0.5] = mut_loc
        else:
          mutations = np.random.randint(low, high, size=mut_len)
          mut_range = np.arange(low,high)
          for i in range(mut_len):
            if mutations[i] == mut_loc[i]:
              mut = np.random.choice(mut_range, 2, replace=False) # para walang katulad
              mutations[i] = mut[0] if not mut[0] == mut_loc[i] else mut[1]
          chromosome[mutrate>0.5] = mutations
      elif dtype == float:
        mutations = np.random.uniform(low, high, size=mut_len)
        for i in range(mut_len):
          while mutations[i] == mut_loc[i]:
            mutations[i] = np.random.uniform(low, high)
        chromosome[mutrate>0.5] = mutations
    else:
      raise ValueError("Wrong mutation type")
    return chromosome


  def __init__(self, fitness_function, crossover=None, mutation=None):
    if fitness_function:
      self.fitness_function = fitness_function
    else:
      raise Exception("Enter Fitness Function")
    if crossover:
      self.crossover = crossover

    if mutation:
      self.mutation = mutation


def fitness_function(chromosome):
	return np.sum(chromosome)


a = GeneticAlgorithm(fitness_function)
pop = a.initialize_population(5,5, 1.0)
#parents = a.tournament(pop, 6, 2, maximum=False)
#print(parents)
#offsprings = a.crossover(parents,4)
#print(offsprings)
chromosome = pop[0]
print(chromosome)
c = a.mutation(chromosome, 2, 1.0)
print(c)