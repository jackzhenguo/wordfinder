# encoding: utf-8
"""
@file: test_encryption.py
@desc:
@author: group3
@time: 2021/5/8
"""
import base64


def str_encryption(s):
    bs = base64.b64encode(s.encode("utf8"))
    decode = base64.b64decode(b'TGh4R3oxMDIyMzE=').decode("utf-8")
    return bs


if __name__ == '__main__':
    str_encryption('dsx')
