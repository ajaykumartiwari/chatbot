import csv
import json
import random
import string
import warnings

import nltk
import numpy as np

warnings.filterwarnings("ignore")

def readFile():
    f=open('chatbot.txt','r',errors = 'ignore')
    var = 100
    if var == 100:
        raw=f.read()
        print("File reading done!")
    raw=raw.lower()
    return raw
