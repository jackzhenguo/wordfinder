# util model
# user: zhenguo
# date: 2020.2.28

from typing import List


# TODO: keeping update
language_list = ['Chinese', 'English', 'French', 'Italian', 'Spanish', 'Korean', 'Russian', 'Portuguese']
language_dict = {'1': 'Chinese', '2': 'English', '3': 'French', '4': 'Italian',
                 '5': 'Spanish', '6': 'Korean', '7': 'Russian', '8': 'Portuguese'}

# database config
# cofig for local database
db_config = {'user': 'root',
             'password': 'root@123',
             'db_host': 'localhost',
             'db_name': 'psd_project'}

# language and corresponding file path of corpus
corpus_language = {'Chinese': 'input//corpus//result//zh.txt',
                   'English': 'input//corpus//result//wiki_en.txt',
                   'French': 'input//corpus//result//wiki_fr.txt',
                   'Italian': 'input//corpus//result//wiki_it.txt',
                   'Spanish': 'input//corpus//result//wiki_es.txt',
                   'Korean': 'input//corpus//result//wiki_ko.txt',
                   'Russian': 'input//corpus//result//wiki_ru.txt',
                   'Portuguese': 'input//corpus//result//wiki_pt.txt'}

udpipe_language = {'Chinese': 'input//udpipemodel//chinese-gsdsimp-ud-2.5-191206.udpipe',
                   'English': 'input//udpipemodel//english-ewt-ud-2.5-191206.udpipe',
                   'French': 'input//udpipemodel//french-gsd-ud-2.5-191206.udpipe',
                   'Italian': 'input//udpipemodel//italian-isdt-ud-2.5-191206.udpipe',
                   'Spanish': 'input//udpipemodel//spanish-gsd-ud-2.5-191206.udpipe',
                   'Korean': 'input//udpipemodel//korean-gsd-ud-2.5-191206.udpipe',
                   'Russian': 'input//udpipemodel//russian-gsd-ud-2.5-191206.udpipe',
                   'Portuguese': 'input//udpipemodel//portuguese-gsd-ud-2.5-191206.udpipe'}

word2vec_language = {'Chinese': 'input//word2vecmodel//gensim-word2vec-model-Chinese',
                     'English': 'input//word2vecmodel//gensim-word2vec-model-English',
                     'French': 'input//word2vecmodel//gensim-word2vec-model-French',
                     'Italian': 'input//word2vecmodel//gensim-word2vec-model-Italian',
                     'Spanish': 'input//word2vecmodel//gensim-word2vec-model-Spanish',
                     'Korean': 'input//word2vecmodel//gensim-word2vec-model-Korean',
                     'Russian': 'input//word2vecmodel//gensim-word2vec-model-Russian',
                     'Portuguese': 'input//word2vecmodel//gensim-word2vec-model-Portuguese'}


def get_keyword_window(sel_word: str, words_of_sentence: List, length=5) -> List[str]:
    """
    find the index of sel_word at sentence, then decide words of @length size
    by backward and forward of it.
    For example: I am very happy to this course of psd if sel_word is happy, then
    returning: [am, very, happy, to, this]

    if length is even, then returning [very, happy, to, this]

    remember: sel_word is lemmatized
    """
    if length <= 0:
        return words_of_sentence
    index = words_of_sentence.index(sel_word)
    if index == -1:
        return words_of_sentence
    # backward is not enough
    if index < length // 2:
        back_slice = words_of_sentence[:index]
        # forward is also not enough,
        # showing the sentence is too short compared to length parameter
        if (length - index) >= len(words_of_sentence):
            return words_of_sentence
        else:
            return back_slice + words_of_sentence[index: index + length - len(back_slice)]
    # forward is not enough
    if (index + length // 2) >= len(words_of_sentence):
        forward_slice = words_of_sentence[index:len(words_of_sentence)]
        # backward is also not enough,
        # showing the sentence is too short compared to length parameter
        if index - length <= 0:
            return words_of_sentence
        else:
            return words_of_sentence[index - (length - len(forward_slice)):index] + forward_slice

    return words_of_sentence[index - length // 2: index + length // 2 + 1] if length % 2 \
        else words_of_sentence[index - length // 2 + 1: index + length // 2 + 1]