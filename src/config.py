"""
@file: config.py
@desc: utility model
@author: group3
@time: 2/28/2021
"""

import base64
import os

pwd = base64.b64decode(b'TGh4R3oxMDIyMzE=')

language_list = ['Chinese',
                 'English',
                 'French',
                 'Italian',
                 'Spanish',
                 'Korean',
                 'Russian',
                 'Portuguese']

language_dict = {'1': 'Chinese',
                 '2': 'English',
                 '3': 'French',
                 '4': 'Italian',
                 '5': 'Spanish',
                 '6': 'Korean',
                 '7': 'Russian',
                 '8': 'Portuguese'}

# database config, remote mysql
db_config = {'user': 'root',
             'password': pwd.decode("utf-8"),
             'db_host': '192.144.171.233',
             'db_name': 'psd_project'}

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# language and corresponding file path of corpus
corpus_language = {'Chinese': os.path.join(root_path, 'input//corpus//result//zh.txt'),
                   'English': os.path.join(root_path, 'input//corpus//result//wiki_en.txt'),
                   'French': os.path.join(root_path, 'input//corpus//result//wiki_fr.txt'),
                   'Italian': os.path.join(root_path, 'input//corpus//result//wiki_it.txt'),
                   'Spanish': os.path.join(root_path, 'input//corpus//result//wiki_es.txt'),
                   'Korean': os.path.join(root_path, 'input//corpus//result//wiki_ko.txt'),
                   'Russian': os.path.join(root_path, 'input//corpus//result//wiki_ru.txt'),
                   'Portuguese': os.path.join(root_path, 'input//corpus//result//wiki_pt.txt')}

udpipe_language = {'Chinese': os.path.join(root_path, 'input//udpipemodel//chinese-gsdsimp-ud-2.5-191206.udpipe'),
                   'English': os.path.join(root_path, 'input//udpipemodel//english-ewt-ud-2.5-191206.udpipe'),
                   'French': os.path.join(root_path, 'input//udpipemodel//french-gsd-ud-2.5-191206.udpipe'),
                   'Italian': os.path.join(root_path, 'input//udpipemodel//italian-isdt-ud-2.5-191206.udpipe'),
                   'Spanish': os.path.join(root_path, 'input//udpipemodel//spanish-gsd-ud-2.5-191206.udpipe'),
                   'Korean': os.path.join(root_path, 'input//udpipemodel//korean-gsd-ud-2.5-191206.udpipe'),
                   'Russian': os.path.join(root_path, 'input//udpipemodel//russian-gsd-ud-2.5-191206.udpipe'),
                   'Portuguese': os.path.join(root_path, 'input//udpipemodel//portuguese-gsd-ud-2.5-191206.udpipe')}

word2vec_language = {'Chinese': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-Chinese'),
                     'English': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-English'),
                     'French': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-French'),
                     'Italian': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-Italian'),
                     'Spanish': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-Spanish'),
                     'Korean': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-Korean'),
                     'Russian': os.path.join(root_path, 'input//word2vecmodel//gensim-word2vec-model-Russian'),
                     'Portuguese': os.path.join(root_path,  'input//word2vecmodel//gensim-word2vec-model-Portuguese')}



