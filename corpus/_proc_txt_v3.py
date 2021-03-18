import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize

multi_lang = sorted(wn.langs())

# import _lang_sel.py

usr_in = input('enter one word here: ')

tokenized = sent_tokenize(usr_in)
for i in tokenized[:2]:
    words = nltk.word_tokenize(i)
    tagged = nltk.pos_tag(words)
    print("NLTK Tag = ", tagged)
    
tagged = str(tagged)
char1 = ","
char2 = ")"
tag_str = tagged[tagged.find(char1)+3 : tagged.find(char2)-1]
print("pos_tag = ", tag_str)

"""
char1 = '('
char2 = ')'
mystr = "mystring(123234sample)"
print mystr[mystr.find(char1)+1 : mystr.find(char2)]
123234sample
"""

syns = wordnet.synsets(usr_in)

usr_wrd_tag = syns[0].name()
usr_wrd_typ = syns[0].lemmas()[0].name()
usr_wrd_def = syns[0].definition()
usr_wrd_exp = syns[0].examples()

print(syns[0].name())
print(syns[0].lemmas()[0].name())
print("defintion = ", syns[0].definition())
print("context example = ", syns[0].examples())

# --------------------------------------------------
# extract raw info
char3 = "'"
char4 = ']'
context_build = str(usr_wrd_exp)
new_con_bud = context_build[context_build.find(char3)+1 : context_build.find(char4)-1]
print("context_build = ",new_con_bud)
# --------------------------------------------------

# '"{}"'.format()
usr_wrd_tag_bud = tag_str # '"{}"'.format(tag_str)
usr_wrd_typ_bud = usr_wrd_typ # '"{}"'.format(usr_wrd_typ)
usr_wrd_exp_bud = new_con_bud # '"{}"'.format(new_con_bud)
print(usr_wrd_tag_bud, usr_wrd_typ_bud,usr_wrd_exp_bud) # works

sel_result = (usr_wrd_typ_bud, usr_wrd_tag_bud, usr_wrd_exp_bud)
print("sel_result = ", sel_result)

sel_result2 = (usr_wrd_typ_bud, usr_wrd_tag_bud, [usr_wrd_exp_bud])
print("sel_result2 = ",sel_result2)

sel_dict = {usr_wrd_tag_bud: [usr_wrd_exp_bud]}
print("sel_dict = ",sel_dict)

"""
OUTPUT AFTER USER INPUT USING NLTK 

enter one word here: free
NLTK Tag =  [('free', 'JJ')]
pos_tag =  JJ
free.n.01
free
defintion =  people who are free
context example =  ['the home of the free and the brave']
sel_result =  ('free', 'JJ', ['the home of the free and the brave'])
sel_result2 =  ('free', 'JJ', ['the home of the free and the brave'])
sel_dict =  {'JJ': ['the home of the free and the brave']}

TRYING TO MATCH INPUT:
sel_result = (("sink", "NOUN", "Don't just leave your dirty plates in the sink!"))


              ("sink", "VERB", "The wheels started to sink into the mud."),
              ("sink", "VERB", "How could you sink so low?"))

sel_result2 = (("sink", "NOUN", ["Don't just leave your dirty plates in the sink!"]),
               ("sink", "VERB", ["The wheels, started to sink into the mud.", "How could you sink so low?"]))

sel_dict = {"NOUN": ["Don't just leave your dirty plates in the sink!"],
            "VERB": ["The wheels, started to sink into the mud.", "How could you sink so low?"]}
"""