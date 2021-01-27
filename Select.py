'''
on a fitness et une liste d'individu
on a dans la class
on modifie le param current population
'''
import numpy as np

# Selection elitiste

# pour etre une classe


def select_elit(self):
    self.current_parents = np.empty(
        (self.number_parents, self.population_size[1]))
    fitness_list = []
    for i in range(self.population_size[0]):
        fitness_list.append(fitness(self.current_population[i]))
    L_indice = np.argsort(fitness_list)
    for i in range(self.number_parents):
        self.current_parents[i] = self.current_population[L_indice[i]]


# fonction classique (comme ca ca je sais que ca marche)
def f_select_elit(fitness, number_parents, L_popul):
    current_parents = []
    fitness_list = [fitness(indiv) for indiv in L_popul]
    L_indice = np.argsort(fitness_list)
    for i in range(number_parents):
        current_parents.append(L_popul[L_indice[i]])

    return current_parents


# Selection tournoi


# il faudrait rajouter l'objet self.proba_win (la chance de gagner un match meme si on devrait le perdre) dans la class
# (ou def une variable global)

def select_tournoi(self):

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

# osef de cette fonction (f_select_tournoi) seul la fonction precedente est a copier dans genetics
# sous la forme de fonction que je pouvais trifouiller pour debuger, normalemetn c'est select_tournoi(self) qu'il faut copier dans genetic et pas cette fonction


def f_select_tournoi(fitness, number_parents, L_popul, proba_win):
    current_parents = np.empty((number_parents, 1))
    L_tier = []
    L_tier.append([[L_popul[i], fitness(L_popul[i])]
                   for i in range(len(L_popul))])
    while len(L_tier[-1]) >= 2:
        L_participant = L_tier[-1]
        L_gagnant = []
        nbr_par = len(L_participant)
        np.random.shuffle(L_participant)
#        print(L_participant)
#        print('L_tier: ' + str(L_tier))
        for i in range(0, nbr_par//2, 1):
            J1, J2 = L_participant[i], L_participant[i+1]
#            print(J1,J2)
            if J1[1] >= J2[1]:
                if np.random.random_sample() < proba_win:
                    L_gagnant.append(J2)
                    L_tier[-1].remove(J2)
                else:
                    L_gagnant.append(J1)
                    L_tier[-1].remove(J1)
            else:
                if np.random.random_sample() < proba_win:
                    L_gagnant.append(J1)
                    L_tier[-1].remove(J1)
                else:
                    L_gagnant.append(J2)
                    L_tier[-1].remove(J2)
        if nbr_par % 2 == 1:
            L_gagnant.append(L_participant[-1])
            L_tier[-1].remove(L_participant[-1])
        L_tier.append(L_gagnant)

#    print('L_tier: ' + str(L_tier))
    L_ajout = []
    for i in range(number_parents):
        if len(L_ajout) == 0:
            L_ajout = L_tier.pop()
        current_parents[i][0] = L_ajout.pop()[0]
    return current_parents


L = [20, 67, 48, 95, 24, 10, 42, 69, 2, 3, 5, 100, 38]

L_survivant = f_select_tournoi(lambda x: x, 5, L, 0.1)
print(L_survivant)
