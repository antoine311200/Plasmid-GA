from plasmid import *
from encodage import *
from Traj3D import *
from RotTable import *
import random
import math as math
import numpy as np

L = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [6, 2, 0]]
np.random.shuffle(L[0])
L[1].remove(0)
print(L)


class Genetic:

    def __init__(self, number_parents, max_generation, population, fitness_function, data={"selection_mode": "tournoi", "crossover_mode": "normal", "mutation_table": None, "fitness_data": None}):
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

        self.current_generation = 0
        self.population_size = self.initial_population.shape
        self.offspring_size = (
            self.population_size[0]-self.number_parents, self.population_size[1])

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
        else:
            return self.fitness_function(individual)

    # elitist selection
    # roulette selection : p_i = f_i / sum f_j (sur-representativity !!!)
    # rang selection : sort -> index = proportion (smoothing) (convergence time !!!)
    # tournament selection : 2 random -> best score (+ probabilty of win) => diversity

    def select_(self):
        self.current_parents = np.empty(
            (self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))

        L_indice = np.argsort(fitness_list)
        for i in range(self.number_parents):
            self.current_parents[i] = self.current_population[L_indice[i]]

        self.evolution_trace.append(
            [self.current_population[L_indice[0]], fitness_list[L_indice[0]]])
        #self.current_parents = sorted(fitness_list)[:self.number_parents]
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)

    def select(self):
        self.proba_win = 0.1
        self.current_parents = np.empty(
            (self.number_parents, self.population_size[1]))

        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))

        L_indice = np.argsort(fitness_list)

        L_tier = []
        L_tier.append([[self.current_population[i], self.fitness(
            self.current_population[i]), i] for i in range(self.population_size[0])])

        # L_tier est la liste des placements, par ex L_tier[0] contient la liste des couples [individu_i,fitness(individu_i)]
        # qui on perdu des le 1er match, L_tier[1] ceux qui on perdu leur 2em match etc

        # on fait le tournoi pour placer tout les joueurs (on s'arrête quand on a un gagnant final)
        while len(L_tier[-1]) >= 2:
            L_participant = L_tier[-1]
            nbr_par = len(L_participant)
            for k in range(nbr_par):
                L_participant[k][2] = k
            L_gagnant = []

            # on melange la liste des participants pour rendre aleatoire les matchs
            np.random.shuffle(L_participant)

            L_ind_to_pop = []

            for i in range(0, nbr_par//2, 2):
                J1, J2 = L_participant[i], L_participant[i+1]
                ind_J1, ind_J2 = J1[2], J2[2]

                if J1[1] <= J2[1]:
                    # le moins bon gagne si l'aleatoire est plus petit que self.proba_win
                    if np.random.random_sample() < self.proba_win:
                        # on ajoute le gagnant a une liste qu'on rajoutera a la fin a L_tier
                        L_gagnant.append(J2[:2] + [i+1])
                        # on l'enleve du tier precedent (car il a réussi a passer au suivant)
                        L_ind_to_pop.append(ind_J2)
                    else:
                        L_gagnant.append(J1[:2] + [i])
                        L_ind_to_pop.append(ind_J1)

                else:
                    if np.random.random_sample() < self.proba_win:
                        L_gagnant.append(J1[:2] + [i])
                        L_ind_to_pop.append(ind_J1)
                    else:
                        L_gagnant.append(J2[:2] + [i+1])
                        L_ind_to_pop.append(ind_J2)

            if nbr_par % 2 == 1:  # quand on a un nombre impaire de participant, par défaut le dernier participant gagne et passe au tier suivant
                L_gagnant.append(L_participant[-1])
                L_ind_to_pop.append(L_participant[-1][2])

            L_ind_to_pop.sort(reverse=True)
            for k in L_ind_to_pop:
                L_tier[-1].pop(k)

            L_tier.append(L_gagnant)

        L_ajout = []        # pour faire l'ajout au current_parents, on rajoute les joueurs en commencant par le tier le plus haut
        for i in range(self.number_parents):
            if len(L_ajout) == 0:
                L_ajout = L_tier.pop()
            self.current_parents[i] = L_ajout.pop()[0]

        self.evolution_trace.append(
            [self.current_population[L_indice[0]], fitness_list[L_indice[0]]])

    # def crossover(self, nb_ch_voulu):
    #     P = self.current_parents
    #     C = []
    #     nb_ch = 0
    #     taille = self.offspring_size[1]
    #     while nb_ch < nb_ch_voulu :
    #         sx_nb_par = nb_ch % self.sx_max_par
    #         sx_weight = self.sx_weigths[nb_ch % self.sx_max_parents]
    #         for i in range(sx_weight): # on a pondéré le nombre d'enfants
    #             child = parent[i].copy()
    #             k = 1
    #             for j in range(taille):
    #                 k = min(taille-1, rd(k+1, taille-1))
    #                 parent = P[(nb_ch + i + k) % self.sx_max_parents]
    #                 child[k:] = parent[k:].copy()
    #             C.append(child)
    #             nb_ch +=  1
    #     self.current_offsprings = C[:nb_ch_voulu]

    def crossover(self):
        # print(self.offspring_size)
        self.current_offspring = np.zeros(self.offspring_size)
        # print(self.current_offspring)
        # print(self.current_parents)
        middle = math.floor(self.offspring_size[1]/2)
        # print(middle)
        for i in range(self.offspring_size[0]):
            parent1 = i % self.number_parents
            parent2 = (i+1) % self.number_parents

            self.current_offspring[i][0:middle] = self.current_parents[parent1][0:middle]
            self.current_offspring[i][middle:] = self.current_parents[parent2][middle:]
        # print(self.current_offspring)

    def mutate(self):
        # print("mutate")
        # print(self.current_offspring)
        if self.mutation_table != None:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    random_method = self.mutation_table[j][0]

                    if random_method == 'gauss':
                        while True:
                            mute_rate = random.gauss(
                                mu=self.mutation_table[j][1], sigma=self.mutation_table[j][2])
                            #print(mute_rate, self.current_offspring[i][j])
                            self.current_offspring[i][j] += mute_rate
                            break
                    elif random_method == 'uniform':
                        # while True:
                        a, b = self.mutation_table[j][1], self.mutation_table[j][2]
                        origin = self.mutation_table[j][3]
                        mute_rate = random.uniform(a, b)
                        # print(mute_rate, self.current_offspring[i][j])
                        if self.current_offspring[i][j]+mute_rate <= origin+b and self.current_offspring[i][j]+mute_rate >= origin+a:
                            self.current_offspring[i][j] += mute_rate
                    elif random_method == 'gauss bounded':
                        origin = self.mutation_table[j][2]
                        sigma = self.mutation_table[j][1]

                        while True:
                            # max(origin-sigma, min(origin+sigma, random.gauss(mu=self.current_offspring[i][j], sigma=sigma)))
                            mute_rate = random.gauss(
                                mu=self.current_offspring[i][j], sigma=sigma/100)
                            # print(self.current_offspring[i][j], mute_rate, origin-sigma, origin+sigma)
                            if mute_rate >= origin-sigma and mute_rate <= origin+sigma:
                                self.current_offspring[i][j] = mute_rate
                                break
                        # if mute_rate == origin-sigma:

                    elif random_method == 'triangular':
                        mute_rate = random.triangular(
                            low=self.mutation_table[j][1], high=self.mutation_table[j][2], mode=self.mutation_table[j][3])
                    elif random_method == 'randint':
                        while True:
                            mute_rate = random.randint(
                                a=self.mutation_table[j][1], b=self.mutation_table[j][2])
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

                    self.current_offspring[i][j] = round(
                        self.current_offspring[i][j], 5)

        else:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    self.current_offspring[i][j] += np.random.randint(
                        self.mutation_table[j].min, self.mutation_table[j].max)

        self.current_population = np.concatenate(
            (self.current_parents, self.current_offspring), axis=0)

    def bestfit(self):
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))
        self.sorted_idx = np.argsort(fitness_list)
        return self.current_population[self.sorted_idx[0]]

    def clear(self):
        self.current_offspring = []
        self.current_parents = []

    def launch(self):
        for _ in range(self.max_generation):
            # print("Next generation")
            self.current_generation += 1
            self.select()
            self.crossover()
            self.mutate()
            # print(self.current_population)
            # print(self.bestfit())
            self.clear()

    def print(self):
        for i in range(len(self.evolution_trace)):
            print("Generation "+str(i+1)+" (best) : ",
                  self.evolution_trace[i][0], " (error : ", str(round(self.evolution_trace[i][1], 4))+")")

# value = [21, 8, 4, 24]
# pop = np.random.randint(low=0, high=15, size=(30,4))
# gen = Genetic(5, 30, pop)
# print(pop)
# gen.launch()
# gen.print()
# print(np.array(gen.evolution_trace))
# Add a pattern system


list = [[1, 2, 3], [[1, 2, 3], [4, [4, 3], 3, 2]]]


lineList = [line.rstrip('\n') for line in open("./resources/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])

mutation_table = dataForMutation(RotTable())
indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5,
         3.5, 33.67, 2.1, 29.8, 6.7, 36.9, 5.3, 40, 5, 36, 0.9]

population = []
for i in range(20):
    sample = []
    for j in range(len(mutation_table)):
        rand = random.uniform(-mutation_table[j][1], +mutation_table[j][1])

        sample.append(round(indiv[j]+rand, 5))
    population.append(sample)
population = np.array(population)


def fitness_indiv(indiv, data):
    trajectory = data[0]
    sequence = data[1]
    return Plasmid("", decodage(indiv), trajectory, sequence).getDistance()

# def fitness_indiv(indiv, data):
#     data[0].compute(data[1], decodage(indiv))
#     lastVect = data[0].getLastFromTraj()
#     return(math.sqrt(lastVect.dot(lastVect)))


data = {"selection_mode": "tournoi", "crossover_mode": "normal",
        "mutation_table": dataForMutation(RotTable()), "fitness_data": [Traj3D(), seq]}


print(fitness_indiv(indiv, [Traj3D(), seq]))


gen = Genetic(5, 10, population, fitness_indiv, data=data)
gen.launch()
gen.print()


rot_table = decodage(gen.evolution_trace[-1][0])
traj = Traj3D()
traj.compute(seq, rot_table)
traj.draw("se")
