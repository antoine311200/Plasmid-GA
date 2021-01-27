'''
on a fitness et une liste d'individu
on a dans la class
on modifie le param current population
'''
import numpy as np

#pour etre une classe
def select(self):
    self.current_parents = np.empty((self.number_parents, self.population_size[1]))
    fitness_list = []
    for i in range(self.population_size[0]):
        fitness_list.append(fitness(self.current_population[i]))
    L_indice = np.argsort(fitness_list)
    for i in range(self.number_parents):
        self.current_parents[i] = self.current_population[L_indice[i]]


L = [2,5,8,3,10,16,18,1]

#fonction classique (comme ca ca je sais que ca marche)
def f_select(fitness,number_parents,L_popul):
    current_parents = []
    fitness_list = [fitness(indiv) for indiv in L_popul]
    L_indice = np.argsort(fitness_list)
    for i in range(number_parents):
        current_parents.append(L_popul[L_indice[i]])

    return current_parents


print(f_select(lambda x :x,3,L))

