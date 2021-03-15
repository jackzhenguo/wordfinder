# this module is mainly used to train our corpus
# according to UDpipe pre-train modules

# third-party modules
from corpy.udpipe import Model
from corpy.udpipe import pprint
from typing import List
import re
# we define modules
from src.train.base_model import ITrain
from src.train.result_model import TResult
from src.train.store import StoreData
from src.util import language_list, db_config


class UdpipeTrain(ITrain):
    def __init__(self, language_name, pre_model_name, our_corpus_name):
        """

        The language of pre_model_name and our_corpus_name should be identical!
        :param language_name:
        :param pre_model_name: it's from udpipe
        :param our_corpus_name: it's our found
        """
        self.language_name = language_name
        self.pre_model_name = pre_model_name
        self.our_corpus_name = our_corpus_name
        try:
            self.store_data = StoreData(db_config['user'],
                                        db_config['password'],
                                        db_host=db_config['db_host'],
                                        db_name=db_config['db_name'])
            self.cursor = self.store_data.db_connect().cursor()

            # second loading udpipe pre-train model
            self.model = Model(self.pre_model_name)

        except Exception as ex:
            print('logging in database error %s' % ex)

    def load_data(self) -> str:
        with open(self.our_corpus_name, 'r') as f:
            for sen in f:
                print('loading one sentence: %s' % (sen,))
                yield sen

        print('loading done for our corpus')

    def clean_data(self, data: str) -> str:
        """
        data is one or several sentence(s) we expect

        if data is \n, \t, empty str, etc, replace them

        :param data: raw data
        :return: data after cleaning
        """
        cleaned_data = re.sub('[\n\t]+', '', data)
        return cleaned_data

    def do_train(self) -> List[TResult]:
        """
        By pre-train modules of unpipe get the results for our corpus
        These udpipe modules can be download here:
        https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131
        :return:
        """
        # train our corpus to get POS for each word
        line_no = 1
        for sen in self.load_data():
            # if line_no < 1811:
            #     line_no += 1
            #     continue
            sen_clean = self.clean_data(sen)
            if not sen_clean:
                continue
            word_pos = list(self.model.process(sen_clean))
            # pprint(word_pos)
            for i, one_sentence in enumerate(word_pos):
                sentence_text = self.extract_one_sentence(one_sentence)
                results = self.extract_one_word(one_sentence, sentence_text)
                self.store_data.insert_data(self.cursor, results, self.language_name)
                print('line %d, batch %d for %s written succeed' % (line_no, i, self.language_name))
            line_no += 1
        print(' all written succeed for corpus of %s' % self.our_corpus_name)

    def extract_one_sentence(self, sentence) -> str:
        """
       This private method is mainly used to extract the sentence text.
       an instance of udpipe Sentence:
       Sentence(
           comments=[
             '# sent_id = 3',
             '# text = 黄土高原严寒而漫长的冬天看来就要过去，但那真正温暖的春天还远远地没有到来。'],
           words=[
             Word(id=0, <root>),
             Word(id=1,
                  form='黄土',
                  lemma='黄土',
                  xpostag='NNP',
                  upostag='PROPN',
                  head=3,
                  deprel='nmod',
                  misc='SpaceAfter=No'),
             Word(id=2,
                  form='高原',
                  lemma='高原',
                  xpostag='NN',
                  upostag='NOUN',
                  head=3,
                  deprel='nmod',
                  misc='SpaceAfter=No'),
             Word(id=3,
                  form='严寒',
                  lemma='严寒',
                  xpostag='NN',
                  upostag='NOUN',
                  head=22,
                  deprel='nsubj',
                  misc='SpaceAfter=No'),
             
             omited by myself ])
       
       :param sentence: udpipe Sentence
       :return: str 黄土高原严寒而漫长的冬天看来就要过去，但那真正温暖的春天还远远地没有到来。
       """
        comment = ''.join(sentence.comments)
        try:
            cs = re.findall(r'text = (.*)', comment)[0]
            return cs
        except Exception as e:
            # TODO: need to write warning log
            print('error: not find a sentence', e)
            return ''

    def extract_one_word(self, sentence, sentence_text: str) -> [TResult]:
        """
        This private method is mainly used to extract one word and it's POS

        :param sentence_text:
        :param sentence:
        :return: [TResult]
        """
        r = []
        for word in sentence.words:
            if word.lemma and word.lemma not in ITrain.FILTER_WORD:
                if word.lemma and word.upostag and sentence_text:
                    r.append(TResult(word.lemma, word.upostag, sentence_text))
        return r

    def word_segmentation(self, sentence) -> List[str]:
        """
        :param sentence:
        :return: word list
        """
        sen_clean = self.clean_data(sentence)
        if not sen_clean:
            return []
        word_pos = list(self.model.process(sen_clean))
        words = []
        for i, one_sentence in enumerate(word_pos):
            sentence_text = self.extract_one_sentence(one_sentence)
            results = self.extract_one_word(one_sentence, sentence_text)
            words.extend([res.word for res in results])
        return words


if __name__ == '__main__':
    # Chinese
    # have done
    udt_chinese = UdpipeTrain(language_list[0],
                             # need to start using different file paths 
                             # or just checking for file in directory
                              '/home/zglg/SLU/psd/pre-model/chinese-gsdsimp-ud-2.5-191206.udpipe', 
                              '/home/zglg/SLU/psd/corpus/chinese/平凡的世界.txt')

    # English
    # train to wiki_en.txt line 15539, batch 0 for English written succeed
    udt_english = UdpipeTrain(language_list[1],
                              '/home/zglg/SLU/psd/pre-model/english-ewt-ud-2.5-191206.udpipe',
                              '/home/zglg/SLU/psd/corpus/english/wiki_en.txt')

    # French
    udt_english.do_train()
