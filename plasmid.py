import math
from RotTable import *
from Traj3D import *

''' Class : Plasmid
Cette class représente un Plasmide
Elle contient des attributs tel que la sequence ADN, la table de rotation
Et contient les methodes qui viennent de Traj3D tel que compute et draw
'''
class Plasmid:
    #les dinucléotide qui sont importants, les autres sont des symetriques de cela
    important_dinucleotides = ["AA", "AC", "AG", "AT", "CA", "CC", "CG", "GA", "GC", "TA"]

    # la table qui permet de retrouver les symétriques
    symetricADN = {"A" : "T", "T" : "A",\
               "C" : "G", "G" : "C"}


    #permet d'obtenir le symetrique d'un dinucleotique
    @staticmethod
    def getSymetric(dinucleotide):
        sym = Plasmid.symetricADN[dinucleotide[1]] + Plasmid.symetricADN[dinucleotide[0]]
        return sym

    """
    @param : indiv : float list de taille 20
    @return : une RotTable qui contient les donnée de indiv
    """
    @staticmethod
    def decodage(indiv):
        data = {}

        for i,dinucleotide in enumerate(Plasmid.important_dinucleotides) :
            data[dinucleotide] = indiv[2*i:2*(i+1)]
            data[Plasmid.getSymetric(dinucleotide)] = indiv[2*i:2*(i+1)]

        return RotTable(data)
    """
    @param:
        signature : ID du Plasmid
        rotation_table : la RotTable du Plasmid
        trajectory : une instance de Traj3D permettant de compute la trajectoire
        sequence : la séquence ADN du plasmid
        number_rempli : le nombre de nucléotide du début de la chaine rajouté à la fin de la chaine
                        pour avoir une fonction de fitness meilleurs
    @return : une instance de Plasmid
    """
    def __init__(self, signature, rotation_table=RotTable(), trajectory=Traj3D(), sequence='AAAA', number_repli=15):
        self.signature = signature
        self.sequence = sequence
        self.rotation_table = rotation_table
        self.trajectory = trajectory
        self.number_repli= number_repli
        self.compute()

    """
    @param : le filepath du fichier ou se trouve un code ADN de Plasmide
    Charge dans self.sequence le fichier ADN en questino, avec le rempliement
    """
    def load(self, filepath):
        self.filepath = filepath
        
        lineList = [line.rstrip('\n') for line in open(filepath)]
        self.sequence = ''.join(lineList[1:])
        self.sequence += self.sequence[:self.number_repli]
        self.compute()
    
    """
    @return : l'individu qui correspond à la rotTable du Plasmid
    """ 
    def encodage(self): #rotTable -> floatlist
        individu = []
        for dinucleotide in Plasmid.important_dinucleotides :
            individu += [self.rotation_table.getTwist(dinucleotide), self.rotation_table.getWedge(dinucleotide)]
        return individu

    # Modifie la RotTable de l'instance de Plasmid
    def setRotationTable(self, rotation_table):
        self.rotation_table = rotation_table

    # Modifie la sequence ADN de l'instance de Plasmid
    def setSequence(self, sequence):
        self.sequence = sequence

    # Dessine le courbe du Plasmide
    def draw(self):
        self.trajectory.draw(self.number_repli)

    # Calcule le courbe du Plasmide
    def compute(self):
        self.trajectory.compute(self.sequence, self.rotation_table)
    
    """
    @return : Renvoie la distance entre les self.number_rempli nucléotides du début de la chaine avec les
    self.number_rempli nucléotides fictifs présents a la fin de la chaine, sert de fonction fitness dans Genetic 
    """
    def getDistance(self):
        dist = 0
        for i in range(self.number_repli):
            point1 = self.trajectory.getIndexFromTraj(i)
            point2 = self.trajectory.getIndexFromTraj(-self.number_repli+i)
            var = point1-point2
            dist += math.sqrt(var.dot(var))/(i+1) # correspond à la norme de var
        return dist/self.number_repli


def fitness_for_plasmid(indiv, data):
    return Plasmid("", Plasmid.decodage(indiv), data[0], data[1], data[2]).getDistance()

def data_for_mutation(rot_tab, mutation_dispersion):
    mut_table = []
    for dinucleotide in Plasmid.important_dinucleotides :
        mut_table += [["gauss bounded", 2*rot_tab.getTwistVariance(dinucleotide), rot_tab.getTwist(dinucleotide), mutation_dispersion],\
                       ["gauss bounded", 2*rot_tab.getWedgeVariance(dinucleotide), rot_tab.getWedge(dinucleotide), mutation_dispersion]]
    return mut_table