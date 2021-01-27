import numpy as np
import math as math

import random

from RotTable import *
from Traj3D import *
from encodage import *
from plasmid import *

class Genetic:

    def __init__(self, number_parents, max_generation, population, fitness_function, data = {"selection_mode" : "elitist", "crossover_mode" : "normal", "mutation_table" : None, "fitness_data" : None}):
        self.data = data
        self.number_parents = number_parents
        self.max_generation = max_generation
        self.initial_population = population
        
        self.mutation_table = data['mutation_table']
        self.fitness_data = data['fitness_data']
        self.has_fitness_data = (data['fitness_data'] != None)
        self.selection_mode = data['selection_mode']
        self.crossover_mode = data['crossover_mode']
        self.fitness_function = fitness_function

        self.sx_weights= data["crossover_data"]


        self.current_generation = 0
        self.population_size = self.initial_population.shape
        self.offspring_size = (self.population_size[0]-self.number_parents, self.population_size[1])

        self.history_population_enable = True
        self.history_parents_enable = True


        self.population_history = []
        self.parents_history = []
        self.current_parents = []
        self.current_population = self.initial_population
        self.current_offspring = []
        self.evolution_trace = []


    def fitness(self, individual):
        if(self.has_fitness_data):
            return self.fitness_function(individual, self.fitness_data)
        else :
            return self.fitness_function(individual)
    
    # elitist selection 
    # roulette selection : p_i = f_i / sum f_j (sur-representativity !!!)
    # rang selection : sort -> index = proportion (smoothing) (convergence time !!!)
    # tournament selection : 2 random -> best score (+ probabilty of win) => diversity
    
    def select(self):
        self.current_parents = np.empty((self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))

        L_indice = np.argsort(fitness_list)
        for i in range(self.number_parents):
            self.current_parents[i] = self.current_population[L_indice[i]]
        
        self.evolution_trace.append([self.current_population[L_indice[0]], fitness_list[L_indice[0]]])
        #self.current_parents = sorted(fitness_list)[:self.number_parents]
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)

    
    def repro(self, Parents, d): # d = nombre de parents
        child = Parents[0].copy() 
        nb_chrmsm = self.offspring_size[1]//d # nb_chrmsm : nombre de gènes transmis par chaque parent à l'enfant
        for i in range(1, d-1):
            child[i*nb_chrmsm:(i+1)*nb_chrmsm] = Parents[i][i*nb_chrmsm:(i+1)*nb_chrmsm].copy() 
        # pour ne pas avoir d'erreur, on complète avec le bon nombre de gènes (provenant du dernier parent)
        child[(d-1)*nb_chrmsm:] = Parents[-1][(d-1)*nb_chrmsm:].copy()
        return child


    def crossover(self):
    
        nb_voulu = self.offspring_size[0]
        Parents = self.current_parents

        for _ in range(nb_voulu//sum(self.sx_weights)):
            # On va créer en boucle sum(self.sx_weights) enfants, jusqu'à en avoir le nombre voulu.
            # L'intérêt est qu'à chaque itération, le nombre d'enfants créés pour chaque méthode 
            # de reproduction (une méthode est caractérisée par un nombre de parents) est donné
            # par le poids de la méthode, indiqué dans le tableau self.sx_weights.
            

            for d in range(2, len(self.sx_weights)+2): # d = nbr of parents pour créer un enfant
                poids = self.sx_weights[d-2] # poids = nombre de fois où on va appliquer la méthode

                for _ in range(poids):
                    rd_parents = [random.choice(Parents) for _ in range(d)] # choix de d parents aléatoires
                    child = self.repro(rd_parents, d) 
                    self.current_offspring.append(child)

    def mutate(self):
        print("mutate", end= '  ')
        #print(self.current_offspring)
        if self.mutation_table != None:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    random_method = self.mutation_table[j][0]

                    if random_method == 'gauss':
                        while True:
                            mute_rate = random.gauss(mu=self.mutation_table[j][1], sigma=self.mutation_table[j][2])
                            #print(mute_rate, self.current_offspring[i][j])
                            self.current_offspring[i][j] += mute_rate
                            break
                    elif random_method == 'uniform':
                        # while True:
                        a,b = self.mutation_table[j][1], self.mutation_table[j][2]
                        origin = self.mutation_table[j][3]
                        mute_rate = random.uniform(a, b)
                        # print(mute_rate, self.current_offspring[i][j])
                        if self.current_offspring[i][j]+mute_rate <= origin+b and self.current_offspring[i][j]+mute_rate >= origin+a:
                            self.current_offspring[i][j] += mute_rate
                    elif random_method == 'gauss bounded':
                        origin = self.mutation_table[j][2]
                        sigma = self.mutation_table[j][1]
                        
                        while True:
                            mute_rate = random.gauss(mu=self.current_offspring[i][j], sigma=sigma/10)#max(origin-sigma, min(origin+sigma, random.gauss(mu=self.current_offspring[i][j], sigma=sigma)))
                            # print(self.current_offspring[i][j], mute_rate, origin-sigma, origin+sigma)
                            if mute_rate >= origin-sigma and mute_rate <= origin+sigma:
                                self.current_offspring[i][j] = mute_rate
                                break
                        # if mute_rate == origin-sigma:


                    elif random_method == 'triangular':
                        mute_rate = random.triangular(low=self.mutation_table[j][1], high=self.mutation_table[j][2], mode=self.mutation_table[j][3])
                    elif random_method == 'randint':
                        while True:
                            mute_rate = random.randint(a=self.mutation_table[j][1], b=self.mutation_table[j][2])
                            self.current_offspring[i][j] += mute_rate
                            break
                    # elif random_method == 'choice':
                    #     while True:
                    #         mute_rate = random.choice(list=self.mutation_table[j][1])
                    #         self.current_offspring[i][j] += mute_rate
                    #         break
                    else:
                        mute_rate = 0.02
                        self.current_offspring[i][j] += mute_rate
                    
                    self.current_offspring[i][j] = round(self.current_offspring[i][j], 5)

        else:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    self.current_offspring[i][j] += np.random.randint(self.mutation_table[j].min, self.mutation_table[j].max)
        
        self.current_population = np.concatenate((self.current_parents,self.current_offspring), axis=0)
    
    def bestfit(self):
        return round(self.evolution_trace[-1][1],4)
        
    def clear(self):
        self.current_offspring = []
        self.current_parents = []

    def launch(self):
        for _ in range(self.max_generation):
            print("Next generation", end=' ')
            self.current_generation += 1
            self.select()
            self.crossover()
            self.mutate()
            #print(self.current_population)
            print(self.bestfit())
            self.clear()

    def print(self):
        for i in range(len(self.evolution_trace)):
            print("Generation "+str(i+1)+" (best) : ", self.evolution_trace[i][0], " (error : ", str(round(self.evolution_trace[i][1],4))+")")


list = [[1,2,3],[[1,2,3],[4,[4,3],3,2]]]


lineList = [line.rstrip('\n') for line in open("./resources/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])

mutation_table= dataForMutation(RotTable())
indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]

pop_nb = 30


population = []
for i in range(pop_nb):
    sample = []
    for j in range(len(mutation_table)):
        rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])

        sample.append(round(indiv[j]+rand,5))
    population.append(sample)
population = np.array(population)

def fitness_indiv(indiv, data):
    return Plasmid("", Plasmid.decodage(indiv), data[0], data[1]).getDistance()

# def fitness_indiv(indiv, data):
#     data[0].compute(data[1], decodage(indiv))
#     lastVect = data[0].getLastFromTraj()
#     return(math.sqrt(lastVect.dot(lastVect)))

data = {"selection_mode" : "elitist", "crossover_mode" : "normal",\
    "mutation_table" : dataForMutation(RotTable()), "fitness_data" : [Traj3D(), seq], "crossover_data" : [5, 2, 1, 1, 1]}



print(fitness_indiv(indiv, [Traj3D(), seq]))

if __name__ == "__main__":

    gen = Genetic(pop_nb//3,30,population, fitness_indiv, data=data)
    gen.launch()
    gen.print()

    plasmid = Plasmid("", Plasmid.decodage(gen.evolution_trace[-1][0]), sequence=seq)
    plasmid.compute()
    plasmid.draw()