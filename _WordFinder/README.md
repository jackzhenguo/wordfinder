# wordfinder

## 1 clone this repository

git clone git@git.cs.slu.edu:psd-project/wordfinder.git

If prompts you permission denied or enter your password or whatever, then you should follow this:

https://stackoverflow.com/questions/2643502/how-to-solve-permission-denied-publickey-error-when-using-git

last step you need to put your local "id_rsa. pub" file content to your "SSH keys" where it is in your gitlab Settings(top-right corner) and then you would see it left side: SSH keys.


By the way if you had any problem, please feel for free to contact me. 


Also, you can git clone https://oauth2:pZkqPY8oKTrx5KNCU8vy@git.cs.slu.edu/psd-project/wordfinder.git

but it's not the recommended way.

## Get Started

Current level we have a demo version following: 

First, select English language

Second, enter the word: sink, then click "Find" button

Enjoy the demo! Only support to show.

## 2 product backlog 

### 2.1 main functions of product

what's the main functionality of our product?
1.  support multilingualism
2.  enter a word and word's Part-Of-Speech, return corresponding sentences as fast as possible
3. Should then “cluster” those sentences into examples with related senses; Present to the user one or more “clusters” of example sentences
4. Must allow the user to examine, then change the number of clusters

### 2.2 Three main modules of big task

1. Database: gather and store text corpora in many languages in a way that makes queries of the type we want (word/part-of-speech lookup) fast and easy
2. Analysis: code to cluster example sentences containing given word; interesting machine learning approaches here that I’ll explain eventually!
3. Front end: simple, usable interface; must work on any platform, and should support messages/menu items in multiple languages

## 3 Sprint backlog

### 3.1 alpha version

what's the main functionality of the alpha version (deadline March 19)?
1. support at least two languages
2. finish design of database tables , including: word-tag-sentence table as language type, such as English table:

| word_name | pos_tag |                                        sentence |
| :-------- | :-----: | ----------------------------------------------: |
| sink      |  NOUN   | Don't just leave your dirty plates in the sink! |
| sink      |  VERB   |        The wheels started to sink into the mud. |
| sink      |  VERB   |                      How could you sink so low? |

3. Also, as fields above, we should train data and get tags of each word in our selected corpus and then put results to write into tables such as table called English_data, another table called Chinese_data, etc.

4. finish front-end disign, including available to any platform, supporting to enter word text box and supporting to  select messages/menu items in multiple languages, etc.

5. a simple alogrithm to implement “cluster” functionality: sentences found by search into examples with related senses.

6. support users to change the number of clusters. 

**Tips:**
- in alpha version we don't need to care to much about the number of words and maybe one millon words are OK, but need to support at least two language  
- Note a possible little trick: **sort** table accordig to alphabeta order.

- Preference choices for sql database is mysql

- NOTE We only return the sentences that **exactly** contain searched word, such as sink rather than sunk and sinking, etc.

- universal dependencies POS tag types: 

  - [ADJ](https://universaldependencies.org/u/pos/ADJ.html): adjective
  - [ADP](https://universaldependencies.org/u/pos/ADP.html): adposition
  - [ADV](https://universaldependencies.org/u/pos/ADV.html): adverb
  - [AUX](https://universaldependencies.org/u/pos/AUX_.html): auxiliary
  - [CCONJ](https://universaldependencies.org/u/pos/CCONJ.html): coordinating conjunction
  - [DET](https://universaldependencies.org/u/pos/DET.html): determiner
  - [INTJ](https://universaldependencies.org/u/pos/INTJ.html): interjection
  - [NOUN](https://universaldependencies.org/u/pos/NOUN.html): noun
  - [NUM](https://universaldependencies.org/u/pos/NUM.html): numeral
  - [PART](https://universaldependencies.org/u/pos/PART.html): particle
  - [PRON](https://universaldependencies.org/u/pos/PRON.html): pronoun
  - [PROPN](https://universaldependencies.org/u/pos/PROPN.html): proper noun
  - [PUNCT](https://universaldependencies.org/u/pos/PUNCT.html): punctuation
  - [SCONJ](https://universaldependencies.org/u/pos/SCONJ.html): subordinating conjunction
  - [SYM](https://universaldependencies.org/u/pos/SYM.html): symbol
  - [VERB](https://universaldependencies.org/u/pos/VERB.html): verb
  - [X](https://universaldependencies.org/u/pos/X.html): other

- more important and useful links about how we develop this project have put at [tmp](./tmp) folder


### 3.2 beta version

what's the main function of the beta version (deadline April 9 )?

to do

### 3.3 final version

what's the main function of the final version (deadline )?

to do

## development tools

tips:
- based on Dr.Scannell materials that contains important corpus we need, like UD
, and tools for POS tag like UDpipe. Once we build some codes, then we can write data to our tables of database, which is very important.

- Python as development language and  web application 
- our repository: https://git.cs.slu.edu/psd-project/wordfinder/-/project_members
- flask as the web framework as convenient 
- unit test 

## how assign to individual of group


## TODO list

HERE we make development plans, dicuss them and pass them. Then we should followthese plans to start. If happing a problem in development, you should tell us in time and then we group should sovle it together before deadline.

2/16/2021 - 2/21/2021 TASKS

Sprint 1
1. Develop UI in any language 
2. Obtain Corpus 
3. Clean the Corpus(Tokenization, lemmatization and stemming)
4. Tag the data according the POS

# wordfinder
