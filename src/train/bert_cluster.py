import en_trf_bertbaseuncased_lg


def bert_en(sentences: List[str]):
    nlp = en_trf_bertbaseuncased_lg.load()
    sents_vectors = []
    for sent in sentences:
        sent_vect = nlp(sent).vector
        sents_vectors.append(sent_vect)


if __name__ == "__main__":
    bert_en([])
