from genetic import *


def fitness_function_sample(indiv):
    return -sum(indiv)


def test_genetic():
    data = {"selection_mode" : "elitist", "crossover_mode" : "normal",\
            "mutation_table" : [["randint", -1,1],["gauss bounded", 2, 3]], "fitness_data" : None, "crossover_data" : [1]}

    gen = Genetic(2,10, np.array([[1,1], [2,2], [2,4]]), fitness_function_sample, data= data )

    gen.select()
    print(gen.current_parents)
    assert gen.current_parents[0][1] == 4
    gen.crossover()
    assert len(gen.current_offspring) == 1
    assert gen.current_offspring[0][0]==2
    assert gen.current_offspring[0][1] == 2 or gen.current_offspring[0][1] == 4
    gen.mutate()
    print(gen.current_offspring[0][1])
    assert gen.current_offspring[0][0] in [3,1,2]
    assert gen.current_offspring[0][1]>=1 and gen.current_offspring[0][1]<=5

test_genetic()