import mathutils
import math

class RotTable:
    """Represents the rotation table"""

    __ORIGINAL_ROT_TABLE = {\
        "AA": [35.62, 7.2, -154,        0.06, 0.6, 0],\
        "AC": [34.4, 1.1, 143,          1.3, 5, 0],\
        "AG": [27.7, 8.4, 2,            1.5, 3, 0],\
        "AT": [31.5, 2.6, 0,            1.1, 2, 0],\
        "CA": [34.5, 3.5, -64,          0.9, 34, 0],\
        "CC": [33.67, 2.1, -57,         0.07, 2.1, 0],\
        "CG": [29.8, 6.7, 0,            1.1, 1.5, 0],\
        "CT": [27.7, 8.4, -2,           1.5, 3, 0],\
        "GA": [36.9, 5.3, 120,          0.9, 6, 0],\
        "GC": [40, 5, 180,              1.2, 1.275, 0],\
        "GG": [33.67, 2.1, 57,          0.07, 2.1, 0],\
        "GT": [34.4, 1.1, -143,         1.3, 5, 0],\
        "TA": [36, 0.9, 0,              1.1, 2, 0],\
        "TC": [36.9, 5.3, -120,         0.9, 6, 0],\
        "TG": [34.5, 3.5, 64,           0.9, 34, 0],\
        "TT": [35.62, 7.2, 154,         0.06, 0.6, 0]\
        }

    def __init__(self, rot_table=[]):
        self.__Rot_Table = {}
        i = 0
        for dinucleotide in RotTable.__ORIGINAL_ROT_TABLE:
            if rot_table != []:
                self.__Rot_Table[dinucleotide] = [rot_table[i],rot_table[i+1],RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][2]]
                i+=2
            else:
                self.__Rot_Table[dinucleotide] = RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][:3]
        # print(self.__Rot_Table)


    ###################
    # WRITING METHODS #
    ###################
    

    ###################
    # READING METHODS #
    ###################

    def getTwist(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][0]#RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][0]

    def getWedge(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][1]#RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][1]

    def getDirection(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][2]#RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][2]

    ###################

# original_sample = [
#     35.62, 7.2,
#     34.564, 1.1,
#     45627.7, 8.4,
#     31.5, 2.6,
#     34.5, 3.5,
#     33.4667, 2.1,
#     29.8, 6.7,
#     27.7, 8.4564,
#     36.9, 5.3,
#     40, 5,
#     33.67, 2.1,
#     34.4, 1.1,
#     36, 0.9,
#     36.9, 5456.3,
#     34.5, 3.465,
#     35.62, 7.2,
# ]
# RotTable(original_sample)
# RotTable()