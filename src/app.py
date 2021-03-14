from flask import Flask, render_template, request, redirect, url_for, flash
from instance import language_dict

app = Flask(__name__)


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
    if request.method == 'POST':
        language_id = request.form['sellanguage']
        sel_word = request.form['selword']
        language_name = language_dict[language_id]
        # select by database
        # TODO
        # demo result
        sel_result = (("sink", "NOUN", "Don't just leave your dirty plates in the sink!"),
                      ("sink", "VERB", "The wheels started to sink into the mud."),
                      ("sink", "VERB", "How could you sink so low?"))
        # analysis
        # groupby column0 and column1
        # care: type of third element for result_dict is a list
        sel_result2 = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
                       ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]))

        global sel_dict
        sel_dict = {"NOUN": ["Don't just leave your dirty plates in the sink!"],
                    "VERB": ["The wheels, started to sink into the mud.", "How could you sink so low?"]}
    return render_template('result.html', input_data={"language_name": language_name,
                                                      "sel_word": sel_word,
                                                      "sel_result": sel_result2})


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
        cluster_input_sentence = sel_dict[sel_tag]
        # add cluster
        # TODO
        # demo method
        cluster_result = [cluster_input_sentence[0]]
        return render_template('cluster.html', cluster_number=cluster_number, cluster_result=cluster_result);


if __name__ == '__main__':
    app.run(port=3000, debug=True)
