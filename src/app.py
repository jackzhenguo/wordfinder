# encoding: utf-8
"""
@file: app.py
@desc: flask application for wordfinder
@author: group3
@time: 4/15/2021
"""
import json
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask import Flask, render_template, request, flash, session
from flask_session import Session
import nltk
from src.config import language_dict
from src.service.find_service import FindWordService
from src.service.kwic_service import KWICService
from src.service.cluster_service import ClusterService
from src.logs import Log

nltk.download('stopwords')
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)
log = Log()


@app.route('/')
def index():
    """
    This is the index web page
    :return:index.html
    """
    try:
        log.info('ip %s visiting...' % (request.remote_addr,))
        return render_template('index.html')
    except Exception as e:
        log.error(e)
        return render_template('404.html')


@app.route('/find', methods=['GET'])
def find():
    """
    This method mainly processes the '/find' request
    first, according to form data, select by database to get result
    second, reorganize to certain data structures
    finally, render to result.html
    :return: result.html
    """
    try:
        if request.method == 'GET':
            language_id = request.args['sellanguage']
            language_name = language_dict[language_id]
            sel_word = request.args['selword']
            log.info('user %s searching word %s in %s' % (request.remote_addr, sel_word, language_name))
            session['language_name'] = language_name
            session['sel_word'] = sel_word

            finds = FindWordService()
            succeed = finds.find_word(language_name, sel_word)
            if not succeed:
                flash("not found %s in %s corpus" % (sel_word, language_name))
                return render_template("index.html")
            session['sel_word_pos_dict'] = finds.sel_word_pos_dict
            ks = KWICService(language_name)
            session['kwic_result'] = ks.kwic(sel_word, finds.sel_results)
            light_kwic_result = [(item[0], item[1], item[3]) for item in session['kwic_result']]
            # return json.dumps(session['kwic_result'])
            return render_template('index.html', input_data={"language_id": language_id,
                                                             "language_name": language_name,
                                                             "sel_word": sel_word,
                                                             "sel_result": light_kwic_result})
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
            cluster_number = request.form['clusterNumber']
            sel_word_pos = request.form['tagInput1']
            cs = ClusterService(session['language_name'], session['sel_word'])
            log.info("user %s clustering tag=%s, language=%s, word=%s, cluster_number=%s" % (request.remote_addr,
                                                                                             sel_word_pos,
                                                                                             session['language_name'],
                                                                                             session['sel_word'],
                                                                                             cluster_number))
            cluster_input_sentence = session['sel_word_pos_dict'][sel_word_pos]
            cluster_succeed = cs.cluster_service(cluster_input_sentence, cluster_number)
            if not cluster_succeed:
                flash("invalid cluster number")
                return render_template('result.html', input_data={"language_name": session['language_name'],
                                                                  "sel_word": session['sel_word'],
                                                                  "sel_result": session['kwic_result']})
            sentences, labels = cs.group_sentences()
            return render_template('cluster.html',
                                   cluster_number=cluster_number,
                                   cluster_result=cs.cluster_sentences,
                                   rec_cluster_result=cs.cluster_sentences_rmd,
                                   sentences_with_labels=zip(sentences, labels),
                                   cluster_score=round(cs.best_score, 2))
    except Exception as e:
        log.error(e)
        return render_template('404.html')


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
