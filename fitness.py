from encodage import decodage

from Traj3D import *

indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]


dna_seq = "AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG"

def fitness_indiv(indiv, traj3D, dna_seq):
    traj3D.compute(dna_seq, decodage(indiv))
    lastVect = traj3D.getLastFromTraj()
    return(lastVect.dot(lastVect))


