import numpy as np

from genetic import *

def fitness(X):
    return ((X[0]-10)**2+(X[1]+5)**2)/2


if __name__ == "__main__":


    # Genetic algorithm parameters

    number_population = 100
    number_parents = 20
    number_generations = 1000

    # Plus le nombre est grand, plus les mutations sont proches de l'original
    # Un nombre trop petit apporte par contre trop de divergence entre l'original et le muté
    mutation_dispersion = 10

    #paramete intra Genetic :
    #Choisir entre "elitist", "tournoi" et "fulltournoi"
    selection_mode = "tournoi"

    #Seul normal est disponible
    crossover_mode = "normal"  
    crossover_data = [1]

    mutation_table = [
        ['uniform bounded', -1/mutation_dispersion, 1/mutation_dispersion, -500, 500],
        ['uniform bounded', -1/mutation_dispersion, 1/mutation_dispersion, 0, -500, 500],
    ]
    """[["gauss bounded", 50, 0, mutation_dispersion],
                    ["gauss bounded", 50, 0, mutation_dispersion]]"""
    
    average_sample = [0,0]
    sample_size = len(average_sample)



    #Creation de la population initial
    initial_population = list(np.random.uniform(-500,500,(number_population-1,2)))
    # initial_population.append([10,-5])
    print(initial_population)
    # for i in range(number_population):
    #     sample = []
    #     for j in range(sample_size):
    #         rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
    #         sample.append(round(average_sample[j]+rand,5))
    #     initial_population.append(sample)

    data = {
        "selection_mode" : selection_mode, 
        "crossover_mode" : crossover_mode,
        "mutation_table" : mutation_table,
        "fitness_data" : None,
        "crossover_data" : crossover_data
        }
    

    genetic_algorithm = Genetic(number_parents, number_generations, initial_population, fitness, data=data)
    genetic_algorithm.launch()
    genetic_algorithm.print()