import nltk

from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize

while True:
    usr_in = input('enter one word here (enter q to exit): ')
    if usr_in == 'q':
        break

    nltk.download('averaged_perceptron_tagger')

    tokenized = sent_tokenize(usr_in)
    for i in tokenized[:2]:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
                print(tagged)

    nltk.download('wordnet')

    syns = wordnet.synsets(usr_in)

    for syn in syns:
        usr_wrd_tag = print(syn.name())
        usr_wrd_typ = print(syn.lemmas()[0].name())
        usr_wrd_def = print("defintion = ", syn.definition())
        usr_wrd_exp = print("context example = ", syn.examples())

    # this script works for one word only
    # still editing the loop to work for multiple word (n-gram) phrases
