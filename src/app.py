from typing import Any

from flask import Flask, render_template, request, redirect, url_for, flash
from collections import defaultdict
import json

from wordfinder.src.train.result_model import TResult
from wordfinder.src.train.store import StoreData
from wordfinder.src.util import language_dict, language_list, db_config
from wordfinder.src.service import AppService

app = Flask(__name__)

appService = AppService()


@app.route('/')
def index():
    """
    This is the index web page

    :return:index.html
    """
    return render_template('index.html')


@app.route('/find', methods=['POST'])
def find():
    """
    this method mainly solve /find request

    first, according to form data, select by database to get result
    second, reorganize to certain data structures
    finally, render to result.html
    :return: result.html
    """
    language_name, sel_word = None, None
    if request.method == 'POST':
        language_id = request.form['sellanguage']
        sel_word = request.form['selword']
        language_name = language_dict[language_id]
        appService.find_service(language_name, sel_word)
    return render_template('result.html', input_data={"language_name": language_name,
                                                      "sel_word": sel_word,
                                                      "sel_result": appService.sel_result})


@app.route('/find2', methods=['POST'])
def find2():
    language_name, sel_word = None, None
    if request.method == 'POST':
        language_name = request.form['sellanguage']
        sel_word = request.form['selword']
        appService.find_service(language_name, sel_word)
    return render_template('result.html', input_data={"language_name": language_name,
                                                      "sel_word": sel_word,
                                                      "sel_result": appService.sel_result})


@app.route('/cluster', methods=['POST'])
def cluster():
    """
    this method is mainly to solve the cluster question

    After getting form data, begining cluster
    finally return cluster example sentences
    :return:cluster.html
    """
    if request.method == 'POST':
        cluster_number = request.form['clusterNumber']
        sel_tag = request.form['tagInput1']
        cluster_input_sentence = appService.pos_dict[sel_tag]
        # add cluster
        # TODO
        # demo method
        cluster_result = [cluster_input_sentence[0]]
        return render_template('cluster.html', cluster_number=cluster_number, cluster_result=cluster_result)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
