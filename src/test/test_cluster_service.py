# encoding: utf-8
"""
@file: test_cluster_service.py
@desc:
@author: group3
@time: 2021/5/12
"""

from src.service.cluster_service import ClusterService
input_sentences = ['I eat the apple', 'Apple was eat by me', 'The apple was green']
cs = ClusterService("English", "apple")
cs.cluster_service(input_sentences, 2)
print("input sentences", end='\t')
print(input_sentences)
print("cluster_sentences ", end='\t')
print(cs.cluster_sentences)
print("cluster_sentences_succeed ", end='\t')
print(cs.cluster_sentences_succeed)
print("best_score ", end='\t')
print(cs.best_score)
print("cluster_best_labels ", end='\t')
print(cs.cluster_best_labels)
print("cluster_sentences_rmd ", end='\t')
print(cs.cluster_sentences_rmd)
