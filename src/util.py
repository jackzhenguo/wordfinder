# util model
# user: zhenguo
# date: 2020.2.28

# TODO: keeping update
language_list = ['Chinese', 'English', 'French', 'Italian', 'Spanish', 'Korean', 'Russian', 'Portuguese']
language_dict = {'1': 'Chinese', '2': 'English', '3': 'French', '4': 'Italian',
                 '5': 'Spanish', '6': 'Korean', '7': 'Russian', '8': 'Portuguese'}

# database config
# cofig for local database
db_config = {'user': 'root',
             'password': 'root@123',
             'db_host': 'localhost',
             'db_name': 'psd_project'}

# language and corresponding file path of corpus
corpus_language = {'Chinese': 'input//corpus//result//zh.txt',
                   'English': 'input//corpus//result//wiki_en.txt',
                   'French': 'input//corpus//result//wiki_fr.txt',
                   'Italian': 'input//corpus//result//wiki_it.txt',
                   'Spanish': 'input//corpus//result//wiki_es.txt',
                   'Korean': 'input//corpus//result//wiki_ko.txt',
                   'Russian': 'input//corpus//result//wiki_ru.txt',
                   'Portuguese': 'input//corpus//result//wiki_pt.txt'}

udpipe_language = {'Chinese': 'input//udpipemodel//chinese-gsdsimp-ud-2.5-191206.udpipe',
                   'English': 'input//udpipemodel//english-ewt-ud-2.5-191206.udpipe',
                   'French': 'input//udpipemodel//french-gsd-ud-2.5-191206.udpipe',
                   'Italian': 'input//udpipemodel//italian-isdt-ud-2.5-191206.udpipe',
                   'Spanish': 'input//udpipemodel//spanish-gsd-ud-2.5-191206.udpipe',
                   'Korean': 'input//udpipemodel//korean-gsd-ud-2.5-191206.udpipe',
                   'Russian': 'input//udpipemodel//russian-gsd-ud-2.5-191206.udpipe',
                   'Portuguese': 'input//udpipemodel//portuguese-gsd-ud-2.5-191206.udpipe'}

word2vec_language = {'Chinese': 'input//word2vecmodel//gensim-word2vec-model-Chinese',
                     'English': 'input//word2vecmodel//gensim-word2vec-model-English',
                     'French': 'input//word2vecmodel//gensim-word2vec-model-French',
                     'Italian': 'input//word2vecmodel//gensim-word2vec-model-Italian',
                     'Spanish': 'input//word2vecmodel//gensim-word2vec-model-Spanish',
                     'Korean': 'input//word2vecmodel//gensim-word2vec-model-Korean',
                     'Russian': 'input//word2vecmodel//gensim-word2vec-model-Russian',
                     'Portuguese': 'input//word2vecmodel//gensim-word2vec-model-Portuguese'}

