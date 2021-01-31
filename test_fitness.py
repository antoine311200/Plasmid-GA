from fitness import *

target = [1,2,3,4,5,6,7,8,9]

sample = [2,4,1,5,3,8,1,9,5]

def test_squared_loss():
    print(Fitness.squared_loss(sample, target))

def test_absolute_loss():
    print(Fitness.absolute_loss(sample, target))

def test_hinge_loss():
    print(Fitness.hinge_loss(sample, target))

def test_logistic_loss():
    print(Fitness.logistic_loss(sample, target))

def test_cross_entropy_loss():
    print(Fitness.cross_entropy_loss(sample, target))

test_squared_loss()
test_absolute_loss()
test_hinge_loss()
test_logistic_loss()
test_cross_entropy_loss()