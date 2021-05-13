# encoding: utf-8
"""
@file: store.py
@desc: This module is mainly used to store our feature result to database
at present this module supports storing for multiple languages.
use and refer interfaces between mysql and python by
https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
pymysql is the library for us to use between python and mysql
@author: group3
@time: 2/25/2021
"""

from __future__ import print_function
import pymysql
from typing import List
from src.feature.pos import TResult
from src.config import db_config, language_dict
from src.logs import Log

log = Log()


class DBStore(object):
    def __init__(self):
        """
        construct database configurations of mysql
        """
        self.DB_USER = db_config['user']
        self.DB_PWD = db_config['password']
        self.DB_HOST = db_config['db_host']
        self.DB_NAME = db_config['db_name']
        self.cnx, self.cursor = None, None

    def db_connect(self):
        """
        connect mysql and return connection object

        remember: should create connection as few as possible
        :return: connection to database object
        """
        try:
            if self.DB_NAME:
                self.cnx = pymysql.connect(user=self.DB_USER,
                                           password=self.DB_PWD,
                                           host=self.DB_HOST,
                                           database=self.DB_NAME, )
            else:
                self.cnx = pymysql.connect(user=self.DB_USER,
                                           password=self.DB_PWD,
                                           host=self.DB_HOST)
            self.cursor = self.cnx.cursor()
        except pymysql.connect.Error as err:
            log.error(err)
        log.info('connection to database succeed!')
        return self.cnx

    def create_database(self, cursor):
        """
        This method is mainly used to create mysql database
        :param cursor: cnx.cursor()
        :return:
        """
        try:
            if not self.DB_NAME:
                self.DB_NAME = db_config['db_name']
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
            log.info('database %s creation succeed' % self.DB_NAME)
        except pymysql.connect.Error as err:
            log.error("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self, tables: dict, tables_sentences: dict):
        if self.cursor.connection is None:
            self.cursor = self.cnx.cursor()

        try:
            self.cursor.execute("USE {}".format(self.DB_NAME))
        except pymysql.connect.Error as err:
            log.error(err)

        for table_name in tables:
            table_description = tables[table_name]
            try:
                log.info("Creating table {}: \n".format(table_name), end='')
                self.cursor.execute(table_description)
                log.info('table %s creation succeed\n' % table_name)
            except pymysql.connect.Error as err:
                log.error("Error occured creating tables coz of {}".format(err))

        for table_name in tables_sentences:
            table_description = tables_sentences[table_name]
            try:
                log.info("Creating table {}: \n".format(table_name), end='')
                self.cursor.execute(table_description)
                log.info('table %s creation succeed\n' % table_name)
            except pymysql.connect.Error as err:
                log.error("Error occured creating tables coz of {}".format(err))

        self.cursor.close()

    def insert_data(self, rows: List[TResult], language_name):
        """
        insert rows to table
        :param rows: results
        :param language_name
        :return: List[TResult]
        """
        if self.cursor.connection is None:
            self.cursor = self.cnx.cursor()

        add_sentence = ("INSERT INTO " + language_name + "_sentences "
                                                         "(sentence) "
                                                         "VALUES (%s)")
        add_words = ("INSERT INTO  " + language_name + "_wordpos "
                                                       "(word, pos_tag, sentence) "
                                                       "VALUES (%s, %s, %s)")
        try:
            # First insert sentence table for a specific language
            self.cursor.execute(add_sentence, rows[0].sentence)
            insert_sentence_id = self.cursor.lastrowid
            # Insert TResults at batch
            data = [(row.word, row.pos_tag, insert_sentence_id) for row in rows]
            self.cursor.executemany(add_words, data)
            self.cnx.commit()
            log.info('insert data succeed')
            self.cursor.close()
        except pymysql.connect.error as e:
            self.cnx.rollback()
            log.error('insert error %s' % (e,))

    def select_data(self, word, language):
        """
        This method is mainly used to select data from database
        by input word from web interface

        The returning result can be mapped to TResult
        :param word: word wanted to find
        :param language: word subjected to which language
        :return:
        """
        if self.cursor.connection is None:
            self.cursor = self.cnx.cursor()

        if self.cursor.connection is None:
            self.cursor = self.cnx.cursor()

        try:
            query = ("SELECT word, pos_tag, sentence FROM %s_wordpos "
                     "WHERE  word = %s") % (language, word)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.cursor.close()
            return rows
        except pymysql.connect.error as err:
            log.error("Query error due to {}".format(err))


if __name__ == '__main__':
    """The ddl script should be executed only once a time """
    TABLES = {}
    for language in language_dict.values():
        TABLES[language + '_wordpos'] = (
                                            "CREATE TABLE IF NOT EXISTS  `%s_wordpos` ("
                                            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
                                            "  `word` varchar(256) NOT NULL,"
                                            "  `pos_tag` varchar(64) NOT NULL,"
                                            "  `sentence` TEXT NOT NULL,"
                                            "  `create_time` timestamp NULL default CURRENT_TIMESTAMP,"
                                            "  PRIMARY KEY (`id`)"
                                            ") ENGINE=InnoDB") % (language,)

    TABLES_SENTENCES = {}
    for language in language_dict.values():
        TABLES_SENTENCES[language + '_sentences'] = (
                                                        "CREATE TABLE IF NOT EXISTS  `%s_sentences` ("
                                                        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
                                                        "  `sentence` TEXT NOT NULL,"
                                                        "  `create_time` timestamp NULL default CURRENT_TIMESTAMP,"
                                                        "  PRIMARY KEY (`id`)"
                                                        ") ENGINE=InnoDB") % (language,)

    # so in alpha version we should install mysql in local
    # put config info of database to db_config variable
    store_data = DBStore()
    conn = store_data.db_connect()
    store_data.create_database(conn.cursor())
    store_data.create_tables(conn.cursor(), TABLES, TABLES_SENTENCES)
    log.info('Done succeed~')
