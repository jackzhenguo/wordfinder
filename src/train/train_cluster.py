# This module mainly solve the cluster question
# to get example sentences.
from gensim.test.utils import datapath
from gensim import utils
import gensim.models
import tempfile

from src.train.train_model import UdpipeTrain


class ClusterModel(object):
    def __init__(self, filename, udpipe_model: UdpipeTrain):
        self.filename = filename
        self.udpipe_model = udpipe_model

    def __iter__(self):
        corpus_path = datapath(self.filename)
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            # processed_line = utils.simple_preprocess(line)
            # processed_line = " ".join(processed_line)
            words = self.udpipe_model.word_segmentation(line)
            print(words)
            yield words


def train_model(language_name, corpus_path, udpipe_model: UdpipeTrain):
    """ train and save word2vec model
    :param udpipe_model:
    :param language_name:
    :param corpus_path:
    :return:
    """
    sentences = ClusterModel(corpus_path, udpipe_model)
    model = gensim.models.Word2Vec(sentences=sentences)
    model.save('/home/zglg/SLU/psd/cluster_pre_train/gensim-word2vec-model-' + language_name)
    print('save succeed')


def load_model(language_name) -> gensim.models.Word2Vec:
    """load model we have trained
    :param language_name:
    :return: word2vec model we have trained
    """
    filename = '/home/zglg/SLU/psd/cluster_pre_train/gensim-word2vec-model-' + language_name
    model = gensim.models.Word2Vec.load(filename)

    print('loadig succeed')
    for index, word in enumerate(model.wv.index2word):
        if index == 100:
            break
        vec = ",".join(map(lambda i: str(i), model.wv[word]))
        print(f"word #{index}/{len(model.wv.index2word)} is {word}, vec = {vec}")
    return model


if __name__ == "__main__":
    languange_name = 'Chinese'
    # first loading udpipe to segement word for each sentence
    udt_chinese = UdpipeTrain(languange_name,
                              '/home/zglg/SLU/psd/pre-model/chinese-gsdsimp-ud-2.5-191206.udpipe',
                              '/home/zglg/SLU/psd/corpus/chinese/平凡的世界.txt')

    train_model(languange_name, '/home/zglg/SLU/psd/corpus/chinese/平凡的世界.txt', udt_chinese)
    # After train, we can load model to use directly
    load_model(languange_name)




