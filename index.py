import numpy as np
import math as math

import random

from plasmid import *
from genetic import *

if __name__ == "__main__":

    # plasmid = Plasmid("awesome plasmid", number_repli=50)
    # plasmid.load("./resources/plasmid_8k.fasta")

    # Genetic algorithm parameters

    number_population = 50
    number_parents = 20
    number_generations = 500

    # Plus le nombre est grand, plus les mutations sont proches de l'original
    # Un nombre trop petit apporte par contre trop de divergence entre l'original et le muté
    mutation_dispersion = 2000

    # nombre de repliment ajouté à la fin de la chaîne ADN pour avoir une meilleure estimation avec la fonction fitness
    number_repliment = 50

    #paramete intra Genetic :
    #Choisir entre "elitist", "tournoi" et "fulltournoi"
    selection_mode = "tournoi"

    #Seul normal est disponible
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
    initial_population = []
    for i in range(number_population):
        sample = []
        for j in range(sample_size):
            origin = mutation_table[j][2]
            sigma = mutation_table[j][1]
            # while True:
            mute_rate = random.uniform(-sigma, sigma)#max(origin-sigma, min(origin+sigma, random.gauss(mu=self.current_offspring[i][j], sigma=sigma)))
                # if average_sample[j]+mute_rate >= origin-sigma and average_sample[j]+mute_rate <= origin+sigma:
            sample.append(round(average_sample[j]+mute_rate,5))
                    # break
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

    plasmid.setRotationTable(Plasmid.decodage(genetic_algorithm.evolution_trace[-1][0]))
    plasmid.compute()
    plasmid.draw()