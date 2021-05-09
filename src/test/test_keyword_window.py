from typing import List
from src.feature.kwic import get_keyword_window


if __name__ == '__main__':
    words = ['I', 'am', 'very', 'happy', 'to', 'this', 'course', 'of', 'psd']

    res = get_keyword_window('happy', words, length=5)
    assert res == ['am', 'very', 'happy', 'to', 'this']
    res = get_keyword_window('to', words, length=4)
    assert res == ['happy', 'to', 'this', 'course']
    res = get_keyword_window('am', words, length=5)
    assert res == ['I', 'am', 'very', 'happy', 'to']
    res = get_keyword_window('of', words, length=5)
    assert res == ['to', 'this', 'course', 'of', 'psd']
    res = get_keyword_window('I', words, length=5)
    assert res == ['I', 'am', 'very', 'happy', 'to']
    res = get_keyword_window('am', words, length=5)
    assert res == ['I', 'am', 'very', 'happy', 'to']
    res = get_keyword_window('am', words, length=8)
    assert res == ['I', 'am', 'very', 'happy', 'to', 'this', 'course', 'of']
    res = get_keyword_window('am', words, length=9)
    assert res == words
    res = get_keyword_window('am', words, length=10)
    assert res == words
    res = get_keyword_window('psd', words, length=5)
    assert res == ['to', 'this', 'course', 'of', 'psd']
    res = get_keyword_window('psd', words, length=1)
    assert res == ['psd']
    res = get_keyword_window('psd', words, length=10)
    assert res == words
    res = get_keyword_window('psd', words, length=0)
    assert res == words
