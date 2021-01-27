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

    rot_table = RotTable()
    traj = Traj3D()

    if args.filename:
	    # Read file
	    lineList = [line.rstrip('\n') for line in open("./resources/plasmid_8k.fasta")]
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
