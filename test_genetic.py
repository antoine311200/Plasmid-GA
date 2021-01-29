from genetic import *
from plasmid import *

def fitness_function_sample(indiv):
    return -sum(indiv)


def test_genetic():
    data = {"selection_mode" : "elitist", "crossover_mode" : "normal",\
            "mutation_table" : [["randint", -1,1],["gauss bounded", 2, 3, 1]], "fitness_data" : None, "crossover_data" : [1]}

    gen = Genetic(2,10, np.array([[1,1], [2,2], [2,4]]), fitness_function_sample, data= data )

    gen.select()
    assert gen.current_parents[0][1] == 4
    gen.crossover()
    assert len(gen.current_offspring) == 1
    assert gen.current_offspring[0][0]==2
    assert gen.current_offspring[0][1] == 2 or gen.current_offspring[0][1] == 4
    gen.mutate()
    assert gen.current_offspring[0][0] in [3,1,2]
    assert gen.current_offspring[0][1]>=1 and gen.current_offspring[0][1]<=5


def test_decodage():
    indiv = [35.62, 7.2, 34.4, 1.1, 27.7, 8.4, 31.5, 2.6, 34.5, 3.5,33.67, 2.1,29.8, 6.7,36.9, 5.3,40, 5,36, 0.9]
    rot_t = Plasmid.decodage(indiv)
    assert rot_t.getDirection("CC") == -57
    assert rot_t.getTwist("TG") == 34.5
    assert rot_t.getWedge("GA") == 5.3

def test_dataForMutation():
    mut_tab = data_for_mutation(RotTable(), 1)
    assert len(mut_tab) == 20
    assert  len(mut_tab[0])== 4
    assert mut_tab[0][0]=="gauss bounded"

def test_encodage():
    plasmid = Plasmid("test")
    indiv = plasmid.encodage()
    assert indiv[3] == RotTable().getWedge("AC")
    assert len(indiv)==20


if __name__ =="__main__":
    test_encodage()
    test_dataForMutation()
    test_decodage()
    test_genetic()
