# from pkl import read
from pkl import read
import os
import numpy as np
def load_vocab():
    vocab_file = os.path.join(os.path.dirname(__file__),"vocab.pkl")
    pklData = read(vocab_file) # list ['我','是']
    vocab = {} 
    for idx, item in enumerate(pklData):
        vocab[item] = idx  # .strip()
    return vocab 

vocab = load_vocab()
embedding_file = os.path.join(os.path.dirname(__file__),"embeddings.pkl")
trainedEmbeddings = read(embedding_file) # 长度 4549 3个手工增加 3个预留

def str2embed(string):
    embeddingList = []
    for word in string:
        embedding = trainedEmbeddings[vocab.get(word,2)]
        embedding = np.array(embedding)
        embeddingList.append(embedding)
    return np.array(embeddingList)
