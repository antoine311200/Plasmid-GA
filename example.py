import numpy as np

from functools import reduce
from genetic import *

target = [1,2,3,4,5,6,7,8,9,10]

def fitness(individual):
    n = len(target)
    error = 0
    for i in range(n):
        error += (individual[i]-target[i])**2
    return error/n

if __name__ == '__main__':

    data = { "mutation_table" : [['uniform', -0.05, 0.05] for i in range(10)] }

    number_population = 50
    number_parents = 10
    number_generation = 250

    initial_population = np.random.uniform(0,20,(number_population,10))

    genetic_algorithm = Genetic(
        number_parents,
        number_generation,
        initial_population, 
        fitness, data
    )
    genetic_algorithm.launch()
    genetic_algorithm.print()

