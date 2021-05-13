# encoding: utf-8
"""
@file: cluster_service.py
@desc:
@author: group3
@time: 2021/5/12
"""
from typing import List

import numpy as np

from src.config import word2vec_language, udpipe_language, corpus_language
from src.feature.clusters import ClusterSentences
from src.feature.kwic import get_keyword_window2
from src.feature.metrics import Evaluator
from src.feature.postrain import UdpipeTrain
from src.feature.vector import load_model
from src.logs import Log

log = Log()


class ClusterService(object):
    def __init__(self, sel_language: str, sel_word: str):
        self.sel_language, self.sel_word = sel_language, sel_word

        self.udt_pre_model = UdpipeTrain(sel_language,
                                         udpipe_language[sel_language],
                                         corpus_language[sel_language])
        # first loading model
        self.word2vec_model = load_model(word2vec_language[self.sel_language])

        # example sentences after clustering
        self.cluster_sentences: List = None
        # recommend_sentences
        self.cluster_sentences_rmd: List = None
        # cluster labels
        self.cluster_best_labels: List = None
        # clustering succeed
        self.cluster_sentences_succeed: List = None
        # cluster score
        self.best_score = None

    def cluster_service(self, sentences: List[str], n_clusters: int) -> List[str]:
        """
        cluster sentences to get examples
        :param sentences: sentences
        :param n_clusters: number of clusters
        """
        no_n_input = False

        if n_clusters == '':
            n_clusters, no_n_input = 2, True

        n_clusters = int(n_clusters)
        if n_clusters <= 0:
            log.warning("cluster param n_clusters %d is invalid" % (n_clusters,))
            return False
        if n_clusters > len(sentences):
            log.warning('number of cluster %d bigger than sentences count %s' % (n_clusters, len(sentences)))
            return False

        if self.word2vec_model is None:
            log.warning("cannot find word2vec model of language %s " % self.sel_language)
            return False

        # second getting vectors for one sentence
        sent_vectors, failure_sentences = [], []
        for sent in sentences:
            words = self.udt_pre_model.word_segmentation(sent)
            # iterator to word
            # window_words = get_keyword_window(AppContext.sel_word, words, 5)
            window_words = get_keyword_window2(self.sel_language, self.sel_word, words, 5)
            word_vectors = [self.word2vec_model.wv[word.lower()] for word in window_words if
                            word.lower() in self.word2vec_model.wv]
            to_array = np.array(word_vectors)
            if len(to_array) == 0:
                failure_sentences.append(sent)
                log.warning('vector of very word in sentence %s not found ' % (sent,))
                continue
            sent_vectors.append(to_array.mean(axis=0).tolist())
        self.cluster_sentences_succeed = [sent for sent in sentences if sent not in failure_sentences]

        # third using kmeans to cluster
        cluster = ClusterSentences(sent_vectors)
        evaluator = Evaluator(sent_vectors)

        labels1 = cluster.kmeans_strategy(n_clusters)
        score1 = evaluator.score(labels1)

        labels2 = cluster.agglomerative_strategy(n_clusters)
        score2 = evaluator.score(labels2)

        # fourth select one sentence with each label
        scores = [(score1, labels1), (score2, labels2)]

        labels3, default_n_clusters = cluster.cluster_default()
        if labels3 is not None:
            score3 = evaluator.score(labels3)
            scores.append((score3, labels3))
            self.cluster_sentences_rmd = self._get_examples(self.cluster_sentences_succeed,
                                                            labels3, default_n_clusters)

        self.best_score, self.cluster_best_labels = max(scores, key=lambda v: v[0])

        # if default DBSCAN cluster algorithm is best
        if labels3 is not None and self.cluster_best_labels is labels3:
            self.cluster_sentences = self.cluster_sentences_rmd
        else:
            self.cluster_sentences = self._get_examples(self.cluster_sentences_succeed,
                                                        self.cluster_best_labels, n_clusters)

        if no_n_input:
            if labels3 is not None:
                self.cluster_sentences = self.cluster_sentences_rmd
            else:
                return False

        return True

    @staticmethod
    def _get_examples(sentences: List[str], labels, n_clusters: int):
        tmp_labels, examples, sentences_with_label = [], [], dict(zip(sentences, labels))
        for sent, label in sentences_with_label.items():
            if label not in tmp_labels:
                tmp_labels.append(label)
                examples.append(sent)
            if len(examples) == n_clusters:
                break
        # add bottom logic for cluster
        if len(examples) < n_clusters:
            for sent in sentences:
                if sent not in examples:
                    examples.append(sent)
                if len(examples) >= n_clusters:
                    break

        # group examples according to labels
        examples = sorted(examples, key=lambda sentence: sentences_with_label[sentence])
        return examples

    def group_sentences(self):
        sentences, labels = self.cluster_sentences_succeed, self.cluster_best_labels
        if len(sentences) != len(labels):
            log.warning('length of sentences %s not equaling labels %s' % (sentences, labels))
            return None
        return ClusterSentences.group_cluster_result(sentences, labels)
