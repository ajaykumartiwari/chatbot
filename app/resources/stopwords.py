import csv
import json
import random
import string
import warnings
from nltk.corpus import wordnet as wn
import nltk
import numpy as np
from flask_cors import CORS, cross_origin  # Access Cross origin from angular


warnings.filterwarnings("ignore")
# Remove stopwords like a, as ,are, we
from nltk.corpus import stopwords
stopwords.words('english')


def tokenized_user_request(message):
    
    print(" ============ ")
    #user_response=message.lower()
    ########################### STOPWORDS CODE ###########################
    user_req=message.lower()
    tokens = [t for t in user_req.split()] 
    clean_tokens = tokens[:] 
    print("Clean Token ====> ", type(clean_tokens) )
    sr = stopwords.words('english')
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
    freq = nltk.FreqDist(clean_tokens) 
    final_token = []
    for key,val in freq.items(): 
        print ("After removing stopwords =========== > ",str(key) + ':' + str(val))
        final_token.append(key)
        print("Final Token Data ============= >",type(final_token), final_token)
    tup = tuple(final_token)
    
    print("Tuple Is ============> ", tup)
    is_noun = lambda pos: pos[:2] == 'NN'
    nouns = [word for (word, pos) in nltk.pos_tag(tup) if is_noun(pos)] 

    # for w in nouns:
    #     tmp = wn.synsets(w)[0].pos()
    #     print(w, ":", tmp)
    # nouns = [ent.text for ent in nlp(txt) if ent.pos_ == 'NOUN']
    print("noun ============> ", nouns)
    #tokenized_word = ''.join(tup)
    #tokenized_word = nouns[0]
    if( nouns == [] ):
        tup_words = ''.join(tup)
        print("Final tokenised word ======== > ", tup_words)
        return tup_words
    
    tokenized_word = ''.join(nouns)
    print("Final tokenised word ======== > ",tokenized_word)
    return tokenized_word
