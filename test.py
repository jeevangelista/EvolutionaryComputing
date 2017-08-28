from EvoComp import GeneticAlgorithm as GA
import numpy as np

def fitness_function(chromosome):
	return np.sum(chromosome)


a = GA.GeneticAlgorithm(fitness_function)
pop = a.initialize_population(5,5, 2)
#parents = a.tournament(pop, 6, 2, maximum=False)
#print(parents)
#offsprings = a.crossover(parents,4)
#print(offsprings)
chromosome = pop[0]
print(chromosome)
c = a.mutation(chromosome, 2, 1.0)
print(c)