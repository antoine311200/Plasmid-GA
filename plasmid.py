import math

from RotTable import *
from Traj3D import *

''' Class : Plasmide
This class is used for modelising a plasmide base on its sequence or the filename containing
its sequence
'''


class Plasmid:
    important_dinucleotides = ["AA", "AC", "AG", "AT", "CA", "CC", "CG", "GA", "GC", "TA"]

    symetricADN = {"A" : "T", "T" : "A",\
               "C" : "G", "G" : "C"}

    @staticmethod
    def getSymetric(dinucleotide):
        sym = Plasmid.symetricADN[dinucleotide[1]] + Plasmid.symetricADN[dinucleotide[0]]
        return sym

    @staticmethod
    def decodage(indiv): # float_list -> rotTable
        data = {}

        for i,dinucleotide in enumerate(Plasmid.important_dinucleotides) :
            data[dinucleotide] = indiv[2*i:2*(i+1)]
            data[Plasmid.getSymetric(dinucleotide)] = indiv[2*i:2*(i+1)]

        return RotTable(data)

    def __init__(self, signature, rotation_table=RotTable(), trajectory=Traj3D(), sequence='AAAA'):
        self.signature = signature
        self.sequence = sequence
        self.rotation_table = rotation_table
        self.trajectory = trajectory
        self.compute()


    def load(self, filepath):
        self.filepath = filepath
        
        lineList = [line.rstrip('\n') for line in open(filepath)]
        self.sequence = ''.join(lineList[1:])
        self.sequence += self.sequence[:2]
        self.compute()

    def encodage(self): #rotTable -> floatlist
        individu = []
        for dinucleotide in Plasmid.important_dinucleotides :
            individu += [self.rotation_table.getTwist(dinucleotide), self.rotation_table.getWedge(dinucleotide)]
        return individu

    def setRotationTable(self, rotation_table):
        self.rotation_table = rotation_table

    def setSequence(self, sequence):
        self.sequence = sequence

    def draw(self):
        self.trajectory.draw(self.signature)

    def compute(self):
        self.trajectory.compute(self.sequence, self.rotation_table)

    def getDistance(self):
        last = self.trajectory.getIndexFromTraj(-1)
        second = self.trajectory.getIndexFromTraj(1)
        prelast = self.trajectory.getIndexFromTraj(-2)
        return math.sqrt(prelast.dot(prelast)) + math.sqrt((second-last).dot(second-last))

    def getAngle(self):
        pass