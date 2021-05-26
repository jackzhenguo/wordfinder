# encoding: utf-8
"""
@file: find_service.py
@desc:
@author: group3
@time: 2021/5/12
"""
from collections import defaultdict
from typing import List, Dict

from src.feature.store import DBStore
from src.logs import Log

log = Log()


class FindWordService(object):
    def __init__(self):
        try:
            self.db_conn = DBStore().db_connect()

            # source of sentences
            self.sel_result_source: List = None

            # Sentences corresponding to the word that customers input
            # sel_result = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
            #                ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]
            self.sel_results: List = None

            # the word corresponding POS dict
            # sel_pos_dict = {"NOUN": ["Don't just leave your dirty plates in the sink!"],
            #                 "VERB": ["The wheels, started to sink into the mud.", "How could you sink so low?"]
            #                }
            self.sel_word_pos_dict: Dict = None
        except Exception as e:
            log.error(e.args[0])

    def find_word(self, language_name: str, sel_word: str):
        """This method get results from database by specified language_name and input word
        assign value to self.pos_dict and self.sel_result
        :param language_name:
        :param sel_word:
        :return: executing okay return True, orFalse
        """
        pos_column_index, sentence_column_index = 2, 6

        # select
        sql_str = "select * from " + language_name + \
                  "_wordpos as w left join " + language_name + \
                  "_sentences as s on " \
                  "w.sentence = s.id " \
                  "where w.word = %s limit 30"
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(sql_str, (sel_word,))
            self.sel_result_source = cursor.fetchall()
            self.db_conn.commit()
            cursor.close()
            if self.sel_result_source is None or len(self.sel_result_source) == 0:
                log.warning('word %s in %s not found in database' % (sel_word, language_name))
                return False
            # convert to data structure following
            # sel_result = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
            #                ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]))
            self.sel_word_pos_dict = defaultdict(list)
            for row in self.sel_result_source:
                pos_sentences = self.sel_word_pos_dict[row[pos_column_index]]
                if row[sentence_column_index] not in pos_sentences:
                    pos_sentences.append(row[sentence_column_index])
            self.sel_results = [(sel_word, k, self.sel_word_pos_dict[k]) for k in self.sel_word_pos_dict]
            return True
        except Exception as e:
            log.error(e.args[0])
