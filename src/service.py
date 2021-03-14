# This module provides service functionality to app.py
# working directory is src folder.

from collections import defaultdict
import json
from typing import List
import sys
import os

from src.train.result_model import TResult
from src.train.store import StoreData
from src.util import language_dict, language_list, db_config
from src.train.train_cluster import load_model

try:
    store_data = StoreData(db_config['user'],
                           db_config['password'],
                           db_host=db_config['db_host'],
                           db_name=db_config['db_name'])
    cnx = store_data.db_connect()
    cursor = cnx.cursor()
except Exception as ex:
    print('logging in database error %s' % ex)

POS_COLUMN_INDEX, SENTENCE_COLUMN_INDEX = 2, 6


class AppService(object):
    def __init__(self):
        self.pos_dict = None
        self.sel_result = None

    def find_service(self, language_name: str, sel_word: str):
        """This method get results from database by specified language_name and input word
        assgin value to self.pos_dict and self.sel_result
        :param language_name:
        :param sel_word:
        :return: None
        """
        # select
        sql_str = "select * from " + language_name + "_wordpos as w left join " + language_name + "_sentences as s on w.sentence = s.id where w.word = %s "
        try:
            cursor.execute(sql_str, (sel_word,))
            self.sel_result = cursor.fetchall()
            cnx.commit()
        except Exception as e:
            print(e)

        # convert to data structure following
        # sel_result = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
        #                ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]))
        self.pos_dict = defaultdict(list)
        for row in self.sel_result:
            pos_sentences = self.pos_dict[row[POS_COLUMN_INDEX]]
            if row[SENTENCE_COLUMN_INDEX] not in pos_sentences:
                pos_sentences.append(row[SENTENCE_COLUMN_INDEX])
        self.sel_result = [(sel_word, k, self.pos_dict[k]) for k in self.pos_dict]

    def cluster_sentences(self, language_name: str, sentences: List[str], n_cluster) -> List[str]:
        """
        cluster sentences to get examples
        :param language_name:
        :param sentences:
        :param n_cluster:
        :return:
        """
        pass



if __name__ == "__main__":
    # get word vector for one sentence
    language_name = 'English'
    sentences = ['Tohru shows great loyalty to whoever he stands by, even back to the time when he was an Enforcer for the Dark Hand.',
                 'The Earth Demon, Dai Gui resembles a large minotaur(with the face of a guardian lion) with great strength.',
                 'Al Mulock was the great-grandson of Sir William Mulock(1843–1944), the former Canadian Postmaster - General.',
                 'Though his surviving images are scarce, his importance to the early history of photography in Asia is great.']

    cluster_result = AppService().cluster_sentences(language_name, sentences, 2)
    print(cluster_result)