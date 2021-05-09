# encoding: utf-8
"""
@file: test_kwic_show.py
@desc:
@author: group3
@time: 5/3/2021
"""
from src.feature.kwic import kwic_show

if __name__ == '__main__':
    words = ['I', 'am', 'very', 'happy', 'to', 'this', 'course', 'of', 'psd']

    print(kwic_show(words, 'I', window_size=1))
    print(kwic_show(words, 'I', window_size=5))

    print(kwic_show(words, 'very', token_space_param=5))
    print(kwic_show(words, 'very', window_size=6, token_space_param=5))
    print(kwic_show(words, 'very', window_size=1, token_space_param=5))

    print(kwic_show(words, 'stem', align_param=20))
    print(kwic_show(words, 'stem', align_param=100))

    # test boundary
    print(kwic_show(words, 'II', window_size=1))
    print(kwic_show(words, 'related', window_size=10000))



