import nltk
from nltk.corpus import treebank
from nltk.stem import WordNetLemmatizer

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')

EXAMPLE_TEXT = "Hello World! Isn't it good to see you? Thanks for buying this book."
tokens = nltk.word_tokenize(EXAMPLE_TEXT)
tagged = nltk.pos_tag(tokens)
print(tagged[0:10])  # part of speech


EXAMPLE_TEXT = "I am very excited about the next generation of Apple products."
tokens = nltk.word_tokenize(EXAMPLE_TEXT)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
print(entities)


t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t.draw()


lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('cooking'))
print(lemmatizer.lemmatize('cooking', pos='v'))
print(lemmatizer.lemmatize('cookbooks'))