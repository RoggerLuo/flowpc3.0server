import numpy as np


class NegSampling(object):

    def __init__(self, config):
        self.config = config

    def train(self, c, t, n):
        step = self.config.learning_rate
        ___cost, ___c_grad, ___t_grad, ___n_grad = self.getGrad(c, t, n)
        c = c - ___c_grad * step
        t = t - ___t_grad * step
        for index in range(len(n)):
            neg = n[index]
            neg_grad = ___n_grad[index]
            neg = neg - neg_grad * step
            n[index] = neg  # 保险？
        return c, t, n, ___cost

    def getGrad(self, c, t, n):
        dotProduct = np.sum(t * c)
        ct_activ = self.sigmoid(dotProduct)
        
        ___cost = - np.log(ct_activ)        
        ___c_grad = self.calcGrad(ct_activ, t)
        ___t_grad = self.calcGrad(ct_activ, c)
        ___n_grad = []

        for neg in n:
            dotProduct = np.sum(neg * c)
            cn_activ = self.sigmoid(-dotProduct)

            ___cost -= np.log(cn_activ)  # cost 第二弹

            # centerword grad 第二弹
            ___c_grad -= self.calcGrad(cn_activ, neg)

            neg_grad = - self.calcGrad(cn_activ, c)
            ___n_grad.append(neg_grad)

        return ___cost, ___c_grad, ___t_grad, ___n_grad

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def calcGrad(self, activation, vector):
        deviation = activation - 1
        grad = deviation * vector
        return grad
