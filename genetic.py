import numpy as np
import math as math
from random import *

class Genetic:

    def __init__(self, number_parents, max_generation, population, *data):
        self.data = data
        self.number_parents = number_parents
        self.max_generation = max_generation
        self.initial_population = population

        self.current_generation = 0
        self.population_size = self.initial_population.shape
        self.offspring_size = (self.population_size[0]-self.number_parents, self.population_size[1])

        self.history_population_enable = True
        self.history_parents_enable = True

        self.fitness = self.fitness_basic

        self.population_history = []
        self.parents_history = []
        self.current_parents = []
        self.current_population = self.initial_population
        self.current_offspring = []
        self.evolution_trace = []


        self.sx_weights = [1, 1, 1, 1, 1] # Pondération des différents modes de reproduction
    

    def fitness_basic(self, cpl, dpl): 
        apl = zip(cpl, dpl)
        cps = len(cpl)
        value = 0
        for cv in apl:
            value += (cv[1]-cv[0])**2
        return math.sqrt(value)/cps

    def fitness(self, fitness_function):
        self.fitness = fitness_function
    
    
    # elitist selection 
    # roulette selection : p_i = f_i / sum f_j (sur-representativity !!!)
    # rang selection : sort -> index = proportion (smoothing) (convergence time !!!)
    # tournament selection : 2 random -> best score (+ probabilty of win) => diversity
    
    def select(self):
        self.current_parents = np.empty((self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness_basic(self.current_population[i], value))
        # print(fitness_list)
        self.sorted_idx = np.argsort(fitness_list)
        # print(self.sorted_idx)
        for i in range(self.number_parents):
            self.current_parents[i] = self.current_population[self.sorted_idx[i]]
        self.evolution_trace.append([self.current_population[self.sorted_idx[0]], fitness_list[self.sorted_idx[0]]])
        #self.current_parents = sorted(fitness_list)[:self.number_parents]
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)
        # print(self.current_parents)

    def repro(self, Parents, d): # d = nombre de parents
        child = Parents[0].copy() 
        nb_chrmsm = self.offspring_size[1]//d # nb_chrmsm : nombre de gènes transmis par chaque parent à l'enfant
        for i in range(1, d-1):
            child[i*nb_chrmsm:(i+1)*nb_chrmsm] = Parents[i][i*nb_chrmsm:(i+1)*nb_chrmsm].copy() 
        # on complète avec le bon nombre de gènes, provenant du dernier parent
        child[(d-1)*nb_chrmsm:] = Parents[-1][(d-1)*nb_chrmsm:].copy()
        return child



    def crossover(self): # crée la prochaine génération

        nb_voulu = self.offspring_size[0]
        Parents = self.current_parents

        while len(self.current_offspring) < nb_voulu :

            for d in range(2, len(self.sx_weights)+2): # d = nbr de parents pour créer un seul enfant
                poids = self.sx_weights[d-2] # poids = nombre de fois où l'on va 

                for _ in range(poids): # 
                    if len(self.current_offspring) >= nb_voulu :
                        return
                    rd_parents = [choice(Parents) for _ in range(d)] # choix de d parents aléatoires
                    child = self.repro(rd_parents, d) # création de l'enfant
                    self.current_offspring.append(child)

     
  

    def mutate(self):
        for i in range(self.offspring_size[0]):
            for j in range(self.offspring_size[1]):
                self.current_offspring[i][j] += np.random.randint(-2,2)
        print(self.current_offspring)
        self.current_population = np.concatenate((self.current_parents,self.current_offspring), axis=0)

    def bestfit(self):
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness_basic(self.current_population[i], value))
        self.sorted_idx = np.argsort(fitness_list)
        return self.current_population[self.sorted_idx[0]]
        
    def clear(self):
        self.current_offspring = []
        self.current_parents = []

    def launch(self):
        for i in range(self.max_generation):
            print("Next generation")
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

value = [21, 8, 4, 24]
pop = np.random.randint(low=0, high=15, size=(30,4))
gen = Genetic(5, 30, pop+15)
print(pop)
gen.launch()
gen.print()
#print(np.array(gen.evolution_trace))
# Add a pattern system

list = [[1,2,3],[[1,2,3],[4,[4,3],3,2]]]



#print(list)
