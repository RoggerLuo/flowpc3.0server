import os
import numpy as np
import math
import random
from random import choice

culture = os.path.join(os.path.dirname(__file__),"culture.txt")
financial = os.path.join(os.path.dirname(__file__),"financial.txt")
military = os.path.join(os.path.dirname(__file__),"military.txt")
sports = os.path.join(os.path.dirname(__file__),"sports.txt")

def getRandomNegSamples():
    data = []
    notes = []
    with open(culture,'rb') as f: 
        data = data + f.readlines()
    with open(financial,'rb') as f: 
        data = data + f.readlines()
    with open(military,'rb') as f: 
        data = data + f.readlines()
    with open(sports,'rb') as f: 
        data = data + f.readlines()
    for i in range(1000):
        content = choice(data)
        try:
            content = content.decode('utf-8')[60:]
            le = len(content)
            start = random.randint(0,le)
            content = content[start:start+random.randint(60,200)]
            notes.append({'content':content})
        except Exception as e:
            print(e)    
    return notes
