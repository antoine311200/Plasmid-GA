import sys

sys.path.append('../')

from . import plasmid

def test_plasmid():
    plsm = Plasmid('Escherichia coli strain', rotation_table=RotTable.__ORIGINAL_ROT_TABLE)
    plsm.load("../resources/plasmid_8k.py")