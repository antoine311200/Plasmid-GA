#For computing
import mathutils
import math

#For drawing
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import collections  as mc


class Traj3D:
    """Represents a 3D trajectory"""

    # Vertical translation (elevation) between two di-nucleotides
    __MATRIX_T = mathutils.Matrix.Translation((0.0, 0.0, 3.38/2.0, 1.0))

    def __init__(self):
        self.__Traj3D = {}

    def getTraj(self):
        return self.__Traj3D

    def compute(self, dna_seq, rot_table):

        # Matrice cumulant l'ensemble des transformations géométriques engendrées par la séquence d'ADN
        total_matrix = mathutils.Matrix()

        # On enregistre la position du premier nucléotide
        self.__Traj3D = [mathutils.Vector((0.0, 0.0, 0.0, 1.0))]

        matrices_Rz = {}
        matrices_Q = {}
        # On parcourt la sequence, nucléotide par nucléotide
        for i in range(1, len(dna_seq)):
            # On lit le dinucleotide courant
            dinucleotide = dna_seq[i-1]+dna_seq[i]
            # On remplit au fur et à mesure les matrices de rotation
            if dinucleotide not in matrices_Rz:
                matrices_Rz[dinucleotide] = mathutils.Matrix.Rotation(math.radians(rot_table.getTwist(dinucleotide)/2), 4, 'Z')
                matrices_Q[dinucleotide] = \
                    mathutils.Matrix.Rotation(math.radians((rot_table.getDirection(dinucleotide)-90)), 4, 'Z') \
                    @ mathutils.Matrix.Rotation(math.radians((-rot_table.getWedge(dinucleotide))), 4, 'X') \
                    @ mathutils.Matrix.Rotation(math.radians((90-rot_table.getDirection(dinucleotide))), 4, 'Z')


            # On calcule les transformations géométrique selon le dinucleotide courant, et on les ajoute à la matrice totale
            total_matrix =  total_matrix @ \
                self.__MATRIX_T \
                @ matrices_Rz[dinucleotide] \
                @ matrices_Q[dinucleotide] \
                @ matrices_Rz[dinucleotide] @ \
                self.__MATRIX_T

            # On calcule la position du nucléotide courant en appliquant toutes les transformations géométriques à la position du premier nucléotide
            self.__Traj3D.append(total_matrix @ self.__Traj3D[0])


    def draw(self, filename):
        xyz = np.array(self.__Traj3D)
        self.__Traj3D = []
        x, y, z = xyz[:,0], xyz[:,1], xyz[:,2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x,y,z)
        plt.show()
        plt.savefig(filename)
