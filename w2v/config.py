class Config(object):
    repeate_times = 6
    db_path = './w2v.pkl'
    vector_dimsensions = 8
    neg_sample_num = 10
    window_size = 3
    learning_rate = 0.05
    
    def rateChange(self,rate):
        self.learning_rate = rate
