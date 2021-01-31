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
    best = [35.69138, 6.41456, 32.73365, -4.81166, 29.7054, 9.5206, 29.95633, 2.43291, 34.32917, 70.16257, 33.76503, -1.90312, 29.85794, 8.87855, 37.24665, -0.17051, 41.61833, 5.9078, 34.71625, -0.70015]

    # best = [35.6082,  7.40623, 34.87048, -0.35868, 28.19604,  7.84619, 31.447,
    #         2.55371,  34.3969,  11.17229, 33.65879, 1.50384, 30.22278,  7.24414,
    #         37.08255, 3.52021, 40.39011,  4.79746, 36.2369,   0.79884]

#     best = [35.66005,  7.12851, 32.50664,  3.22198, 26.43402, 11.99214, 30.01582,
#       2.75054,
#  36.03844, 65.92154, 33.62013, -0.1638,  30.55007,  7.02352, 38.11358, -5.87874,
#  40.66411,  5.32515, 34.28866, -1.27557]

#     best = [35.65971,  7.14187, 32.52023,  3.66162, 26.41211, 12.02372, 30.03467,
#    2.84766,
#  36.0475,  66.14299, 33.61835, -0.1471 , 30.55315 , 7.04398, 38.10897, -5.9284,
#  40.59823,  5.26535, 34.25751, -1.36465]

#     best = [35.66014,  7.12536 ,32.52884 , 3.80588 ,26.38461, 12.06161, 30.01574,
#       2.83204,
#  36.0387 , 66.24149, 33.61997, -0.14671, 30.55945,  7.00146, 38.06833, -5.97425,
#  40.55165,  5.21129, 34.2458,  -1.40511]


#     [35.65798  7.10825 32.48623  3.63843 26.43215 12.13824 30.01666  2.82094
#  36.04131 66.31438 33.62137 -0.245   30.60268  6.94842 38.03826 -6.02887
#  40.56469  5.18218 34.25775 -1.33656]

    best = [35.69082,  6.40527, 32.73024, -4.81154, 29.69277,  9.53337, 29.95384,  2.43124,
 34.33251, 70.13121, 33.76634, -1.86582, 29.85654,  8.88096, 37.24316, -0.17171,
 41.67329,  5.92123, 34.71164, -0.69246]

    best = [35.69110054 , 6.39949137, 32.72914697, -4.81738299 ,29.7162775,   9.56188979,
 29.9534456,   2.43769609, 34.33701906 ,70.14562442, 33.76588115, -1.87109478,
 29.85492141 , 8.8883577,  37.24703549, -0.17266251, 41.67593791,  5.92216544,
 34.69793073, -0.68207309]

    initial_population = []#best] #* number_population
    for i in range(number_population):
        sample = []
        for j in range(sample_size):
            rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
            sample.append(round(average_sample[j]+rand/40,9))
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

    Genetic.plot_all()