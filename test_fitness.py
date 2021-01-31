from fitness import *

target = [1,2,3,4,5,6,7,8,9]
sample = [2,4,1,5,3,8,1,9,5]

target_entropy = [0.2,0.5,0.3,0.1,0.2]
sample_entropy = [0.1,0.8,0.4,0.1,0.5]

def test_squared_loss():
    assert Fitness.squared_loss(sample, target) == 35.5

def test_absolute_loss():
    assert Fitness.absolute_loss(sample, target) == 10.5

def test_hinge_loss():
    assert Fitness.hinge_loss(sample, target) == 0

def test_logistic_loss():
    assert Fitness.logistic_loss(sample, target) == 0.1767625434068119

def test_cross_entropy_loss():
    assert Fitness.cross_entropy_loss(sample_entropy, target_entropy) == 2.3804694344400286

test_squared_loss()
test_absolute_loss()
test_hinge_loss()
test_logistic_loss()
test_cross_entropy_loss()