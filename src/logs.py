# encoding: utf-8
"""
@file: logs.py
@desc: log module
@author: group3
@time: 2/26/2021
"""

import logging
import time
import os


class Log:
    def __init__(self):
        # log path
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        log_path = os.path.join(root_path, 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        self.now = time.strftime("%Y-%m-%d")
        self.log_name = os.path.join(log_path, '{0}.log'.format(self.now))

    def __print_console(self, level, message):
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # create handler to write log files
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # create another handler to write console interface
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # define output format of handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)
        logger.addHandler(ch)
        # log
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        # remove handler after logging
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # close file
        fh.close()

    def debug(self, message):
        self.__print_console('debug', message)

    def info(self, message):
        self.__print_console('info', message)

    def warning(self, message):
        self.__print_console('warning', message)

    def error(self, message):
        self.__print_console('error', message)
