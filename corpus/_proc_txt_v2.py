import nltk
from nltk.tokenize import sent_tokenize
# multiple word inputs
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn


usr_in = input("enter word or phrase here: ")

nltk.download('punkt')

tokenized = sent_tokenize(usr_in)
print("tokenized text = ",tokenized)

for items in tokenized:
    space = str(usr_in.isspace()),
    print("user input = ", items)
    print("The number of inputs ",space)

    syns[items] = wordnet(tokenized[items]).synsets()
    print("syns = ", syns(items.count[str(tokenized)]))

    words[items] = nltk.word_tokenize(items)
    print("input grouped = ", words.count(tokenized))

    tagged[items] = nltk.pos_tag(words)
    print("PoS tags = ", tagged)

    # usr_wrd_tag = print(tokenized(items).name(items[int(items)])
    # # usr_wrd_typ = print(syns[0].lemmas()[0].name())
    # usr_wrd_def = print(tokenized(items).definition(items[int(items)]))
    usr_wrd_exp = print("context examples = ",wn.synset('home.n.01').examples())
# this script works for one word only
# still editing the loop to work for multiple word (n-gram) phrases
