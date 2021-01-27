
from RotTable import *
from Traj3D import *

''' Class : Plasmide
This class is used for modelising a plasmide base on its sequence or the filename containing
its sequence
'''
class Plasmid:

    def __init__(self, signature, rotation_table=RotTable.__ORIGINAL_ROT_TABLE, sequence=[]):
        self.signature = signature
        self.sequence = sequence
        self.rotation_table = rotation_table
        self.trajectory = Traj3D()

    def load(self, filepath):
        self.filepath = filepath
        
        lineList = [line.rstrip('\n') for line in open(filepath)]
        self.sequence = ''.join(lineList[1:])

    def setRotationTable(rotation_table):
        self.rotation_table = rotation_table

    def setSequence(sequence):
        self.sequence = sequence

    def draw(self):
        self.trajectory.draw(self.signature)

    def compute(self):
        self.trajectory.compute(self.sequence, self.rotation_table)