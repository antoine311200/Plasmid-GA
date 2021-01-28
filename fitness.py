from encodage import decodage

from Traj3D import *

indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]


dna_seq = "AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG"

def fitness_indiv(indiv, traj3D, dna_seq):
    traj3D.compute(dna_seq, decodage(indiv))
    lastVect = traj3D.getLastFromTraj()
    return(lastVect.dot(lastVect))


"""
data est un dictionnaire qui contient toute les informations importantes pour le choix des méthodes de Genetic
"selection_mode" : mode de selection des individu : elitist, tournoi ou fulltournoi sont acceptés
"crossover_mode" : méthode du crossover, actuellement seul : "normal" est accepté
"mutation_table" : Continent None, ou une liste de liste, chaque élement représente un gène ["type de mutation", param1, param2, ...]
                   "type de mutation" accepte beaucoup de valeur : gauss, uniform, gauss bounded, randint, triangular
                   param1, param2 correspond au paramètre de chaque fonction particuliere
"fitness_data" : un liste de donnée qui sera mise en paramètre de la fitness_function, None si il n'y en a pas besoin

"""