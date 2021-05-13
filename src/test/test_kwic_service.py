# encoding: utf-8
"""
@file: test_kwic_service.py
@desc:
@author: group3
@time: 2021/5/12
"""
from src.service.kwic_service import KWICService

if __name__ == "__main__":
    s = [("NOUN", "bank", ["I go to the bank", "The house lies the right of the river bank"]),
         ("VERB", "bank", ["I banked in a slot"])]

    res = KWICService('English').kwic('bank', s)
    print(res)
