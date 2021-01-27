import numpy as np
import math as math

import random


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
        self.population_size = (len(self.initial_population),  len(self.initial_population[0]))
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
    def select_elit(self):
        self.current_parents = np.empty(
            (self.number_parents, self.population_size[1]))
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
    
    def select(self):
        if(self.selection_mode == "elitist"):
            self.select_elit()
        elif (self.selection_mode == "tournoi"):
            self.select_tournoi2()


    def select_tournoi2(self):
        indice_list = list(range(self.population_size[0]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))
        sorted_idx = np.argsort(fitness_list)

        for i in range(self.number_parents//10):
            indice_list.remove(sorted_idx[i])
            self.current_parents.append(self.current_population[sorted_idx[i]])
        loser_idx=[]
        for i in range(self.number_parents-self.number_parents//10):
            if(len(indice_list)<2):
                indice_list += loser_idx
                loser_idx=[]
            a=random.choice(indice_list)
            indice_list.remove(a)
            b=random.choice(indice_list)
            indice_list.remove(b)

            if( fitness_list[a] > fitness_list[b]):# b gagne
                self.current_parents.append(self.current_population[b])
                loser_idx.append(a)
            else : # a gagne
                self.current_parents.append(self.current_population[a])
                loser_idx.append(b)
        
        self.evolution_trace.append([self.current_population[sorted_idx[0]], fitness_list[sorted_idx[0]]])

        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)



    def select_tournoi(self):
        self.proba_win = 0.01
        self.current_parents = np.empty(
            (self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))
        L_indice = np.argsort(fitness_list)
        L_tier = []
        L_tier.append([[self.current_population[i], fitness_list[i], i]
                     for i in range(self.population_size[0])])
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
        while True :
            # On va créer en boucle sum(self.sx_weights) enfants, jusqu'à en avoir le nombre voulu.
            # L'intérêt est qu'à chaque itération, le nombre d'enfants créés pour chaque méthode 
            # de reproduction (une méthode est caractérisée par un nombre de parents) est donné
            # par le poids de la méthode, indiqué dans le tableau self.sx_weights.

            for d in range(2, len(self.sx_weights)+2): # d = nbr of parents pour créer un enfant
                poids = self.sx_weights[d-2] # poids = nombre de fois où on va appliquer la méthode

                for _ in range(poids):
                    if len(self.current_offspring) >= self.offspring_size[0]  :
                        return
                    rd_parents = [random.choice(self.current_parents) for _ in range(d)] # choix de d parents aléatoires
                    child = self.repro(rd_parents, d)
                    self.current_offspring.append(child)

    def mutate(self):
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
                        variance = self.mutation_table[j][3]
                        while True:
                            mute_rate = random.gauss(mu=self.current_offspring[i][j], sigma=sigma/variance)#max(origin-sigma, min(origin+sigma, random.gauss(mu=self.current_offspring[i][j], sigma=sigma)))
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
        for i in range(self.max_generation):
            print(f"Generation : {i} : ", end=' ')
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
