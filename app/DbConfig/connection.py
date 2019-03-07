import sys
import os
from pymongo import MongoClient
import nltk
import warnings
import json
warnings.filterwarnings("ignore")
import csv
import numpy as np
import random
import string
from flask import Flask, jsonify, redirect, request, url_for
import pandas as pd

#============================ Run a batch file ============================#

# from subprocess import run
# run(".\conn.bat")

def connect_to_database(argument):
    switcher = {
        1: mongodb,
        2: mysql,
        3: cassandra,
        4: neo4j
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, "nothing")
    return func()

def mongodb():
    """ Database connection """
    global conn
    client = MongoClient('localhost', 27017)
    db = client.chatbot
    conn = db.bankFaq
    print("Mongo Database Connected")
    return getAllRecords()
 
def mysql():
    print("Mysql Database not connected")
    test = "Mysql Database"
    return test
 
def cassandra():
    return "Cassandra Database Connected"
 
def neo4j():
    return "Neo4J Connected"
 

# """ Database connection """
# client = MongoClient('localhost', 27017)
# db = client.chatbot
# conn = db.bankFaq

def getAllRecords():
    if(conn != ''):
        question = []
        answer = []
        for records in conn.find({}):
            question.append(records['Question'])
            answer.append(records['Answer'])

        quest = pd.DataFrame({'Question' : question})
        ans = pd.DataFrame({'Answer' : answer})
        results = [quest,ans]
        #result = quest.append(ans)
        result = pd.concat(results,axis=1, join='inner')

        #print("Conversation from database ===========> \n",result)
        return result #return as JSON all the records
    else:
        print("Your Selected Database Not connected")
        