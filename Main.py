from RotTable import *
from Traj3D import *

# from genetic import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", help="input filename of DNA sequence")
parser.parse_args()
args = parser.parse_args()

def main():

    t = [   3.55080e+01,  7.12900e+00,  3.35560e+01,  9.28400e+00,  2.95870e+01,       
            8.67100e+00,  3.13770e+01,  3.93900e+00,  3.16420e+01, -1.13472e+02,
            3.36570e+01,  4.58400e+00,  2.85600e+01,  5.91800e+00,  2.74990e+01,
            5.30300e+00,  3.89990e+01, -1.13510e+01,  3.75360e+01,  2.87000e+00,
            3.36160e+01,  1.07000e+00,  3.30960e+01,  1.06000e-01,  3.71370e+01,
            2.99000e-01,  3.55210e+01, -2.10200e+00,  3.07820e+01, -1.26407e+02,
            3.56420e+01,  6.62200e+00]

    t = [
        35.63523,  7.65859, 35.61739, -1.95424, 26.99996,  6.11289, 32.56878,  4.53437,
        33.97872, 23.56189, 33.60168,  2.47102, 28.8904,   5.27788, 26.33274,  8.8519,
        36.99769,  8.57998, 39.90583,  5.59704, 33.68543,  3.89652, 33.80079, -3.61387,
        36.18033,  2.80521, 36.84558,  8.49777, 33.77856, 20.17643, 35.5756,  7.7045,
    ]

    t = [
        35.62099,   7.38758,  33.73401,   4.5026,   28.17119,   8.89446, 31.09185,
        1.73088,  34.70028, -15.92808,  33.73513,   1.38119,  29.56542,   5.29297,
        28.59094,   5.85735,  37.5411,    5.68214,  40.04789,   5.76726,  33.64255,
        3.34472,  34.68894,   3.33968,  35.04764,  -0.83569,  36.97577,   7.25949,
        34.91264,  26.28606,  35.67998,   6.79352
    ]

    rot_table = RotTable(t)
    traj = Traj3D()

    if args.filename:
	    # Read file
	    lineList = [line.rstrip('\n') for line in open("./resources/plasmid_180k.fasta")]
		# Formatting
	    seq = ''.join(lineList[1:])
	    traj.compute(seq, rot_table)
    else:
        traj.compute("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG", rot_table)

    #print(traj.getTraj())

    if args.filename:
        traj.draw(args.filename+".png")
    else:
        traj.draw("sample.png")


if __name__ == "__main__" :
    main()
