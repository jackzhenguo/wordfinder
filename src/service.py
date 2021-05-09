# encoding: utf-8
"""
@file: service.py
@desc: This module provides service functionalities to app.py
@author: group3
@time: 4/15/2021
"""

from typing import List, Dict
from collections import defaultdict
import numpy as np

from src.feature.postrain import UdpipeTrain
from src.feature.vector import load_model
from src.feature.store import StoreData
from src.feature.kwic import kwic_show, get_keyword_window, get_keyword_window2
from src.feature.clusters import ClusterSentences
from src.feature.metrics import Evaluator
from src.config import (language_list,
                        db_config,
                        corpus_language,
                        udpipe_language)
from src.logs import Log

POS_COLUMN_INDEX, SENTENCE_COLUMN_INDEX = 2, 6
log = Log()


class AppContext(object):
    """Encapsulate the context data of the current language and the currently selected word
    """
    # the language that customers selected
    sel_language: str = None

    # the word that customers input
    sel_word: str = None
    # select which Part of speech
    sel_word_pos: str = None

    # source of sentences
    sel_result_source: List = None

    # Sentences corresponding to the word that customers input
    # sel_result = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
    #                ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]
    sel_results: List = None

    # the word corresponding POS dict
    # sel_pos_dict = {"NOUN": ["Don't just leave your dirty plates in the sink!"],
    #                 "VERB": ["The wheels, started to sink into the mud.", "How could you sink so low?"]
    #                }
    sel_word_pos_dict: Dict = None

    # KWIC of sentences corresponding to the word that customers input
    sentence_kwic: List = None

    # udpipe model to segment word for each sentence
    udt_pre_model = None

    # example sentences after clustering
    cluster_sentences: List = None
    # recommend_sentences
    cluster_sentences_rmd: List = None
    # cluster labels
    cluster_best_labels: List = None
    # clustering succeed
    cluster_sentences_succeed: List = None
    # cluster score
    best_score = None

    # the connection object of the database
    db_conn = None


class AppService(object):
    def __init__(self):
        try:
            store_data = StoreData(db_config['user'],
                                   db_config['password'],
                                   db_host=db_config['db_host'],
                                   db_name=db_config['db_name'])
            AppContext.db_conn = store_data.db_connect()
        except Exception as ex:
            log.error('database link error %s' % (ex,))

    def config_udpipe(self, language_name, db_conn=None):
        """config udpipe"""
        # first loading udpipe to segment word for each sentence
        # all these need to be at preprocessed level
        AppContext.udt_pre_model = UdpipeTrain(language_name,
                                               udpipe_language[language_name],
                                               corpus_language[language_name],
                                               db_conn)
        return self

    @staticmethod
    def find_service(language_name: str, sel_word: str):
        """This method get results from database by specified language_name and input word
        assign value to self.pos_dict and self.sel_result
        :param language_name:
        :param sel_word:
        :return: None
        """
        # select
        sql_str = "select * from " + language_name + "_wordpos as w left join " + language_name + "_sentences as s on " \
                                                                                                  "w.sentence = s.id " \
                                                                                                  "where w.word = %s "
        try:
            cursor = AppContext.db_conn.cursor()
            cursor.execute(sql_str, (sel_word,))
            AppContext.sel_result_source = cursor.fetchall()
            AppContext.db_conn.commit()
        except Exception as e:
            log.error(e)
        if AppContext.sel_result_source is None:
            log.warning('language %s word %s not found in database' % (AppContext.sel_language, AppContext.sel_word))
            return None
        # convert to data structure following
        # sel_result = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
        #                ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]))
        AppContext.sel_word_pos_dict = defaultdict(list)
        for row in AppContext.sel_result_source:
            pos_sentences = AppContext.sel_word_pos_dict[row[POS_COLUMN_INDEX]]
            if row[SENTENCE_COLUMN_INDEX] not in pos_sentences:
                pos_sentences.append(row[SENTENCE_COLUMN_INDEX])
        AppContext.sel_results = [(sel_word, k, AppContext.sel_word_pos_dict[k]) for k in AppContext.sel_word_pos_dict]

    def cluster_service(self, save_path: str, sentences: List[str], n_clusters: int) -> List[str]:
        """
        cluster sentences to get examples
        :param save_path: the saved path for our word vector model
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
        if len(AppContext.sel_result_source) <= 0:
            log.warning('no sentence')
            return False

        # first loading model
        word2vec_model = load_model(save_path)
        if word2vec_model is None:
            return False

        # second getting vectors for one sentence
        sent_vectors, failure_sentences = [], []
        for sent in sentences:
            words = AppContext.udt_pre_model.word_segmentation(sent)
            # iterator to word
            # window_words = get_keyword_window(AppContext.sel_word, words, 5)
            window_words = get_keyword_window2(AppContext.sel_language, AppContext.sel_word, words, 5)
            word_vectors = [word2vec_model.wv[word.lower()] for word in window_words if word.lower() in word2vec_model.wv]
            to_array = np.array(word_vectors)
            if len(to_array) == 0:
                failure_sentences.append(sent)
                log.warning('vector of very word in sentence %s not found ' % (sent, ))
                continue
            sent_vectors.append(to_array.mean(axis=0).tolist())
        AppContext.cluster_sentences_succeed = [sent for sent in sentences if sent not in failure_sentences]

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
            AppContext.cluster_sentences_rmd = self._get_examples(AppContext.cluster_sentences_succeed,
                                                                  labels3, default_n_clusters)

        AppContext.best_score, AppContext.cluster_best_labels = max(scores, key=lambda v: v[0])

        # if default DBSCAN cluster algorithm is best
        if labels3 is not None and AppContext.cluster_best_labels is labels3:
            AppContext.cluster_sentences = AppContext.cluster_sentences_rmd
        else:
            AppContext.cluster_sentences = self._get_examples(AppContext.cluster_sentences_succeed,
                                                              AppContext.cluster_best_labels, n_clusters)

        if no_n_input:
            if labels3 is not None:
                AppContext.cluster_sentences = AppContext.cluster_sentences_rmd
            else:
                return False

        return True

    @staticmethod
    def kwic(sel_word: str, sentence_with_pos: List):
        """
        :param: sel_word
        :param: sentenceWithPOS

        sentence_with_pos examples:
        [("NOUN", "bank", ["I go to the bank", "The house lies the right of the river bank"]),
        ("VERB", "bank", ["I banked in a slot"])
        """
        result = []
        for sentTuple in sentence_with_pos:
            sents_kwic, tmp_pre_kwic = [], []
            sents_origin = sentTuple[2]
            for sent in sents_origin:
                words = AppContext.udt_pre_model.word_segmentation(sent)
                result_text, pre_kwic = kwic_show(AppContext.sel_language, words, sel_word, window_size=9, token_space_param=2)
                if result_text:
                    sents_kwic.append(result_text)
                    tmp_pre_kwic.append(pre_kwic)

            tmp_dict = dict(zip(sents_kwic, tmp_pre_kwic))
            # first sort by size of words of pre part
            sents_kwic_sorted = sorted(sents_kwic, key=lambda res: len(tmp_dict[res].strip().split(' ')))
            # second sort by length of pre part
            sents_kwic_sorted = sorted(sents_kwic_sorted, key=lambda res: len(''.join(tmp_dict[res].strip())))
            result.append((sentTuple[0], sentTuple[1], sentTuple[2], sents_kwic_sorted))

        AppContext.sentence_kwic = result

        return result

    @staticmethod
    def group_sentences():
        sentences, labels = AppContext.cluster_sentences_succeed, AppContext.cluster_best_labels
        if len(sentences) != len(labels):
            log.warning('length of sentences %s not equaling labels %s' % (sentences, labels))
            return None
        return ClusterSentences.group_cluster_result(sentences, labels)

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
