
# import nltk
# import warnings
# import json
# warnings.filterwarnings("ignore")
# import csv
# import numpy as np
# import random
# import string
# from resources.ReadData import readFile
# import pandas as pd

# """ MongoDb Connection """
# from DbConfig.connection import getAllRecords

# #row = readFile()
# row = getAllRecords()
# print("Inside Impl Method row data", type(row))
# #nltk.download('punkt')
# #nltk.download('wordnet')

# from flask import Flask, jsonify

# # f=open('chatbot.txt','r',errors = 'ignore')
# # var = 100
# # if var == 100:
# #     raw=f.read()
# #     print("File reading done!")
# # raw=raw.lower()

# sent_tokens = nltk.sent_tokenize(row)
# word_tokens = nltk.word_tokenize(row)

# lemmer = nltk.stem.WordNetLemmatizer()

# def LemTokens(tokens):
#     return [lemmer.lemmatize(token) for token in tokens]
# remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# def LemNormalize(text):
#     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def response(user_response):
#     # sent_tokens = nltk.sent_tokenize(user_response)
#     # word_tokens = nltk.word_tokenize(user_response)
#     req = user_response
#     robo_response=''
#     sent_tokens.append(user_response)
#     print("sent_tokens==============>", sent_tokens, type(sent_tokens))
#     TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
#     tfidf = TfidfVec.fit_transform(sent_tokens)
    
#     cols = TfidfVec.get_feature_names()
#     matrix = tfidf.todense()
#     print(pd.DataFrame(matrix,columns = cols))
    
#    # print("Word Matrix :",matrix)
#     vals = cosine_similarity(tfidf[-1], tfidf)
#     idx=vals.argsort()[0][-2]
#     flat = vals.flatten()
#     flat.sort()
#     req_tfidf = flat[-2]
#     if(req_tfidf==0):
#         robo_response=robo_response+"I am sorry! I don't understand you"
#         return robo_response
#     else:
#         robo_response = robo_response+sent_tokens[idx]   
#         # print("Robo Response ===============================>",robo_response)
#         # res = connect(robo_response)
#         # print("Data Type =========>",type(res))
#         # print(res['answer'])
#         # answer = res['answer']
#         # print(answer)
#         return robo_response

# print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")