import numpy as np
from train.train import Train

class Task(object):

    def __init__(self,config):
        self.train = Train(config)
        self.config = config
        
    def save(self):
        self.train.save()

    def feedlist(self,wordlist):        
        cost = 0
        if len(wordlist) >= 2:
            for i in range(self.config.repeate_times):
                cost += self.train.wordlist(wordlist)
        return cost
        
    def basic(self, string):
        for i in range(self.config.repeate_times):
            cost = self.train.sentence_str(string)
            print(cost)
        self.train.save()

    def readTxtLine(self, line):
        if len(line) > 20 :
            self.basic(line)


