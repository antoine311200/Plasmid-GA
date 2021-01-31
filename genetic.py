import numpy as np
import math as math
import os
import matplotlib.pyplot as plt
import random

""" Class Genetic :
    Classe qui permet d'effectuer un algorithme génétique sur une population d'individu (liste de leur gène)
    avec plusieurs paramètres ajustables
"""
class Genetic:

    """ Méthode : init
        Permet d'instancié un objet de la classe Genetic qui opère l'algorithme génétique
        @param :
        - number_parent : nombre de parent entre chaque génération
        - max_generation : nombre de génération effectué
        - population : population initiale
        - fitness_function : fonction qui prent en arg (indiv) ou (indiv, fitness_data)
                            et renvoi un nombre plus il est bas meilleurs et l'individu
        - data : dictionnaire de donnée supplémentaire
        @return :
        Une instance de Genetic :
            launch permet de lancer le calcul avec max_generation générations
            print donne le dernier meilleurs individus de la derniere génération
    """
    def __init__(self, number_parents, max_generation, population, fitness_function, data = {}):
        
        self.data = {"selection_mode" : "elitist", "crossover_mode" : "normal", "mutation_table" : None, "fitness_data" : None, "crossover_data": [1,1,1,1]}
        
        for (k,v) in data.items():
            self.data[k] = v
        
        self.number_parents = number_parents
        self.max_generation = max_generation
        self.initial_population = population
        """ Explication de data
            data est un dictionnaire qui contient toute les informations importantes pour le choix des méthodes de Genetic
            "selection_mode" : mode de selection des individu : elitist, tournoi ou fulltournoi sont acceptés
            "crossover_mode" : méthode du crossover, actuellement seul : "normal" est accepté
            "mutation_table" : Continent None, ou une liste de liste, chaque élement représente un gène ["type de mutation", param1, param2, ...]
                   "type de mutation" accepte beaucoup de valeur : gauss, uniform, uniform bounded, gauss bounded, randint, triangular
                   param1, param2 correspond au paramètre de chaque fonction particuliere
            "fitness_data" : un liste de donnée qui sera mise en paramètre de la fitness_function, None si il n'y en a pas besoin

        """
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

    """ Méthode : fitness
        selon qu'il y ai besoin de la fitness_data, appelle la fonction donnée en argument avec les bon paramètre
        renvoie la valeur en tant que fitness de l'individu
    """
    def fitness(self, individual):
        if(self.has_fitness_data):
            return self.fitness_function(individual, *self.fitness_data)
        else :
            return self.fitness_function(individual)

    """ Méthode : select
        La fonction de selection qui est appelé par launch
        la méthode utlisé dépend du paramètre self.selection_mode
    """
    def select(self):
        if(self.selection_mode == "elitist"):
            self.select_elit()
        elif (self.selection_mode == "tournoi"):
            self.select_tournoi_simple()
        elif(self.selection_mode == "fulltournoi"):
            self.select_tournoi()
    
    """ Méthode : select_elit
        Méthode de sélection elitist, prend simplement les self.number_parent individu les meilleurs
    """
    def select_elit(self):
        self.current_parents = np.empty(
            (self.number_parents, self.population_size[1]))
        fitness_list = []
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))
        L_indice = np.argsort(fitness_list)
        for i in range(self.number_parents):
            self.current_parents[i] = self.current_population[L_indice[i]]

        #Sauvegarde l'historique de l'algorithme génétique
        self.evolution_trace.append([self.current_population[L_indice[0]], fitness_list[L_indice[0]], sum(fitness_list)/self.population_size[0]])
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)

    """ Méthode : select_tournoi_simple
        Méthode de selection par tounoi classique
        D'abord on prends 10% du nombre de parents voulu simplement car ils sont les meilleurs de leur génération,
        puis on effectue le tournoi, on prends deux individus, on regarde qui est le meilleurs, et on le selectionne
        on repete l'opération jusqu'à obtenir le nombre de parents voulus
    """
    def select_tournoi_simple(self):
        indice_list = list(range(self.population_size[0]))
        fitness_list = []
        #Calcule de la fitness de chaque individu
        for i in range(self.population_size[0]):
            fitness_list.append(self.fitness(self.current_population[i]))
        sorted_idx = np.argsort(fitness_list)
        #selection des meilleurs
        for i in range(self.number_parents//10):
            indice_list.remove(sorted_idx[i])
            self.current_parents.append(self.current_population[sorted_idx[i]])
        
        #Tournoi en tant que tel, si on epuise la liste des indices avant la fin du tournoi,
        # on réutilise les perdants, jusqu'à obtenir le bon nombre de survivant
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

        #Sauvegarde l'historique de l'algorithme génétique
        self.evolution_trace.append([self.current_population[sorted_idx[0]], fitness_list[sorted_idx[0]], sum(fitness_list)/self.population_size[0]])
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

        for i in range(self.number_parents//10):
            self.current_parents[i] = self.current_population[L_indice[0]]
            
        
        L_tier = []
        L_tier.append([[self.current_population[i], fitness_list[i], i]
                     for i in L_indice[self.number_parents//10:]])
        
        # L_tier est la liste des placements, par ex L_tier[0] contient la liste des couples [individu_i,fitness(individu_i)]
        # qui on perdu des le 1er match, L_tier[1] ceux qui on perdu leur 2em match etc
        # on fait le tournoi pour placer tout les joueurs (on s'arrête quand on a un gagnant final)
        
        # .remove ne marche pas ici car les individu contiennent des arrays
        # donc on a besoin des indices des individus dans L_tier pour les pop plus tard
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
            # on prend les indices a pop en ordres decroissant (pour ne pas modifier les indices a pop suivant)
            L_ind_to_pop.sort(reverse=True)
            for k in L_ind_to_pop:
                L_tier[-1].pop(k)
            L_tier.append(L_gagnant)
        # pour faire l'ajout au current_parents, on rajoute les joueurs en commencant par le tier le plus haut
        L_ajout = []
        for i in range(self.number_parents//10, self.number_parents):
            if len(L_ajout) == 0:
                L_ajout = L_tier.pop()
            self.current_parents[i] = L_ajout.pop()[0]
        
        #Sauvegarde l'historique de l'algorithme génétique
        self.evolution_trace.append([self.current_population[L_indice[0]], fitness_list[L_indice[0]], sum(fitness_list)/self.population_size[0]])
        if self.history_parents_enable:
            self.parents_history.append(self.current_parents)

    """ Méthode : repro
        Crée un enfant en mélangeant les gènes des d parents
    """
    def repro(self, Parents, d): # d = nombre de parents
        
        nb_chrmsm = self.offspring_size[1]//d # nb_chrmsm : nombre de gènes transmis par chaque parent à l'enfant
        
        # Méthode déterministe : on sélectionne un bout de même taille pour chaque parent, puis on les concatène
        if self.crossover_mode == "normal":
            child = Parents[0].copy() 
            for i in range(1, d-1):
                child[i*nb_chrmsm:(i+1)*nb_chrmsm] = Parents[i][i*nb_chrmsm:(i+1)*nb_chrmsm].copy() 
            # on complète avec le bon nombre de gènes, provenant du dernier parent
            child[(d-1)*nb_chrmsm:] = Parents[-1][(d-1)*nb_chrmsm:].copy()


        # Méthode probabiliste discrète : chaque gène est choisi au hasard parmi ceux de ses parents
        elif self.crossover_mode == "uniform":
            child = []
            for i in range(self.population_size[1]):
                j = random.randint(0, d-1)
                child += [Parents[j][i]]

        # Méthode probabiliste discrète : chaque gène est choisi au hasard parmi ceux de ses parents,
        #mais le gène du premier parent a plus d'une chance sur deux, soit (d+1)/(2d), d'être sélectionné.
        elif self.crossover_mode == "uniform bias":
            child = []
            for i in range(self.population_size[1]):
                j = random.randint(0, d-1)
                j = random.randint(0, j)
                child += [Parents[j][i]]

        # Méthode probabiliste continue : chaque gène suit une somme de lois normales, chacune centrée sur le gène d'un parent
        elif self.crossover_mode == "gaussian":
            child = []
            
            for i in range(self.population_size[1]):
                var_gene = self.mutation_table[i][1] # variance sur le gene i
                s = 0
                for j in range(self.population_size[1]):
                    s += random.gauss(Parents[j], self.mutation_table[i][1], 1000)
                s = s/d # renormalisation de la probabilité
                if s < (self.mutation_table[i][2] - var_gene):
                    child.append(self.mutation_table[i][2] - var_gene)
                elif s > (self.mutation_table[i][2] + var_gene):
                    child.append(self.mutation_table[i][2] + var_gene)
                else:
                    child.append(s)

        return child

    """ Méthode : crossover
        Applique le crossover aux individus sélectionnés par le select() afin de revenir à un popultation de taille normale
    """
    def crossover(self): # crée la prochaine génération

        while len(self.current_offspring) < self.offspring_size[0] :

            for d in range(2, len(self.sx_weights)+2): # d = nbr de parents pour créer un seul enfant
                poids = self.sx_weights[d-2] # poids = nombre de fois où l'on va crée un enfant avec ce nombre de parents

                for _ in range(poids):
                    if len(self.current_offspring) >= self.offspring_size[0] :
                        return
                    rd_parents = [random.choice(self.current_parents) for _ in range(d)]# choix de d parents aléatoires
                    child = self.repro(rd_parents, d) # création de l'enfant
                    self.current_offspring.append(child)

    ''' Méthode : mutate
        Cette méthode est l'opérateur de mutation de l'algorithme génétique.
        Elle ne prend pas d'argument et utilise la table de mutation fournie dans les data
        au moment de créer une nouvelle instance de la classe Genetic.
        Pour chaque gène de chaque individu, on applique une mutation basée sur la distribution
        donnée dans la table de mutation. Dans le cas où il n'y aurait pas de table de mutation,
        on applique seulement une mutation uniforme sur un intervalle réduit.
        Voici la syntaxe pour les éléments de la table de mutation en fonction de la distribution
        de probabilité choisie : 
        - gauss             -> 'gauss', mu (float, la moyenne), sigma (float, la variance)
        - uniform           -> 'uniform', min (float), max (float)
        - uniform bounded   -> 'uniform bounded', mut_min, mut_max, min(float), max(float)
        - gauss bounded     -> 'gauss bounded', sigma (float, la variance), origin (float, centre de l'intervall de taill 2 sigma), factor (float, )
        - triangular        -> 'triangular', low (float), high (float), mode (float)
        - randint           -> 'randint', min (int), max (int)
        - choices           -> 'choice', list (float list)
    '''
    def mutate(self):
        if self.mutation_table != None:
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    random_method = self.mutation_table[j][0]

                    # Distribution gaussienne
                    if random_method == 'gauss':
                        mute_rate = random.gauss(mu=self.mutation_table[j][1], sigma=self.mutation_table[j][2])
                        self.current_offspring[i][j] += mute_rate

                    # Distribution uniforme
                    elif random_method == 'uniform':
                        a,b = self.mutation_table[j][1], self.mutation_table[j][2]
                        # origin = self.mutation_table[j][3]
                        mute_rate = random.uniform(a, b)

                        # if self.current_offspring[i][j]+mute_rate <= origin+b and self.current_offspring[i][j]+mute_rate >= origin+a:
                        self.current_offspring[i][j] += mute_rate
                    
                    # Distribution uniforme bornée
                    elif random_method == 'uniform bounded':

                        vmin,vmax=self.mutation_table[j][1], self.mutation_table[j][2]
                        a,b = self.mutation_table[j][3], self.mutation_table[j][4]

                        # l = 0
                        if self.current_offspring[i][j] < a or self.current_offspring[i][j] > b:
                            print('\n', a, self.current_offspring[i][j], b)
                            raise Exception("individual "+str(i)+" is out of segment")
                    
                        fail_index = 0
                        while True:
                            fail_index+=1
                            if fail_index>=25:
                                raise Exception("individual "+str(i)+" is out of segment")

                            mute_rate = random.uniform(vmin, vmax)
                            if self.current_offspring[i][j]+mute_rate >= a and self.current_offspring[i][j]+mute_rate <= b:
                                self.current_offspring[i][j] += mute_rate
                                break
                    
                    # Distribution gaussienne restreinte à un intervalle
                    elif random_method == 'gauss bounded':

                        sigma = self.mutation_table[j][1]
                        origin = self.mutation_table[j][2]
                        variance = self.mutation_table[j][3]

                        if self.current_offspring[i][j] < origin-sigma or self.current_offspring[i][j] > origin+sigma:
                            raise Exception("individual "+str(i)+" is out of segment")
                        
                        fail_index = 0
                        while True:
                            fail_index+=1
                            if fail_index>=25:
                                raise Exception("individual "+str(i)+" is out of segment")

                            mute_rate = random.gauss(mu=self.current_offspring[i][j], sigma=sigma/variance)#max(origin-sigma, min(origin+sigma, random.gauss(mu=self.current_offspring[i][j], sigma=sigma)))
                            if mute_rate >= origin-sigma and mute_rate <= origin+sigma:
                                self.current_offspring[i][j] = mute_rate
                                break
                    
                    # Distribution triangulaire
                    elif random_method == 'triangular':
                        mute_rate = random.triangular(low=self.mutation_table[j][1], high=self.mutation_table[j][2], mode=self.mutation_table[j][3])
                    elif random_method == 'randint':
                        mute_rate = random.randint(a=self.mutation_table[j][1], b=self.mutation_table[j][2])
                        self.current_offspring[i][j] += mute_rate

                    # Choix d'un mute rate parmi une liste de floatant
                    # elif random_method == 'choice':
                        # mute_rate = random.choice(list=self.mutation_table[j][1])
                        # self.current_offspring[i][j] += mute_rate
                    else:
                        mute_rate = random.uniform(-0.02, 0.02)
                        self.current_offspring[i][j] += mute_rate
                    
                    self.current_offspring[i][j] = round(self.current_offspring[i][j], 9)

        else:
            # Mutation uniforme dans le cas où la table de mutation n'a pas été fournie
            for i in range(self.offspring_size[0]):
                for j in range(self.offspring_size[1]):
                    self.current_offspring[i][j] += random.uniform(-0.02, 0.02)
        
        self.current_population = np.concatenate((self.current_parents,self.current_offspring), axis=0)
    
    ''' Method : log
        Cette méthode permet d'enregistrer les paramètres du modèle ainsi 
        que les erreurs aux différentes générations dans un fichier
        @param folder - le path du dossier où sera stocké le fichier de donnée
        @param name - un nom pour reconnaître son modèle 
        @return - None, mais le fichier est créé au nom 'ga_[name]_[random int]'
    '''
    def log(self, folder, name=""):
        self.folder = folder
        self.name = name

        string_parameters = [
            str(self.number_parents),
            str(self.max_generation),
            str(self.population_size[0]),
            str(self.population_size[1]),
            self.selection_mode,
            self.crossover_mode
        ]

        line_data = ' '.join(string_parameters)
        line_error = ' '.join(list(map(str, np.array(self.evolution_trace, dtype=object)[::,1])))

        file = open(self.folder+'/ga_'+self.name+str(random.randint(0,100000)), 'w')
        file.write(line_data)
        file.write('\n')
        file.write(line_error)
        file.close()

    ''' Method : plot
        Affiche l'évolution de l'erreur du meilleur individu à chaque génération
    '''
    def plot(self):
        plt.plot(np.linspace(1, self.max_generation, self.max_generation), np.array(self.evolution_trace, dtype=object)[::,1])
        
        plt.xlabel('Generations')
        plt.ylabel('Minimum error')

        plt.show()

    ''' Static method : plot_all
        Méthode statique qui permet de charger tous les fichiers de donnée dans le dossier
        donné
        @param folder - le nom du dossier où sont enregistés les fichiers de donnée
        @return - None, mais on affiche un graphe des évolutions des erreurs de chaque fichier 
    '''
    @staticmethod
    def plot_all(folder='ga_save'):
        pathname = os.getcwd()+'/'+folder
        for filename in os.listdir(pathname):
            with open(os.path.join(pathname, filename), 'r') as file:
                number_generation = int(file.readline().split(' ')[1])
                line = file.readline()
                # print(number_generation, line, list(map(float,line.split(' '))))
                plt.plot(np.linspace(1, number_generation, number_generation), list(map(float,line.split(' '))))
                file.close()
        plt.show()
    ''' Méthode : bestfit
        @return Renvoie le score de fitness du meilleur 
                individu de la dernière génération en cours
    '''
    def bestfit(self):
        return round(self.evolution_trace[-1][1],4)
    
    """ Méthode : meanfit
        @return Renvoie la valeur du fitness moyen de la génération
    """
    def meanfit(self):
        return round(self.evolution_trace[-1][2], 2)

    ''' Méthode : clear
        Vide les parents et enfants actuels afin de préparer la nouvelle génération
    '''
    def clear(self):
        self.current_offspring = []
        self.current_parents = []

    ''' Méthode : launch
        Fait fonctionner l'algorithme génération par génération
        en faisant appel à chaque opérateur
    '''
    def launch(self):
        for i in range(self.max_generation):
            print(f"Generation : {i} : ", end=' ')
            self.current_generation += 1

            self.select()
            self.crossover()
            self.mutate()

            print(self.bestfit(), "   ", self.meanfit())
            self.clear()

    ''' Méthode : print
        Renvoie le meilleur individu de la dernière génération en cours et son erreur
    '''
    def print(self):
        print("Generation last (best) : ", self.evolution_trace[-1][0], " (error : ", str(round(self.evolution_trace[-1][1],4))+")")