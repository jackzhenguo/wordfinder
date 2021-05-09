# encoding: utf-8
"""
@file: clusters.py
@desc: This module is to evaluate cluster result
mainly based on an assumption that we don't know the
true labels of clusters.
@author: group3
@time: 4/2/2021
"""
from typing import List
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from src.feature.metrics import Evaluator


class ClusterSentences(object):
    def __init__(self, sentence_vector):
        self.sentence_vector = sentence_vector

    def kmeans_strategy(self, n_clusters: int):
        """
        kmeans cluster
        @param: n_clusters
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(self.sentence_vector)
        labels = kmeans.labels_
        return labels

    def agglomerative_strategy(self, n_clusters: int):
        """
        agglomerative cluster
        @param: n_clusters
        """
        best_score, best_labels = -1., None
        for metric in ["cosine", "euclidean", "cityblock"]:
            model = AgglomerativeClustering(n_clusters=n_clusters,
                                            linkage="average", affinity=metric)
            model.fit(self.sentence_vector)
            labels = model.labels_
            score = Evaluator(self.sentence_vector).score(labels)
            if best_score < score:
                best_score = score
                best_labels = labels

        return best_labels

    def cluster_default(self):
        """
        noise label is -1
        """
        db = DBSCAN(eps=0.3, min_samples=2).fit(self.sentence_vector)
        labels = db.labels_
        # if being more than half noise points
        noise_count = sum(1 for i in labels if i == -1)
        if len(self.sentence_vector) > 0 and noise_count / len(self.sentence_vector) >= 0.5:
            return None, None

        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_clusters_

    @staticmethod
    def group_cluster_result(sentences: List, labels: List):
        sents_dict = dict(zip(sentences, labels))
        sents_sorted = sorted(sentences, key=lambda sentence: sents_dict[sentence])
        corresp_labels = [sents_dict[sent] for sent in sents_sorted]
        return sents_sorted, corresp_labels
