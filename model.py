import gpt_2_simple as gpt2
from datetime import datetime


class Sess:
    def __init__(self):
        super(Sess, self).__init__()
        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess)