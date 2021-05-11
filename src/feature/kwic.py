# encoding: utf-8
"""
@file: kwic.py
@desc: providing functions about KWIC presentation
@author: group3
@time: 5/9/2021
"""

import re
from typing import List
from nltk.corpus import stopwords
from src.logs import Log

log = Log()


def get_keyword_window2(language_name: str, sel_word: str, words_of_sentence: List, length=5):
    """get_keyword_window function with removing stop words
    @param language_name: language name
    @param sel_word: refer to get_keyword_window function
    @param words_of_sentence:
    @param length:
    @return:
    """
    # remove numbers, special characters and stop words possible appearing in words_of_sentence
    try:
        stop_words = stopwords.words(language_name)
    except OSError as os:
        stop_words = []
    if stop_words is None:
        stop_words = []

    words_of_sentence2 = [word for word in words_of_sentence if not re.match(r'[\d\W\-\_]+', word.lower())]
    words_of_sentence2 = [word for word in words_of_sentence2 if word.lower() not in stop_words]
    return get_keyword_window(sel_word, words_of_sentence2, length)


def get_keyword_window(sel_word: str, words_of_sentence: List, length=5) -> List[str]:
    """
    find the index of sel_word at sentence, then decide words of @length size
    by backward and forward of it.
    For example: I am very happy to this course of psd if sel_word is happy, then
    returning: [am, very, happy, to, this]

    if length is even, then returning [very, happy, to, this]

    remember: sel_word being word root
    """
    if length <= 0 or len(words_of_sentence) <= length:
        return words_of_sentence
    index = -1
    for iw, word in enumerate(words_of_sentence):
        word = word.lower()
        if len(re.findall(sel_word.lower(), word)) > 0:
            index = iw
            break

    if index == -1:
        log.warning("warning: cannot find %s in sentence: %s" % (sel_word, words_of_sentence))
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


def kwic_show(sel_language, words_of_sentence, sel_word, window_size=9, align_param=70, token_space_param=1):
    """return kwic string for words_of_sentence and sel_word being key token
    :param sel_language: selected language
    :param words_of_sentence: all words in one sentence
    :param sel_word: key token
    :param window_size: size of kwic window
    :param align_param: parameters used to align the display
    :param token_space_param: space length before or after keyword

    window_size and align_param's default value is not suggested to revise
    """
    if window_size < 1:
        return None
    if window_size >= len(words_of_sentence):
        window_size = len(words_of_sentence)

    words_in_window = get_keyword_window2(sel_language, sel_word, words_of_sentence, window_size)

    sent = ' '.join(words_in_window)
    # TODO: better to use token after lemmatization to sel_word
    try:
        key_index = sent.lower().index(sel_word.lower())
    except ValueError as ve:
        # log.warning('%s not in sentence %s' % (sel_word, sent))
        key_index = -1
    if key_index == -1:
        return None, None

    align_param = align_param - len(sel_word) - 2 * token_space_param
    if align_param < 0:
        log.warning('align_param value required bigger length of input word')
        return None, None
    pre_part = sent[:key_index].rstrip()
    # dealing with the problem of too long string on the left side of keyword
    i, n_pre_words = 1, len(pre_part.split(' '))
    while i < n_pre_words and len(pre_part) > align_param // 2:
        pre_words = pre_part.split(' ')
        pre_words = pre_words[i:]
        pre_part = " ".join(pre_words)
        i += 1

    pre_kwic = pre_part.rjust(align_param // 2)
    key_kwic = token_space_param * ' ' + sent[key_index: key_index + len(sel_word)].lstrip() + token_space_param * ' '

    # dealing with the problem of too long string on the right side of keyword
    post_kwic = sent[key_index + len(sel_word):].lstrip()
    n_post_words = len(post_kwic.split(' '))
    i = n_post_words - 1
    while i > 0 and len(post_kwic) > align_param // 2:
        post_kwic_words = post_kwic.split(' ')
        post_kwic_words = post_kwic_words[:i]
        post_kwic = " ".join(post_kwic_words)
        i -= 1

    sel_word_kwic = pre_kwic + key_kwic + post_kwic
    return sel_word_kwic, pre_kwic
