from RotTable import *

important_dinucleotides = ["AA", "AC", "AG", "AT", "CA", "CC", "CG", "GA", "GC", "TA"]

symetricADN = {"A" : "T", "T" : "A",\
               "C" : "G", "G" : "C"}

def dataForMutation(rot_tab):
    mut_table = []
    for dinucleotide in important_dinucleotides :
        mut_table += [["gauss bounded", rot_tab.getTwistVariance(dinucleotide), rot_tab.getTwist(dinucleotide)],\
                       ["gauss bounded", rot_tab.getWedgeVariance(dinucleotide), rot_tab.getWedge(dinucleotide)]]
    return mut_table

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


def test_decodage():
    indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]
    rot_t = decodage(indiv)
    assert rot_t.getDirection("CC") == -57
    assert rot_t.getTwist("TG") == 34.5
    assert rot_t.getWedge("GA") == 5.3

def test_dataForMutation():
    mut_tab = dataForMutation(RotTable())
    assert len(mut_tab) == 20
    assert  len(mut_tab[0])== 3
    assert mut_tab[0][0]=="gauss bounded"

def test_encodage():
    rot_t = RotTable()
    indiv = encodage(rot_t)
    assert indiv[3] == rot_t.getWedge("AC")
    assert len(indiv)==20
