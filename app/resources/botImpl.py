 
# FAQ Machine is a Frequently Asked Questions semantic matching application that will produce improved results using NLP features and techniques. This project has implementation of bag-of-words strategy and improved method

import sys
import pandas as pd
import math
import re
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import Counter


""" Database Connection """
from DbConfig.connection import connect_to_database
print("Please Insert a option to connect with Database :")
print("1.  MongoDB   2.  Mysql ")
user_number = input("Please enter your option : ")
args = int(user_number)

#Reading FAQ data from MongoDB Dataase
row = connect_to_database(args)
print("Database", type(row))
if(type(row) == str):
    flag = 0
else:
    flag = 1
#print("Row Data  ======= > ", row)
if(flag == 1):
    #Extracting the questions and answers from the dataframe.
    question = row['Question'].values
    answer = row['Answer'].values

    num_of_results = 10

    #Cosine Similarity function
    WORD = re.compile(r'\w+')

    def cosine_similarity(v1, v2):
        int = set(v1.keys()) & set(v2.keys())
        num = sum([v1[x] * v2[x] for x in int])

        summing1 = sum([v1[x]**2 for x in v1.keys()])
        summing2 = sum([v2[x]**2 for x in v2.keys()])
        den = math.sqrt(summing1) * math.sqrt(summing2)

        if not den:
            return 0.0
        else:
            return float(num) / den

    def text2vec(text):
        words = WORD.findall(text)
        return Counter(words)

    #Downloading Stop words data and punctuation Data
    #nltk.download("stopwords")
    #nltk.download("punkt")

    stopwords = set(stopwords.words('english'))

    #Downloading Lancaster Stemmer
    l_stemmer = LancasterStemmer()

    #Downloading WordNet lemmatizer
    lemmatizer = WordNetLemmatizer()

    #Take the Question and Answers from the whole FAQ data and do the below specified functions

    class FAQ_data:
        def __init__(self, str_question, str_answer):
            self.all_question = []
            self.all_answer = []
            self.all = []
            self.bow = []
            
            # Remove the unwanted spaces, tabs and new line character
            self.str_question = str_question.strip()
            self.str_answer = str_answer.strip()

            # Split the strings (words) into tokens based on whitespace and punctuation
            # Also called as Bag of Words
            self.bag_question = word_tokenize(self.str_question)
            self.bag_answer = word_tokenize(self.str_answer)

            #Count the number of tokens in the bag
            self.counter_question = Counter(self.bag_question)
            self.counter_answer = Counter(self.bag_answer)
            
            # Tag the Question and Answer tokens based on POS in the form of (token, token's POS)
            self.bag_question_pos = nltk.pos_tag(self.bag_question)
            self.bag_answer_pos = nltk.pos_tag(self.bag_answer)

            # Filtering stop words from the bag of tokens
            self.bag_question_sw_removed = [word for word in self.bag_question if word.lower() not in stopwords]
            self.bag_answer_sw_removed = [word for word in self.bag_answer if word.lower() not in stopwords]
            self.all_question +=self.bag_question_sw_removed
            self.all_answer+=self.bag_answer_sw_removed

            # Reducing each token to its root or base word : Stemming
            self.bag_question_stemmed = []
            self.bag_answer_stemmed = []
            for word in self.bag_question:
                self.bag_question_stemmed.append(l_stemmer.stem(word))
            for word in self.bag_answer:
                self.bag_answer_stemmed.append(l_stemmer.stem(word))
                
            self.all_question +=self.bag_question_stemmed
            self.all_answer+=self.bag_answer_stemmed

            # Group tokens based on the words lemma
            self.bag_question_lemmatized = []
            self.bag_answer_lemmatized = []
            for word in self.bag_question:
                self.bag_question_lemmatized.append(lemmatizer.lemmatize(word))
            for word in self.bag_answer:
                self.bag_answer_lemmatized.append(lemmatizer.lemmatize(word))
                
            self.all_question +=self.bag_question_lemmatized
            self.all_answer+=self.bag_answer_lemmatized

            # Tree parsing representing the syntactic structure of a based on context-free grammar
            self.sent_question = sent_tokenize(self.str_question)
            self.sent_answer = sent_tokenize(self.str_answer)
            # self.parse_tree_q = parser.raw_parse_sents(self.sent_question)
            # self.parse_tree_a = parser.raw_parse_sents(self.sent_answer)

            # Extracting hypernymns, hyponyms, meronyms, holonyms from Wordnet 
            self.hypernymns = []
            self.hyponyms = []
            self.meronyms = []
            self.holonyms = []
            self.bag_counter = Counter(self.bag_question_sw_removed) + Counter(self.bag_answer_sw_removed)
            for word in self.bag_counter.keys():
                synsets = wn.synsets(word)
                if synsets:
                    max_cos = 0.0
                    target_synset = None
                    for synset in synsets:
                        definition = synset.definition()
                        cos = cosine_similarity(Counter(self.bag_question + self.bag_answer), Counter(definition))
                        if cos > max_cos:
                            max_cos = cos
                            target_synset = synset
                    if target_synset is None:
                        target_synset = synsets[0]
                    if target_synset.hypernyms():
                        self.hypernymns += target_synset.hypernyms()
                    if target_synset.hyponyms():
                        self.hyponyms += target_synset.hyponyms()
                    if target_synset.part_meronyms():
                        self.meronyms += target_synset.part_meronyms()
                    if target_synset.part_holonyms():
                        self.holonyms += target_synset.part_holonyms()
            
            self.all = self.all_question + self.hypernymns + self.hyponyms + self.meronyms + self.holonyms + self.all_answer 
            
            self.bow = self.bag_question + self.bag_answer 
            
        def print(self):
            print("Question:", self.str_question)
            print("Answer:", self.str_answer)

        def print_bag(self):
            print("Question:", self.bag_question)
            print("Answer:", self.bag_answer)

        def print_counter(self):
            print("Question:", self.counter_question)
            print("Answer:", self.counter_answer)

        def concat(self):
            return self.bag_question+self.bag_answer

        def print_all_features(self):
            print(self.str_question)
            print(self.str_answer)
            print("***** Removing Stop Words *****")
            print('\t\t', self.bag_question_sw_removed)
            print('\t\t', self.bag_answer_sw_removed)
            print("***** Stemming Words *****")
            print('\t\t', self.bag_question_stemmed)
            print('\t\t', self.bag_answer_stemmed)
            print("***** Lemmatizing Words *****")
            print('\t\t', self.bag_question_lemmatized)
            print('\t\t', self.bag_answer_lemmatized)
            print("***** Tagging with Parts of Speech *****")
            print('\t\t', self.bag_question_pos)
            print('\t\t', self.bag_answer_pos)
            print("***** Implementing Word net features *****")
            print("***** Adding Hypernyms *****")
            print('\t\t', self.hypernymns)
            print("***** Adding Hyponyms *****")
            print('\t\t', self.hyponyms)
            print("***** Adding Meronyms *****")
            print('\t\t', self.meronyms)
            print("***** Adding Holonyms *****")
            print('\t\t', self.holonyms)        

    # In[6]:

    faq_corpus = []
    for text in range(70):
        faq_corpus.append(FAQ_data(question[text], answer[text]))

    print("Tokenized successully")

    # In[1]:

    flag=True
    print("Jarvis: My name is Jarvis.I am here to clear your queries. If you want to exit, type Bye!")
    def response(user_request):
        while(flag==True):
            user_query = user_request
        
            #user_query = input("For help menu: Enter jarvis \nEnter your question:\n")
            print("********************************************************")
            options = "Manual: \n faq: Show original data"+"\n bow: Bag of Words"+"\n count: Show the count"+"\n feature: Show all the features"
            if user_query == "jarvis":
                print(options)
                return "Please See the Log"
            elif user_query == "faq":
                print(row)
                return "Please See the Log"
            elif user_query == "show":
                for faq in faq_corpus:
                    print(faq_corpus.index(faq))
                    faq.print()
                return "Please See the Log"
            elif user_query == "bow":
                for faq in faq_corpus:
                    filtered_sentence = faq_corpus.index(faq)
                    print(filtered_sentence)
                    faq.print_bag()
                #filtered_sentence = [w for w in faq if not w in stopwords]
                return "Please See the Log"

            elif user_query == "count":
                for faq in faq_corpus:
                    print(faq_corpus.index(faq))
                    faq.print_counter()
                return "Please See the Log"
            elif user_query == "feature":
                for faq in faq_corpus:
                    print(faq_corpus.index(faq))
                    faq.print_all_features()
                return "Please See the Log"
            else:
                # Remove the unwanted spaces, tabs and new line character
                user_input = user_query.strip()

                # Split the strings (words) into tokens based on whitespace and punctuation
                # Also called as Bag of Words
                user_sents = sent_tokenize(user_input)
                user_bag = word_tokenize(user_input)

                # Tag the Question and Answer tokens based on POS in the form of (token, token's POS)
                user_pos = nltk.pos_tag(user_bag) 

                # Filtering stop words from the bag of tokens
                user_sw_removed = [w for w in user_bag if w.lower() not in stopwords]

                # Reducing each token to its root or base word : Stemming
                user_stemmed = []
                user_lemmatized = []
                for word in user_bag:
                    user_stemmed.append(l_stemmer.stem(word))
                    user_lemmatized.append(lemmatizer.lemmatize(word))

                # Tree parsing representing the syntactic structure of a based on context-free grammar
                # user_tree = parser.raw_parse_sents(user_sents)

                # Extracting hypernymns, hyponyms, meronyms, holonyms from Wordnet 
                user_hypernymns = []
                user_hyponyms = []
                user_meronyms = []
                user_holonyms = []
                user_bag_counter = Counter(user_sw_removed)
                for word in user_bag_counter.keys():
                    synsets = wn.synsets(word)
                    if synsets:
                        max_cos = 0.0
                        output_synset = None
                        for synset in synsets:
                            definition = synset.definition()
                            cos = cosine_similarity(Counter(user_bag), Counter(definition))
                            if cos > max_cos:
                                max_cos = cos
                                output_synset = synset
                        if output_synset is None:
                            output_synset = synsets[0]
                        if output_synset.hypernyms():
                            user_hypernymns += output_synset.hypernyms()
                        if output_synset.hyponyms():
                            user_hyponyms += output_synset.hyponyms()
                        if output_synset.part_meronyms():
                            user_meronyms += output_synset.part_meronyms()
                        if output_synset.part_holonyms():
                            user_holonyms += output_synset.part_holonyms()
                # Taking the features into a bag
                user_bag += user_hypernymns + user_hyponyms + user_meronyms + user_holonyms + user_stemmed + user_lemmatized
                user_counter = Counter(user_bag)
                cos_counter = {}
                for faq in faq_corpus:
                    cos = cosine_similarity(user_counter, Counter(faq.all))
                    cos_counter[faq_corpus.index(faq)] = cos

                show_count = 0
                final_response = ''
                res = ''
                for index in sorted(cos_counter, key=cos_counter.get, reverse=True):
                    if cos_counter[index] > 0 and show_count < num_of_results:
                        print("*****FAQ Index: ", index, "\t*****Cosine Similarity: ", cos_counter[index])
                        faq_corpus[index].print()
                        #print("index--->",index)
                        #final_response = answer[index]
                        #print("Answer ready to return ================>", final_response)
                        print()
                        if(show_count == 0 and cos_counter[index]):
                            res = answer[index]
                        show_count += 1
                    #     return final_response 
                    # else:
                    #     final_response = final_response+"I am sorry! I don't understand you"
                    #     return final_response   
                if res != '':
                    return res
                else:
                    final_response = final_response+"I am sorry! I don't understand you"
                    return final_response
else:
    print("Your Selected Database is not connected")
    # return "Database Not Connected"
    def response(user_request):
        return "Database Not Connected"

#row = getAllRecords()
#print("Inside Bot Impl Method =========================>>\n",row)

#print("Inside Impl Questions ============> \n",question)

      