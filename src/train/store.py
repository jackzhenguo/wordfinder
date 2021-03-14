# This module is mainly used to store our train result to database
# at present this module supports storing for multiple languages.
# use and refer interfaces between mysql and python by
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

from __future__ import print_function
import pymysql
from typing import List

# import modules we define
from wordfinder.src.train.result_model import TResult
from wordfinder.src.util import db_config
from wordfinder.src.util import language_dict


class StoreData(object):
    def __init__(self, db_user, db_pwd, db_host, db_name):
        """
        construct databse configurations of mysql
        :param db_user:
        :param db_pwd:
        :param db_host:
        :param db_name:
        """
        self.DB_USER = db_user
        self.DB_PWD = db_pwd
        self.DB_HOST = db_host
        self.DB_NAME = db_name
        self.cnx = None

    def db_connect(self):
        """
        connect mysql and return connection object

        remember: should create connection as few as possible
        :return: connection to databse object
        """
        try:
            if self.DB_NAME:
                self.cnx = pymysql.connect(user=self.DB_USER, password=self.DB_PWD,
                                           host=self.DB_HOST,
                                           database=self.DB_NAME,
                                           connect_timeout=31536000)
            else:
                self.cnx = pymysql.connect(user=self.DB_USER, password=self.DB_PWD,
                                           host=self.DB_HOST,
                                           connect_timeout=31536000)
        except pymysql.connect.Error as err:
            print(err)
        print('connection succeed!')
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
            print('database %s creation succeed' % self.DB_NAME)
        except pymysql.connect.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self, cursor, tables: dict, tables_senteces: dict):
        TABLES, TABLES_SETENCES = tables, tables_senteces
        try:
            cursor.execute("USE {}".format(self.DB_NAME))
        except pymysql.connect.Error as err:
            print(error)

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: \n".format(table_name), end='')
                cursor.execute(table_description)
                print('table %s creation succeed\n' % table_name)
            except pymysql.connect.Error as err:
                print(err)

        for table_name in TABLES_SETENCES:
            table_description = TABLES_SETENCES[table_name]
            try:
                print("Creating table {}: \n".format(table_name), end='')
                cursor.execute(table_description)
                print('table %s creation succeed\n' % table_name)
            except pymysql.connect.Error as err:
                print(err)

        cursor.close()

    def insert_data(self, cursor, rows: List[TResult], language_name):
        """
        insert rows to table
        :param cursor
        :param rows: results
        :param language_name
        :return: List[TResult]
        """
        add_sentence = ("INSERT INTO " + language_name + "_sentences "
                        "(sentence) " 
                        "VALUES (%s)")
        add_words = ("INSERT INTO  " + language_name + "_wordpos "
                                       "(word, pos_tag, sentence) "
                                       "VALUES (%s, %s, %s)")
        try:
            # First insert sentence table for a specific language
            cursor.execute(add_sentence, rows[0].sentence)
            insert_sentence_id = cursor.lastrowid
            # Insert TResults batchly
            data = [(row.word, row.pos_tag, insert_sentence_id) for row in rows]
            cursor.executemany(add_words, data)
            self.cnx.commit()
            print('insert data succeed')
        except Exception as e:
            # roll back transaction once happening an error
            cursor.execute('rollback;')
            # TODO: add log
            print('insert error', rows)

    def select_data(self, cursor, word, language):
        """
        This method is mainly used to select data from database
        by input word from web interface

        The returning result can be mapped to TResult
        :param cursor:
        :param word: word wanted to find
        :param language: word subjected to which language
        :return:
        """
        # "select * from Chinese_wordpos as w left join Chinese_sentences as s on w.sentence=s.id limit 1000;"
        try:
            query = ("SELECT word, pos_tag, sentence FROM %s_wordpos "
                     "WHERE  word = %s") % (language, word)

            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as ex:
            print("query error")


# next, we do unit test
if __name__ == '__main__':
    """The ddl srcipt should be executed only once a time """
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

    TABLES_SETENCES = {}
    for language in language_dict.values():
        TABLES_SETENCES[language + '_sentences'] = (
                                             "CREATE TABLE IF NOT EXISTS  `%s_sentences` ("
                                             "  `id` int(11) NOT NULL AUTO_INCREMENT,"
                                             "  `sentence` TEXT NOT NULL,"
                                             "  `create_time` timestamp NULL default CURRENT_TIMESTAMP,"
                                             "  PRIMARY KEY (`id`)"
                                             ") ENGINE=InnoDB") % (language,)

    # login cofig for remote distribution
    # store_data = StoreData('zguo4', 'SJk+6L4K3fKX',
    #                        db_host='db1.mcs.slu.edu',
    #                        db_name='psd_project')

    store_data = StoreData(db_config['user'],
                           db_config['password'],
                           db_host=db_config['db_host'],
                           db_name=None)
    conn = store_data.db_connect()
    store_data.create_database(conn.cursor())
    store_data.create_tables(conn.cursor(), TABLES, TABLES_SETENCES)
    print('Done succeed~')
