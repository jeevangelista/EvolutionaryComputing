from EvoComp import GeneticAlgorithm as GA
from EvoComp import ARO
import numpy as np

def fitness_function(chromosome):
	return np.sum(chromosome)
def crossover():
	print("cross")

a = GA.GeneticAlgorithm(fitness_function)
pop = a.initialize_population(5,5, 2)
# parents = a.tournament(pop, 3, 2, maximum=False)
# print(parents)
# offsprings = a.crossover(parents,4)
# print(offsprings)
# chromosome = pop[0]
# print(chromosome)
# c = a.mutation(chromosome, 2, 1.0)
# print(c)
# elite= a.get_elite(pop)
# print(elite)
# print(a.fitness_function(elite))
b = ARO.ARO(a, pop[0], 2, 2)
print ("final")
print(b)