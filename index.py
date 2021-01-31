import numpy as np
import math as math

import random

from plasmid import *
from genetic import *
from fitness import *

if __name__ == "__main__":


    # Genetic algorithm parameters

    number_population = 100
    number_parents = 25
    number_generations = 1

    # Plus le nombre est grand, plus les mutations sont proches de l'original
    # Un nombre trop petit apporte par contre trop de divergence entre l'original et le muté
    mutation_dispersion = 1000

    #numbre de repliment ajouté à la fin de la chaîne ADN pour avoir une meilleure estimation avec la fonction fitness
    number_repliment = 100

    #paramete intra Genetic :
    #Choisir entre "elitist", "tournoi" et "fulltournoi"
    selection_mode = "tournoi"

    #Choisir entre : "normal", "unitform", "uniform bias" et "gaussian"
    crossover_mode = "normal"  

    #Correspond au nombre d'enfant par méthode de crossover (par nombre de parent)
    crossover_data = [1,1,1,1] 
    # [1] -> seulement 2 parents
    # [1,1,1] -> 2, 3 et 4 parents équirepartis
    # [3,0,1] -> 25% 4 parents 75% 2 parents

    
    plasmid = Plasmid("plasmid", number_repli=number_repliment)
    plasmid.load("./resources/plasmid_8k.fasta")

    mutation_table = data_for_mutation(RotTable(), mutation_dispersion)
    average_sample = plasmid.encodage()
    sample_size = len(average_sample)



    #Creation de la population initial
    best = [35.69138, 6.41456, 32.73365, -4.81166, 29.7054, 9.5206, 29.95633, 2.43291, 34.32917, 70.16257, 33.76503, -1.90312, 29.85794, 8.87855, 37.24665, -0.17051, 41.61833, 5.9078, 34.71625, -0.70015]

    initial_population = []
    for i in range(number_population):
        sample = []
        for j in range(sample_size):
            rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
            sample.append(round(average_sample[j]+rand,9))
        initial_population.append(sample)

    data = {
        "selection_mode" : selection_mode, 
        "crossover_mode" : crossover_mode,
        "mutation_table" : mutation_table,
        "fitness_data" : [Traj3D(), plasmid.sequence, plasmid.number_repli],
        "crossover_data" : crossover_data
        }
    

    genetic_algorithm = Genetic(number_parents, number_generations, initial_population, fitness_for_plasmid, data=data)
    genetic_algorithm.launch()
    genetic_algorithm.print()
    # genetic_algorithm.log("ga_save")

    plasmid.setRotationTable(Plasmid.decodage(genetic_algorithm.evolution_trace[-1][0]))
    plasmid.compute()
    plasmid.draw()

    # Genetic.plot_all()