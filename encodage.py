from RotTable import *

important_dinucleotides = ["AA", "AC", "AG", "AT", "CA", "CC", "CG", "GA", "GC", "TA"]

symetricADN = {"A" : "T", "T" : "A",\
               "C" : "G", "G" : "C"}

def dataForMutation(rot_tab):
    minmaxList = []
    for dinucleotide in important_dinucleotides :
        minmaxList += [[rot_tab.getTwistVariance(dinucleotide), rot_tab.getWedgeVariance(dinucleotide)]]
    return minmaxList

def encodage(rot_tab): #rotTable -> floatlist
    individu = []
    for dinucleotide in important_dinucleotides :
        individu += [rot_tab.getTwist(dinucleotide), rot_tab.getWedge(dinucleotide)]
    return individu

def decodage(indiv): # float_list -> rotTable
    data = {}

    for i,dinucleotide in enumerate(important_dinucleotides) :
        data[dinucleotide] = indiv[2*i:2*(i+1)]
        data[getSymetric(dinucleotide)] = indiv[2*i:2*(i+1)]

    return RotTable(data)

def getSymetric(dinucleotide):
    sym = symetricADN[dinucleotide[1]] + symetricADN[dinucleotide[0]]
    return sym

