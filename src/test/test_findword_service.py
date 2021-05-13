# encoding: utf-8
"""
@file: test_findword_service.py
@desc:
@author: group3
@time: 2021/5/12
"""
from src.service.find_service import FindWordService

if __name__ == '__main__':

    fws = FindWordService()
    fws.find_word('English', 'bank')
    print(fws.sel_results)

    fws.find_word('Chinese', '银行')
    print(fws.sel_results)

    fws.find_word('French', 'Banque')
    print(fws.sel_results)

    fws.find_word('Italian', 'banca')
    print(fws.sel_results)

    fws.find_word('Spanish', 'Banco')
    print(fws.sel_results)

    fws.find_word('Korean', '은행')
    print(fws.sel_results)

    fws.find_word('Russian', 'банк')
    print(fws.sel_results)

    fws.find_word('Portuguese', 'Banco')
    print(fws.sel_results)



