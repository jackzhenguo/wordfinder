"""
Creates a corpus from Wikipedia dump file.
Inspired by:
https://github.com/panyang/Wikipedia_Word2vec/blob/master/v1/process_wiki.py
english corpus:
https://dumps.wikimedia.org/enwiki

"""

import sys
from gensim.corpora import WikiCorpus


def make_corpus(in_f, out_f):
    """Convert Wikipedia xml dump file to text corpus"""
    output = open(out_f, 'w')
    wiki = WikiCorpus(in_f)
    i = 0
    for text in wiki.get_texts():
        # output.write(bytes(' '.join(text), 'utf-8').decode('utf-8') + '\n')
        print(text)
        output.write(text)
        i = i + 1
        if i % 10000 == 0:
            print('Processed ' + str(i) + ' articles')
    output.close()
    print('Processing complete!')


if __name__ == '__main__':
    in_f = '/home/zglg/SLU/psd/corpus/english/enwiki-20210301-pages-articles-multistream11.xml-p6899367p7054859.bz2'
    out_f = 'wiki_en2.txt'
    make_corpus(in_f, out_f)
