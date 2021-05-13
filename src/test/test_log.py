# encoding: utf-8
"""
@file: test_log.py
@desc:
@author: group3
@time: 2021/5/12
"""
import traceback
from src.logs import Log

log = Log()

try:
    a = 1 / 0
except Exception as e:
    msg = traceback.format_exc()
    log.error(e.args[0])
