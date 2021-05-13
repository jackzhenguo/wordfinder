# encoding: utf-8
"""
@file: kwic_service.py
@desc:
@author: group3
@time: 2021/5/12
"""
from typing import List

from src.config import udpipe_language, corpus_language
from src.feature.kwic import kwic_show
from src.feature.postrain import UdpipeTrain


class KWICService(object):
    def __init__(self, sel_language: str):
        self.sel_language = sel_language
        self.udt_pre_model = UdpipeTrain(sel_language,
                                         udpipe_language[sel_language],
                                         corpus_language[sel_language])

    def kwic(self, sel_word: str, sentences_with_pos: List):
        """
        :param: sel_word
        :param: sentenceWithPOS

        sentence_with_pos examples:
        [("NOUN", "bank", ["I go to the bank", "The house lies the right of the river bank"]),
        ("VERB", "bank", ["I banked in a slot"])

        :@return: [('NOUN', 'bank', ['I go to the bank', 'The house lies the right of the river bank'], ['                             go  bank  ', '          house lie right river  bank  ']),
        ('VERB', 'bank', ['I banked in a slot'], ['                                 bank  slot'])]
        """

        result = []
        for sentTuple in sentences_with_pos:
            sents_kwic, tmp_pre_kwic = [], []
            sents_origin = sentTuple[2]
            for sent in sents_origin:
                words = self.udt_pre_model.word_segmentation(sent)
                result_text, pre_kwic = kwic_show(self.sel_language,
                                                  words,
                                                  sel_word,
                                                  window_size=9,
                                                  token_space_param=2)
                if result_text:
                    sents_kwic.append(result_text)
                    tmp_pre_kwic.append(pre_kwic)

            tmp_dict = dict(zip(sents_kwic, tmp_pre_kwic))
            # first sort by size of words of pre part
            sents_kwic_sorted = sorted(sents_kwic, key=lambda res: len(tmp_dict[res].strip().split(' ')))
            # second sort by length of pre part
            sents_kwic_sorted = sorted(sents_kwic_sorted, key=lambda res: len(''.join(tmp_dict[res].strip())))
            result.append((sentTuple[0], sentTuple[1], sentTuple[2], sents_kwic_sorted))

        return result
