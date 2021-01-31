import math

class Fitness:

    @staticmethod
    def squared_loss(predict, real):
        loss = 0
        length = len(predict)
        if length != len(real):
            raise ValueError('real and predict arguments do not have the same length')
        for i in range(len(predict)):
            loss += (real[i]-predict[i])**2
        return loss/2
    
    @staticmethod
    def absolute_loss(predict, real):
        loss = 0
        length = len(predict)
        if length != len(real):
            raise ValueError('real and predict arguments do not have the same length')
        for i in range(len(predict)):
            loss += abs(real[i]-predict[i])
        return loss/2

        
    @staticmethod
    def hinge_loss(predict, real):
        loss = 0
        length = len(predict)
        if length != len(real):
            raise ValueError('real and predict arguments do not have the same length')
        for i in range(len(predict)):
            loss += max(0, 1-predict[i]*real[i])
        return loss
    
    
    @staticmethod
    def logistic_loss(predict, real):
        loss = 0
        length = len(predict)
        if length != len(real):
            raise ValueError('real and predict arguments do not have the same length')
        for i in range(len(predict)):
            loss += math.log(1+math.exp(-predict[i]*real[i]))
        return loss
    
    
    @staticmethod
    def cross_entropy_loss(predict, real):
        loss = 0
        length = len(predict)
        if length != len(real):
            raise ValueError('real and predict arguments do not have the same length')
        for i in range(len(predict)):
            if predict[i] > 0 and predict[i] < 1:
                loss += -real[i]*math.log(predict[i])-(1-predict[i])*math.log(1-predict[i])
            else:
                raise ValueError("predict must be between 0 and 1")
        return loss
    