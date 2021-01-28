import numpy as np

from genetic import *

def fitness(X):
    return (np.abs(X[0]-10))**(1/10)+((X[1]+5)**2)**(1/10)


if __name__ == "__main__":


    # Genetic algorithm parameters

    number_population = 100
    number_parents = 20
    number_generations = 100

    # Plus le nombre est grand, plus les mutations sont proches de l'original
    # Un nombre trop petit apporte par contre trop de divergence entre l'original et le muté
    mutation_dispersion = 100

    #paramete intra Genetic :
    #Choisir entre "elitist", "tournoi" et "fulltournoi"
    selection_mode = "tournoi"

    #Seul normal est disponible
    crossover_mode = "normal"  
    crossover_data = [1]

    mutation_table = [["gauss bounded", 50, 0, mutation_dispersion],\
                       ["gauss bounded", 50, 0, mutation_dispersion]]
    
    average_sample = [0,0]
    sample_size = len(average_sample)



    #Creation de la population initial
    initial_population = []
    for i in range(number_population):
        sample = []
        for j in range(sample_size):
            rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
            sample.append(round(average_sample[j]+rand,5))
        initial_population.append(sample)

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