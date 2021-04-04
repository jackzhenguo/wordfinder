# util model
# user: zhenguo
# date: 2020.2.28

# TODO: keeping update
language_list = ['Chinese', 'English', 'French', 'Italian', 'Japanese', 'Korean', 'Russian']
language_dict = {'1': 'Chinese', '2': 'English', '3': 'French', '4': 'Italian',
                 '5': 'Japanese', '6': 'Korean', '7': 'Russian'}

# database config
# cofig for local database
db_config = {'user': 'root',
             'password': 'root@123',
             'db_host': 'localhost',
             'db_name': 'psd_project'}

# language and corresponding file path of corpus
corpus_language = {'Chinese': 'input//chinese//平凡的世界.txt',
                   'English': 'input//english//wiki_en.txt',
                   'French': '',
                   'Italian': '',
                   'Japanese': '',
                   'Korean': '',
                   'Russian': ''}

udpipe_language = {'Chinese': 'input//udpipemodel//chinese-gsdsimp-ud-2.5-191206.udpipe',
                   'English': 'input//udpipemodel//english-ewt-ud-2.5-191206.udpipe',
                   'French': '',
                   'Italian': '',
                   'Japanese': '',
                   'Korean': '',
                   'Russian': ''}

word2vec_language = {'Chinese': 'input//word2vecmodel//gensim-word2vec-model-Chinese',
                     'English': 'input//word2vecmodel//gensim-word2vec-model-English',
                     'French': '',
                     'Italian': '',
                     'Japanese': '',
                     'Korean': '',
                     'Russian': ''}

