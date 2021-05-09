# encoding: utf-8
"""
@file: metrics.py
@desc: evaluate clustering result
@author: group3
@time: 5/9/2021
"""
import numpy as np
from sklearn import metrics


class Evaluator(object):
    def __init__(self, sentence_vector):
        self.sentence_vector = sentence_vector

    def score(self, labels):
        """
        higher value means better cluster result
        """
        # only one cluster
        if labels.min() == labels.max():
            return 0.0
        # cluster count equals to len of X
        if len(np.unique(labels)) == len(self.sentence_vector):
            return 0.0
        return metrics.silhouette_score(self.sentence_vector, labels, metric='euclidean')
