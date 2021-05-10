# encoding: utf-8
"""
@file: app.py
@desc: flask application for wordfinder
@author: group3
@time: 4/15/2021
"""
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask import Flask, render_template, request, flash
import nltk
from src.config import language_dict, word2vec_language
from src.service import AppService, AppContext
from src.logs import Log

nltk.download('stopwords')
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app_service = AppService()

log = Log()


@app.route('/')
def index():
    """
    This is the index web page
    :return:index.html
    """
    try:
        return render_template('index.html')
    except Exception as e:
        log.error(e)
        return render_template('404.html')


@app.route('/find', methods=['POST'])
def find():
    """
    This method mainly processes the '/find' request
    first, according to form data, select by database to get result
    second, reorganize to certain data structures
    finally, render to result.html
    :return: result.html
    """
    try:
        language_name, sel_word = None, None
        if request.method == 'POST':
            language_id = request.form['sellanguage']
            sel_word = request.form['selword']
            language_name = language_dict[language_id]

            if AppContext.sel_language != language_name or not AppContext.udt_pre_model:
                app_service.config_udpipe(language_name, AppContext.db_conn)

            AppContext.sel_language = language_name
            AppContext.sel_word = sel_word

            app_service.find_service(language_name, sel_word)
            app_service.kwic(sel_word, AppContext.sel_results)

        return render_template('result.html', input_data={"language_name": language_name,
                                                          "sel_word": sel_word,
                                                          "sel_result": AppContext.sentence_kwic})
    except Exception as e:
        log.error(e)
        return render_template('404.html')


@app.route('/find2', methods=['POST'])
def find2():
    try:
        language_name, sel_word = None, None
        if request.method == 'POST':
            language_name = request.form['sellanguage']
            sel_word = request.form['selword']
            if AppContext.sel_language != language_name or not AppContext.udt_pre_model:
                app_service.config_udpipe(language_name, AppContext.db_conn)
            if AppContext.sel_word != sel_word:
                AppContext.sel_word = sel_word
                AppContext.sel_language = language_name
                app_service.find_service(language_name, sel_word)
                app_service.kwic(sel_word, AppContext.sel_results)
        return render_template('result.html', input_data={"language_name": language_name,
                                                          "sel_word": sel_word,
                                                          "sel_result": AppContext.sentence_kwic})
    except Exception as e:
        log.error(e)
        return render_template('404.html')


@app.route('/cluster', methods=['POST'])
def cluster():
    """
    this method is mainly to solve the cluster question

    After getting form data, begining cluster
    finally return cluster example sentences
    :return:cluster.html
    """
    try:
        if request.method == 'POST':
            language_name = request.form['languageName']
            cluster_number = request.form['clusterNumber']
            AppContext.sel_word_pos = request.form['tagInput1']
            if language_name is None:
                language_name = AppContext.sel_language
            if AppContext.sel_language is None:
                AppContext.sel_language = language_name

            if AppContext.sel_word_pos_dict is None:
                app_service.find_service(AppContext.sel_language, AppContext.sel_word)
            cluster_input_sentence = AppContext.sel_word_pos_dict[AppContext.sel_word_pos]
            if not AppContext.udt_pre_model:
                app_service.config_udpipe(language_name, AppContext.db_conn)

            cluster_model_file = word2vec_language[language_name]

            cluster_succeed = app_service.cluster_service(cluster_model_file,
                                                          cluster_input_sentence, cluster_number)

            if not AppContext.cluster_sentences:
                if not cluster_succeed:
                    flash("invalid cluster number")
                    return render_template('result.html', input_data={"language_name": language_name,
                                                                      "sel_word": AppContext.sel_word,
                                                                      "sel_result": AppContext.sentence_kwic})
            sentences, labels = AppService.group_sentences()
            return render_template('cluster.html',
                                   cluster_number=cluster_number,
                                   cluster_result=AppContext.cluster_sentences,
                                   rec_cluster_result=AppContext.cluster_sentences_rmd,
                                   sentences_with_labels=zip(sentences, labels),
                                   cluster_score=round(AppContext.best_score, 2))
    except Exception as e:
        log.error(e)
        return render_template('404.html')


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
