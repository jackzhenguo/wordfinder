# This module mainly supports result models after executing train_model.py
# author: zhenguo
# data: 2021.2.25

class TResult(object):
    def __init__(self, word: str, pos_tag: str, sentence: str):
        """
        Construction function for result after training(train_model.py module)
        :param word: word
        :param tag: tag info
        :param sentence: sentence including this word
        """
        self.word = word
        self.pos_tag = pos_tag
        self.sentence = sentence


