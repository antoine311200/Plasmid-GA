import numpy as np
import math as math

import random

from plasmid import *
from genetic import *


def fitness_indiv(indiv, data):
    return Plasmid("", Plasmid.decodage(indiv), data[0], data[1]).getDistance()


def dataForMutation(rot_tab, mutation_variance):
    mut_table = []
    for dinucleotide in Plasmid.important_dinucleotides :
        mut_table += [["gauss bounded", rot_tab.getTwistVariance(dinucleotide), rot_tab.getTwist(dinucleotide), mutation_variance],\
                       ["gauss bounded", rot_tab.getWedgeVariance(dinucleotide), rot_tab.getWedge(dinucleotide), mutation_variance]]
    return mut_table

if __name__ == "__main__":

    plasmid = Plasmid("awesome plasmid")
    plasmid.load("./resources/plasmid_8k.fasta")

    # Genetic algorithm parameters

    number_population = 30
    number_parents = 7
    number_generations = 10
    mutation_variance = 100


    mutation_table = dataForMutation(RotTable(), mutation_variance)
    sample_size = len(mutation_table)
    average_sample = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]

    initial_population = []

    for i in range(number_population):
        sample = []
        for j in range(sample_size):
            rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
            sample.append(round(average_sample[j]+rand,5))
        initial_population.append(sample)



    data = {
        "selection_mode" : "elitist",
        "crossover_mode" : "normal",
        "mutation_table" : mutation_table,
        "fitness_data" : [Traj3D(), plasmid.sequence],
        "crossover_data" : [5, 2, 1, 1, 1]
    }

    genetic_algorithm = Genetic(number_parents, number_generations, initial_population, fitness_indiv, data=data)
    genetic_algorithm.launch()
    genetic_algorithm.print()

    plasmid.setRotationTable(Plasmid.decodage(genetic_algorithm.evolution_trace[-1][0]))
    plasmid.compute()
    plasmid.draw()