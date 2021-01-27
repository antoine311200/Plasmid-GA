import numpy as np
import math as math
import random

from math import *

from RotTable import *
from Traj3D import *

lineList = [line.rstrip('\n') for line in open("./resources/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])
# seq = 'AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG'

class Genetic:

    def __init__(self, number_parents, max_generation, population, data={'mutation_table':[]}):
        self.data = data
        self.number_parents = number_parents
        self.max_generation = max_generation
        self.initial_population = population
        self.mutation_table = data['mutation_table']

        self.current_generation = 0
        self.population_size = (len(self.initial_population), len(self.initial_population[0]))
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

    def fitness_basic(self, cpl): #dpl
        # apl = zip(cpl, dpl)
        # cps = len(cpl)
        # value = 0
        # for cv in apl:
        #     value += (cv[1]-cv[0])**2
        # return math.sqrt(value)/cps
        # print(cpl)
        plsm = Plasmid.encode(indiv)

        rot_table = RotTable(cpl)
        traj = Traj3D()
        traj.compute(seq, rot_table)
        dist = 0
        trajectory = traj.getTraj()
        for i in range(3):
            # print(trajectory[-1], trajectory[-1][0])
            dist += trajectory[-1][i]**2
        return sqrt(dist)

    def fitness(self, fitness_function):
        self.fitness = fitness_function

    # elitist selection 
    # roulette selection : p_i = f_i / sum f_j (sur-representativity !!!)
    # rang selection : sort -> index = proportion (smoothing) (convergence time !!!)
    # tournament selection : 2 random -> best score (+ probabilty of win) => diversity


    def select_tournoi(self):
        self.current_parents = np.empty((self.number_parents, self.population_size[1]))
        L_tier = []
        L_tier.append([[self.current_population[i],fitness(self.current_population[i])] for i in range(self.population_size[0])])
        
        #L_tier est la liste des placements, par ex L_tier[0] contient la liste des couples [individu_i,fitness(individu_i)]
        #qui on perdu des le 1er match, L_tier[1] ceux qui on perdu leur 2em match etc
        
        while len(L_tier[-1]) >= 2:  #on fait le tournoi pour placer tout les joueurs (on s'arrête quand on a un gagnant final)
            L_participant = L_tier[-1] 
            L_gagnant = []
            nbr_par = len(L_participant)
            np.random.shuffle(L_participant) #on melange la liste des participants pour rendre aleatoire les matchs

            for i in range(0,nbr_par//2,1):
                J1,J2 = L_participant[i],L_participant[i+1]
                if J1[1] >= J2[1]:
                    if np.random.random_sample() < self.proba_win: #le moins bon gagne si l'aleatoire est plus petit que self.proba_win
                        L_gagnant.append(J2)                #on ajoute le gagnant a une liste qu'on rajoutera a la fin a L_tier
                        L_tier[-1].remove(J2)               #on l'enleve du tier precedent (car il a réussi a passer au suivant)
                    else:
                        L_gagnant.append(J1)
                        L_tier[-1].remove(J1)
                else:
                    if np.random.random_sample() < self.proba_win:
                        L_gagnant.append(J1)
                        L_tier[-1].remove(J1)
                    else:
                        L_gagnant.append(J2)
                        L_tier[-1].remove(J2)

            if nbr_par%2 == 1:    #quand on a un nombre impaire de participant, par défaut le dernier participant gagne et passe au tier suivant 
                L_gagnant.append(L_participant[-1])
                L_tier[-1].remove(L_participant[-1])

            L_tier.append(L_gagnant)
        
        L_ajout = []  
        for i in range(self.number_parents): #pour faire l'ajout au current_parents, on rajoute les joueurs en commencant par le tier le plus haut
            if len(L_ajout) == 0:
                L_ajout = L_tier.pop()
            self.current_parents[i] = L_ajout.pop()    #je call des bug ici sorry
    
    def select(self):

        self.current_parents = np.empty((self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            #print(self.current_population[i])
            fitness_list.append(self.fitness_basic(self.current_population[i]))
        #print(fitness_list)
        self.sorted_idx = np.argsort(fitness_list)
        #print(self.sorted_idx)
        for i in range(self.number_parents):
            self.current_parents[i] = self.current_population[self.sorted_idx[i]]
        self.evolution_trace.append([self.current_population[self.sorted_idx[0]], fitness_list[self.sorted_idx[0]]])
        #self.current_parents = sorted(fitness_list)[:self.number_parents]
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)
        # print(self.current_parents)

    def crossover(self):
        #print(self.offspring_size)
        self.current_offspring = np.zeros(self.offspring_size)
        #print(self.current_offspring)
        #print(self.current_parents)
        middle = math.floor(self.offspring_size[1]/2)
        #print(middle)
        for i in range(self.offspring_size[0]):
            parent1 = i%self.number_parents
            parent2 = (i+1)%self.number_parents

            self.current_offspring[i][0:middle] = self.current_parents[parent1][0:middle]
            self.current_offspring[i][middle:] = self.current_parents[parent2][middle:]
        #print(self.current_offspring)

    # [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]

    def mutate(self):
        print("mutate")
        #print(self.current_offspring)
        if self.mutation_table != None:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    random_method = self.mutation_table[j][0]

                    if random_method == 'gauss':
                        mute_rate = random.gauss(mu=self.mutation_table[j][1], sigma=self.mutation_table[j][2])
                        #print(mute_rate, self.current_offspring[i][j])
                        self.current_offspring[i][j] += mute_rate
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
                        mute_rate = random.randint(a=self.mutation_table[j][1], b=self.mutation_table[j][2])
                        self.current_offspring[i][j] += mute_rate
                    elif random_method == 'choice':
                        mute_rate = random.choice(list=self.mutation_table[j][1])
                        self.current_offspring[i][j] += mute_rate
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
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness_basic(self.current_population[i]))
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
            # print(self.bestfit())
            self.clear()

    def print(self):
        for i in range(len(self.evolution_trace)):
            print("Generation "+str(i+1)+" (best) : ", self.evolution_trace[i][0], " (error : ", str(round(self.evolution_trace[i][1],4))+")")

# value = [21, 8, 4, 24]
# mutation_table = [['uniform', -0.6, 0.6, 21], ['uniform', -0.6, 0.6, 8], ['uniform', -0.6, 0.6, 4], ['uniform', -0.6, 0.6, 24]]#[['gauss',0,3],['gauss',0,1],['gauss',0,4],['gauss',0,10]]
# pop = np.random.randint(low=0, high=15, size=(30,4))
# gen = Genetic(5, 30, pop, {'mutation_table': mutation_table})
# print(pop)
# gen.launch()
# gen.print()
#print(np.array(gen.evolution_trace))
# Add a pattern system

# list = [[1,2,3],[[1,2,3],[4,[4,3],3,2]]]
__ORIGINAL_ROT_TABLE = {\
        "AA": [35.62, 7.2, -154,        0.06, 0.6, 0],\
        "AC": [34.4, 1.1, 143,          1.3, 5, 0],\
        "AG": [27.7, 8.4, 2,            1.5, 3, 0],\
        "AT": [31.5, 2.6, 0,            1.1, 2, 0],\
        "CA": [34.5, 3.5, -64,          0.9, 34, 0],\
        "CC": [33.67, 2.1, -57,         0.07, 2.1, 0],\
        "CG": [29.8, 6.7, 0,            1.1, 1.5, 0],\
        "CT": [27.7, 8.4, -2,           1.5, 3, 0],\
        "GA": [36.9, 5.3, 120,          0.9, 6, 0],\
        "GC": [40, 5, 180,              1.2, 1.275, 0],\
        "GG": [33.67, 2.1, 57,          0.07, 2.1, 0],\
        "GT": [34.4, 1.1, -143,         1.3, 5, 0],\
        "TA": [36, 0.9, 0,              1.1, 2, 0],\
        "TC": [36.9, 5.3, -120,         0.9, 6, 0],\
        "TG": [34.5, 3.5, 64,           0.9, 34, 0],\
        "TT": [35.62, 7.2, 154,         0.06, 0.6, 0]\
        }

# original_sample = [
#     35.62, 7.2,
#     34.4, 1.1,
#     27.7, 8.4,
#     31.5, 2.6,
#     34.5, 3.5,
#     33.67, 2.1,
#     29.8, 6.7,
#     27.7, 8.4,
#     36.9, 5.3,
#     40, 5,
#     33.67, 2.1,
#     34.4, 1.1,
#     36, 0.9,
#     36.9, 5.3,
#     34.5, 3.5,
#     35.62, 7.2,
# ]

original_sample = []
mutation_table = []
for c in __ORIGINAL_ROT_TABLE:
    dinuc = __ORIGINAL_ROT_TABLE[c]
    for i in range(2):
        original_sample.append(dinuc[i])
        mutation_table.append(['gauss bounded', dinuc[3+i], dinuc[i]])
# print(original_sample)
print(mutation_table)

population = []
for i in range(50):
    sample = []
    for j in range(len(mutation_table)):
        rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])
        # print(rand)
        sample.append(round(original_sample[j]+rand,5))
    population.append(sample)
print(population)
# population = np.array(population)

GA = Genetic(10, 100, population, {'mutation_table': mutation_table})
GA.launch()
GA.print()


rot_table = RotTable(GA.evolution_trace[-1][0])
traj = Traj3D()
traj.compute(seq, rot_table)
traj.draw("sample.png")