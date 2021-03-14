import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize

usr_in = input('enter one word here: ')

tokenized = sent_tokenize(usr_in)
for i in tokenized[:2]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)

syns = wordnet.synsets(usr_in)

usr_wrd_tag = print(syns[0].name())
usr_wrd_typ = print(syns[0].lemmas()[0].name())
usr_wrd_def = print("defintion = ", syns[0].definition())
usr_wrd_exp = print("context example = ", syns[0].examples())

antonyms = []
for syn in wordnet.synsets(usr_in):
    for lm in syn.lemmas():
        if lm.antonyms():
            antonyms.append(lm.antonyms()[0].name())

print("antonyms = ", set(antonyms))
